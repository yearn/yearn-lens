// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

// Adapter-specific imports
import "../../interfaces/Yearn/V1Vault.sol";
import "../../interfaces/Yearn/V1Registry.sol";

// Common imports
import "../../interfaces/Common/IERC20.sol";
import "../Common/Adapter.sol";

contract RegisteryAdapterV1Vault is Adapter {
    /**
     * Common code shared by all adapters
     */
    function assets(address[] memory _assetsAddresses)
        public
        view
        returns (Asset[] memory)
    {
        uint256 numberOfAssets = _assetsAddresses.length;
        Asset[] memory _assets = new Asset[](numberOfAssets);
        for (uint256 assetIdx = 0; assetIdx < numberOfAssets; assetIdx++) {
            address assetAddress = _assetsAddresses[assetIdx];
            Asset memory _asset = asset(assetAddress);
            _assets[assetIdx] = _asset;
        }
        return _assets;
    }

    function assets() external view returns (Asset[] memory) {
        address[] memory _assetsAddresses = assetsAddresses();
        return assets(_assetsAddresses);
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
     * Common code shared by v1 vaults, v2 vaults and earn
     */
    function positionsOf(
        address accountAddress,
        address[] memory _assetsAddresses
    ) public view returns (Position[] memory) {
        uint256 numberOfAssets = _assetsAddresses.length;
        Position[] memory positions = new Position[](numberOfAssets);
        for (uint256 assetIdx = 0; assetIdx < numberOfAssets; assetIdx++) {
            address assetAddress = _assetsAddresses[assetIdx];
            Position memory position = positionOf(accountAddress, assetAddress);
            positions[assetIdx] = position;
        }
        return positions;
    }

    function positionsOf(address accountAddress)
        external
        view
        returns (Position[] memory)
    {
        address[] memory _assetsAddresses = assetsAddresses();
        return positionsOf(accountAddress, _assetsAddresses);
    }

    /**
     * V1 Vaults Adapter
     */
    function adapterInfo() public view returns (AdapterInfo memory) {
        return
            AdapterInfo({
                id: address(this),
                typeId: "v1Vault",
                categoryId: "vault"
            });
    }

    struct AssetMetadata {
        string symbol;
        uint256 pricePerShare;
        bool migrationAvailable;
        address latestVaultAddress;
        uint256 totalSupply;
    }

    function underlyingTokenAddress(address assetAddress)
        public
        view
        returns (address)
    {
        V1Vault vault = V1Vault(assetAddress);
        address tokenAddress = vault.token();
        return tokenAddress;
    }

    function assetsLength() public view returns (uint256) {
        return V1Registry(registryAddress).getVaultsLength();
    }

    function assetsAddresses() public view returns (address[] memory) {
        return V1Registry(registryAddress).getVaults();
    }

    function asset(address assetAddress) public view returns (Asset memory) {
        V1Vault vault = V1Vault(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        string memory name = vault.name();
        uint256 totalAssets = vault.balance();
        uint256 totalSupply = vault.totalSupply();
        string memory version = "1.0.0";
        uint256 pricePerShare = 0;
        bool vaultHasShares = totalSupply != 0;
        if (vaultHasShares) {
            pricePerShare = vault.getPricePerFullShare();
        }

        // address latestVaultAddress = registry.latestVault(tokenAddress);
        // bool migrationAvailable = latestVaultAddress != assetAddress;

        AssetMetadata memory metadata =
            AssetMetadata({
                symbol: vault.symbol(),
                pricePerShare: pricePerShare,
                migrationAvailable: false,
                latestVaultAddress: address(0),
                totalSupply: totalSupply
            });
        return
            Asset({
                id: assetAddress,
                typeId: adapterInfo().typeId,
                name: vault.name(),
                version: version,
                balance: assetBalance(assetAddress),
                balanceUsdc: assetTvl(assetAddress),
                token: tokenMetadata(tokenAddress),
                metadata: metadata
            });
    }

    function assetBalance(address assetAddress) public view returns (uint256) {
        V1Vault vault = V1Vault(assetAddress);
        return vault.balance();
    }

    function assetTvl(address assetAddress) public view returns (uint256) {
        V1Vault vault = V1Vault(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        uint256 amount = assetBalance(assetAddress);
        uint256 tvl = oracle.getNormalizedValueUsdc(tokenAddress, amount);
        return tvl;
    }

    function positionOf(address accountAddress, address assetAddress)
        public
        view
        returns (Position memory)
    {
        V1Vault _asset = V1Vault(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        IERC20 token = IERC20(tokenAddress);
        uint256 balance =
            (_asset.balanceOf(accountAddress) * _asset.getPricePerFullShare()) /
                10**18;
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
                typeId: "deposit",
                balance: balance,
                balanceUsdc: balanceUsdc,
                tokenPosition: tokenPosition,
                allowances: _positionAllowances
            });
        return position;
    }
}
