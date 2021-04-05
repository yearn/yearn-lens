// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

// Adapter-specific imports
import "../../interfaces/Yearn/V2Vault.sol";
import "../../interfaces/Yearn/IV2Registry.sol";

// Common imports
import "../../interfaces/Common/IERC20.sol";
import "../Common/Adapter.sol";

contract RegisteryAdapterV2Vault is Adapter {
    /**
     * Common code shared by all adapters
     */
    function assets() external view returns (Asset[] memory) {
        address[] memory assetAddresses = assetsAddresses();
        uint256 numberOfAssets = assetAddresses.length;
        Asset[] memory _assets = new Asset[](numberOfAssets);
        for (uint256 assetIdx = 0; assetIdx < numberOfAssets; assetIdx++) {
            address assetAddress = assetAddresses[assetIdx];
            Asset memory _asset = asset(assetAddress);
            _assets[assetIdx] = _asset;
        }
        return _assets;
    }

    function assetsTvl() external view returns (uint256) {
        uint256 tvl;
        address[] memory assetAddresses = assetsAddresses();
        uint256 numberOfAssets = assetAddresses.length;
        for (uint256 assetIdx = 0; assetIdx < numberOfAssets; assetIdx++) {
            address assetAddress = assetAddresses[assetIdx];
            uint256 _assetTvl = assetTvl(assetAddress);
            tvl += _assetTvl;
        }
        return tvl;
    }

    function positionsOf(address accountAddress)
        external
        view
        returns (Position[] memory)
    {
        address[] memory _assetAddresses = assetsAddresses();
        uint256 numberOfAssets = _assetAddresses.length;
        Position[] memory positions = new Position[](numberOfAssets);
        for (uint256 assetIdx = 0; assetIdx < numberOfAssets; assetIdx++) {
            address assetAddress = _assetAddresses[assetIdx];
            Position memory position = positionOf(accountAddress, assetAddress);
            positions[assetIdx] = position;
        }
        return positions;
    }

    function positionOf(address accountAddress, address assetAddress)
        public
        view
        returns (Position memory)
    {
        IERC20 asset = IERC20(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        IERC20 token = IERC20(tokenAddress);
        uint256 balance = asset.balanceOf(accountAddress);
        uint256 balanceUsdc =
            oracle.getNormalizedValueUsdc(tokenAddress, balance);
        uint256 tokenBalance = token.balanceOf(accountAddress);
        uint256 tokenBalanceUsdc =
            oracle.getNormalizedValueUsdc(tokenAddress, tokenBalance);

        Allowance[] memory _tokenPositionAllowances =
            tokenPositionAllowances(accountAddress, tokenAddress, assetAddress);
        Allowance[] memory _positionAllowances =
            positionAllowances(accountAddress, assetAddress);

        TokenPosition memory tokenPosition =
            TokenPosition({
                tokenId: tokenAddress,
                balance: tokenBalance,
                balanceUsdc: tokenBalanceUsdc,
                allowances: _tokenPositionAllowances
            });

        Position memory position =
            Position({
                assetId: assetAddress,
                categoryId: "deposit",
                balance: balance,
                balanceUsdc: balanceUsdc,
                tokenPosition: tokenPosition,
                allowances: _positionAllowances
            });
        return position;
    }

    struct Asset {
        address id;
        string typeId;
        string name;
        string version;
        uint256 balance;
        uint256 balanceUsdc;
        Token token;
        AssetMetadata metadata;
    }

    constructor(
        address _registryAddress,
        address _oracleAddress,
        address _managementListAddress
    ) Adapter(_registryAddress, _oracleAddress, _managementListAddress) {}

    /**
     * V2 Vaults Adapter
     */
    function adapterInfo() public view returns (AdapterInfo memory) {
        return
            AdapterInfo({
                id: address(this),
                typeId: "v2Vault",
                categoryId: "vault"
            });
    }

    struct AssetMetadata {
        string symbol;
        uint256 pricePerShare;
        bool migrationAvailable;
        address latestVaultAddress;
        uint256 depositLimit;
        bool emergencyShutdown;
    }

    function underlyingTokenAddress(address assetAddress)
        public
        view
        returns (address)
    {
        V2Vault vault = V2Vault(assetAddress);
        address tokenAddress = vault.token();
        return tokenAddress;
    }

    function assetsLength() public view returns (uint256) {
        IV2Registry registry = IV2Registry(registryAddress);
        uint256 numTokens = registry.numTokens();
        uint256 numVaults;
        for (uint256 tokenIdx = 0; tokenIdx < numTokens; tokenIdx++) {
            address currentToken = registry.tokens(tokenIdx);
            uint256 numVaultsForToken = registry.numVaults(currentToken);
            numVaults += numVaultsForToken;
        }
        return numVaults;
    }

    function assetsAddresses() public view returns (address[] memory) {
        uint256 numVaults = assetsLength();
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

    function asset(address assetAddress) public view returns (Asset memory) {
        V2Vault vault = V2Vault(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        IV2Registry registry = IV2Registry(registryAddress);
        uint256 totalSupply = vault.totalSupply();
        uint256 pricePerShare = 0;
        bool vaultHasShares = totalSupply != 0;
        if (vaultHasShares) {
            pricePerShare = vault.pricePerShare();
        }

        address latestVaultAddress = registry.latestVault(tokenAddress);
        bool migrationAvailable = latestVaultAddress != assetAddress;

        AssetMetadata memory metadata =
            AssetMetadata({
                symbol: vault.symbol(),
                pricePerShare: pricePerShare,
                migrationAvailable: migrationAvailable,
                latestVaultAddress: latestVaultAddress,
                depositLimit: vault.depositLimit(),
                emergencyShutdown: vault.emergencyShutdown()
            });

        Asset memory _asset =
            Asset({
                id: assetAddress,
                typeId: adapterInfo().typeId,
                name: vault.name(),
                version: vault.apiVersion(),
                balance: assetBalance(assetAddress),
                balanceUsdc: assetTvl(assetAddress),
                token: token(tokenAddress),
                metadata: metadata
            });
        return _asset;
    }

    function assetBalance(address assetAddress) public view returns (uint256) {
        V2Vault vault = V2Vault(assetAddress);
        return vault.totalAssets();
    }

    function assetTvl(address assetAddress) public view returns (uint256) {
        V2Vault vault = V2Vault(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        uint256 amount = assetBalance(assetAddress);
        uint256 tvl = oracle.getNormalizedValueUsdc(tokenAddress, amount);
        return tvl;
    }

    // function tokens() public view returns (Token[] memory) {
    //     IV2Registry registry = IV2Registry(registryAddress);
    //     uint256 numTokens = registry.numTokens();
    //     Token[] memory _tokens = new Token[](numTokens);
    //     for (uint256 tokenIdx = 0; tokenIdx < numTokens; tokenIdx++) {
    //         address tokenAddress = registry.tokens(tokenIdx);
    //         Token memory _token = token(tokenAddress);
    //         _tokens[tokenIdx] = _token;
    //     }
    //     return _tokens;
    // }
}
