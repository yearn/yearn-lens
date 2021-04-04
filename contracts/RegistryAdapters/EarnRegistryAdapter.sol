// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

// Adapter-specific imports
import "../../interfaces/Yearn/IEarnToken.sol";
import "../../interfaces/Yearn/IGenericRegistry.sol";

// Common imports
import "../../interfaces/Common/IERC20.sol";
import "../../interfaces/Common/IOracle.sol";
import "../Common/Adapter.sol";

contract RegistryAdapterEarn is Adapter {
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
     * Earn Adapter
     */
    function adapterInfo() public view returns (AdapterInfo memory) {
        return
            AdapterInfo({
                id: address(this),
                typeId: "earn",
                categoryId: "deposit",
                subcategoryId: "safe"
            });
    }

    struct AssetMetadata {
        uint256 totalSupply;
        uint256 pricePerShare;
    }

    function underlyingTokenAddress(address assetAddress)
        public
        view
        returns (address)
    {
        IEarnToken earnToken = IEarnToken(assetAddress);
        address tokenAddress = earnToken.token();
        return tokenAddress;
    }

    function assetsLength() public view returns (uint256) {
        return assetsAddresses().length;
    }

    function assetsAddresses() public view returns (address[] memory) {
        return IGenericRegistry(registryAddress).assets();
    }

    function asset(address assetAddress) public view returns (Asset memory) {
        IEarnToken earnToken = IEarnToken(assetAddress);
        uint256 totalAssets = earnToken.pool();
        uint256 totalSupply = earnToken.totalSupply();
        address tokenAddress = underlyingTokenAddress(assetAddress);
        uint256 pricePerShare = 0;
        bool earnTokenHasShares = totalSupply != 0;
        if (earnTokenHasShares) {
            pricePerShare = earnToken.getPricePerFullShare();
        }
        AssetMetadata memory metadata =
            AssetMetadata({
                totalSupply: totalSupply,
                pricePerShare: pricePerShare
            });
        return
            Asset({
                id: assetAddress,
                typeId: adapterInfo().typeId,
                name: earnToken.name(),
                version: "2.0.0",
                balance: assetBalance(assetAddress),
                balanceUsdc: assetTvl(assetAddress),
                token: token(tokenAddress),
                metadata: metadata
            });
    }

    function assetBalance(address assetAddress) public view returns (uint256) {
        IEarnToken earnToken = IEarnToken(assetAddress);
        return earnToken.calcPoolValueInToken();
    }

    function assetTvl(address assetAddress) public view returns (uint256) {
        IEarnToken earnToken = IEarnToken(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        uint256 amount = earnToken.calcPoolValueInToken();
        uint256 tvl = oracle.getNormalizedValueUsdc(tokenAddress, amount);
        return tvl;
    }
}
