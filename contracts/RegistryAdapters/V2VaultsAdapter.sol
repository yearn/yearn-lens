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
    function assetsStatic(address[] memory _assetsAddresses)
        public
        view
        returns (AssetStatic[] memory)
    {
        uint256 numberOfAssets = _assetsAddresses.length;
        AssetStatic[] memory _assets = new AssetStatic[](numberOfAssets);
        for (uint256 assetIdx = 0; assetIdx < numberOfAssets; assetIdx++) {
            address assetAddress = _assetsAddresses[assetIdx];
            AssetStatic memory _asset = assetStatic(assetAddress);
            _assets[assetIdx] = _asset;
        }
        return _assets;
    }

    function assetsDynamic(address[] memory _assetsAddresses)
        public
        view
        returns (AssetDynamic[] memory)
    {
        uint256 numberOfAssets = _assetsAddresses.length;
        AssetDynamic[] memory _assets = new AssetDynamic[](numberOfAssets);
        for (uint256 assetIdx = 0; assetIdx < numberOfAssets; assetIdx++) {
            address assetAddress = _assetsAddresses[assetIdx];
            AssetDynamic memory _asset = assetDynamic(assetAddress);
            _assets[assetIdx] = _asset;
        }
        return _assets;
    }

    function assetsStatic() external view returns (AssetStatic[] memory) {
        address[] memory _assetsAddresses = assetsAddresses();
        return assetsStatic(_assetsAddresses);
    }

    function assetsDynamic() external view returns (AssetDynamic[] memory) {
        address[] memory _assetsAddresses = assetsAddresses();
        return assetsDynamic(_assetsAddresses);
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

    struct AssetDynamic {
        address assetId;
        address tokenId;
        TokenAmount underlyingTokenBalance; // Amount of underlying token in the asset
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
        return numVaults - numberOfDeprecatedAssets;
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
                if (assetDeprecated[currentVaultAddress] == false) {
                    vaultAddresses[currentVaultIdx] = currentVaultAddress;
                    currentVaultIdx++;
                }
            }
        }
        return vaultAddresses;
    }

    function assetStatic(address assetAddress)
        public
        view
        returns (AssetStatic memory)
    {
        V2Vault vault = V2Vault(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        return
            AssetStatic({
                id: assetAddress,
                typeId: adapterInfo().typeId,
                name: vault.name(),
                version: vault.apiVersion(),
                token: tokenMetadata(tokenAddress)
            });
    }

    function assetDynamic(address assetAddress)
        public
        view
        returns (AssetDynamic memory)
    {
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

        TokenAmount memory underlyingTokenBalance =
            TokenAmount({
                amount: assetBalance(assetAddress),
                amountUsdc: assetTvl(assetAddress)
            });

        return
            AssetDynamic({
                assetId: assetAddress,
                tokenId: tokenAddress,
                metadata: metadata,
                underlyingTokenBalance: underlyingTokenBalance
            });
    }

    function assetBalance(address assetAddress) public view returns (uint256) {
        V2Vault vault = V2Vault(assetAddress);
        return vault.totalAssets();
    }

    function assetTvl(address assetAddress) public view returns (uint256) {
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
        V2Vault _asset = V2Vault(assetAddress);
        uint8 assetDecimals = _asset.decimals();
        address tokenAddress = underlyingTokenAddress(assetAddress);
        IERC20 token = IERC20(tokenAddress);
        uint256 balance = _asset.balanceOf(accountAddress);
        uint256 _accountTokenBalance =
            (balance * _asset.pricePerShare()) / 10**assetDecimals;
        uint256 _underlyingTokenBalance = token.balanceOf(accountAddress);

        return
            Position({
                assetId: assetAddress,
                tokenId: tokenAddress,
                typeId: "deposit",
                balance: balance,
                underlyingTokenBalance: TokenAmount({
                    amount: _underlyingTokenBalance,
                    amountUsdc: oracle.getNormalizedValueUsdc(
                        tokenAddress,
                        _underlyingTokenBalance
                    )
                }),
                accountTokenBalance: TokenAmount({
                    amount: _accountTokenBalance,
                    amountUsdc: oracle.getNormalizedValueUsdc(
                        tokenAddress,
                        _accountTokenBalance
                    )
                }),
                tokenAllowances: tokenAllowances(
                    accountAddress,
                    tokenAddress,
                    assetAddress
                ),
                assetAllowances: assetAllowances(accountAddress, assetAddress)
            });
    }

    // function tokens() public view returns (Token[] memory) {
    //     IV2Registry registry = IV2Registry(registryAddress);
    //     uint256 numTokens = registry.numTokens();
    //     Token[] memory _tokens = new Token[](numTokens);
    //     for (uint256 tokenIdx = 0; tokenIdx < numTokens; tokenIdx++) {
    //         address tokenAddress = registry.tokens(tokenIdx);
    //         Token memory _token = tokenMetadata(tokenAddress);
    //         _tokens[tokenIdx] = _token;
    //     }
    //     return _tokens;
    // }
}
