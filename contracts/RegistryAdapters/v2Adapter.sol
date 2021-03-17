// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

import "../../interfaces/Yearn/V2Vault.sol";
import "../../interfaces/Yearn/IV2Registry.sol";
import "../../interfaces/Common/IERC20.sol";
import "../../interfaces/Common/Oracle.sol";

contract RegisteryAdapterV2Vault {
    address public registryAddress;
    string public constant registryType = "v2Adapter";
    Oracle public oracle;

    struct Asset {
        string name;
        address id;
        string version;
        AssetMetadata metadata;
    }

    // TODO: Inherit from standardized interface?
    struct Position {
        address assetId;
        uint256 depositedBalance;
        uint256 tokenBalance;
        uint256 tokenAllowance;
    }

    struct AssetMetadata {
        address controller;
        uint256 totalAssets;
        uint256 totalSupply;
        uint256 pricePerShare;
    }

    constructor(address _registryAddress, address _oracleAddress) {
        require(_registryAddress != address(0), "Missing registry address");
        registryAddress = _registryAddress;
        oracle = Oracle(_oracleAddress);
    }

    function getAssetsLength() public view returns (uint256) {
        IV2Registry registry = IV2Registry(registryAddress);
        uint256 numTokens = registry.numTokens();
        uint256 numVaults;
        for (uint256 i = 0; i < numTokens; i++) {
            address currentToken = registry.tokens(i);
            uint256 numVaultsForToken = registry.numVaults(currentToken);
            numVaults += numVaultsForToken;
        }
        return numVaults;
    }

    function getAssetsAddresses() public view returns (address[] memory) {
        uint256 numVaults = getAssetsLength();
        address[] memory vaultAddresses = new address[](numVaults);
        IV2Registry registry = IV2Registry(registryAddress);
        uint256 numTokens = registry.numTokens();
        uint256 currentVaultIdx;
        for (uint256 tokenIdx = 0; tokenIdx < numTokens; tokenIdx++) {
            address currentTokenAddress = registry.tokens(tokenIdx);
            uint256 numVaultsForToken = registry.numVaults(currentTokenAddress);
            for (
                uint256 vaultTokenIdx = 0;
                vaultTokenIdx < numVaultsForToken;
                vaultTokenIdx++
            ) {
                address currentVaultAddress =
                    registry.vaults(currentTokenAddress, vaultTokenIdx);
                vaultAddresses[currentVaultIdx] = currentVaultAddress;
                currentVaultIdx++;
            }
        }
        return vaultAddresses;
    }

    function getAssetTvl(address vaultAddress) public view returns (uint256) {
        V2Vault vault = V2Vault(vaultAddress);
        uint256 valueInToken = vault.totalAssets();
        address underlyingTokenAddress = vault.token();
        IERC20 underlyingToken = IERC20(underlyingTokenAddress);
        uint256 underlyingTokenDecimals = underlyingToken.decimals();

        uint256 usdcDecimals = 6;
        uint256 decimalsAdjustment = underlyingTokenDecimals - usdcDecimals;
        uint256 price = oracle.getPriceUsdc(underlyingTokenAddress);
        uint256 tvl;
        if (decimalsAdjustment > 0) {
            tvl =
                (valueInToken * price * (10**decimalsAdjustment)) /
                10**(decimalsAdjustment + underlyingTokenDecimals);
        } else {
            tvl = (valueInToken * price) / 10**usdcDecimals;
        }
        return tvl;
    }

    function getAssetsTvl() external view returns (uint256) {
        uint256 tvl;
        address[] memory assetAddresses = getAssetsAddresses();
        uint256 numberOfAssets = assetAddresses.length;
        Asset[] memory assets = new Asset[](numberOfAssets);
        for (uint256 i = 0; i < numberOfAssets; i++) {
            address assetAddress = assetAddresses[i];
            uint256 assetTvl = getAssetTvl(assetAddress);
            tvl += assetTvl;
        }
        return tvl;
    }

    // TODO: Add metadata for vault upgrades/versioning
    function getAsset(address vaultAddress) public view returns (Asset memory) {
        V2Vault vault = V2Vault(vaultAddress);
        string memory vaultName = vault.name();
        uint256 totalAssets = vault.totalAssets();
        uint256 totalSupply = vault.totalSupply();
        uint256 pricePerShare = 0;
        string memory version = "0.00";
        bool vaultHasShares = totalSupply != 0;
        if (vaultHasShares) {
            pricePerShare = vault.pricePerShare();
        }

        AssetMetadata memory metadata =
            AssetMetadata({
                controller: vaultAddress,
                totalAssets: totalAssets,
                totalSupply: totalSupply,
                pricePerShare: pricePerShare
            });
        Asset memory asset =
            Asset({
                name: vaultName,
                id: vaultAddress,
                version: version,
                metadata: metadata
            });
        return asset;
    }

    function getAssets() external view returns (Asset[] memory) {
        address[] memory vaultAddresses = getAssetsAddresses();
        uint256 numberOfVaults = vaultAddresses.length;
        Asset[] memory assets = new Asset[](numberOfVaults);
        for (uint256 i = 0; i < numberOfVaults; i++) {
            address vaultAddress = vaultAddresses[i];
            Asset memory asset = getAsset(vaultAddress);
            assets[i] = asset;
        }
        return assets;
    }

    function getPositionsForVault(address accountAddress, address vaultAddress)
        public
        view
        returns (Position memory)
    {
        V2Vault vault = V2Vault(vaultAddress);
        address tokenAddress = vault.token();
        IERC20 token = IERC20(tokenAddress);
        uint256 depositedBalance = vault.balanceOf(accountAddress);
        uint256 tokenBalance = token.balanceOf(accountAddress);
        uint256 tokenAllowance = token.allowance(accountAddress, vaultAddress);
        Position memory position =
            Position({
                assetId: vaultAddress,
                depositedBalance: depositedBalance,
                tokenBalance: tokenBalance,
                tokenAllowance: tokenAllowance
            });
        return position;
    }

    function getPositionsOf(address accountAddress)
        external
        view
        returns (Position[] memory)
    {
        address[] memory vaultAddresses = getAssetsAddresses();
        uint256 numberOfVaults = vaultAddresses.length;
        Position[] memory positions = new Position[](numberOfVaults);
        for (uint256 i = 0; i < numberOfVaults; i++) {
            address vaultAddress = vaultAddresses[i];
            Position memory position =
                getPositionsForVault(accountAddress, vaultAddress);

            positions[i] = position;
        }
        return positions;
    }
}
