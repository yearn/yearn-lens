// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

// Adapter-specific imports
import "../../interfaces/Cream/Unitroller.sol";
import "../../interfaces/Cream/CyToken.sol";

// Common imports
import "../../interfaces/Common/IERC20.sol";
import "../Common/Adapter.sol";

contract RegistryAdapterIronBank is Adapter {
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
        // AssetMetadata metadata;
    }

    constructor(
        address _registryAddress,
        address _oracleAddress,
        address _managementListAddress
    ) Adapter(_registryAddress, _oracleAddress, _managementListAddress) {}

    /**
     * Iron Bank Adapter
     */
    function adapterInfo() public view returns (AdapterInfo memory) {
        return
            AdapterInfo({
                id: address(this),
                typeId: "ironBank",
                categoryId: "lending"
            });
    }

    struct AssetMetadata {
        uint256 totalSupplied;
        uint256 totalSuppliedUsdc;
        uint256 totalBorrowed;
        uint256 totalBorrowedUsdc;
        uint256 cashUsdc;
        uint256 liquidity;
        uint256 liquidityUsdc;
        uint256 supplyApyBips;
        uint256 borrowApyBips;
    }

    function underlyingTokenAddress(address assetAddress)
        public
        view
        returns (address)
    {
        CyToken cyToken = CyToken(assetAddress);
        address tokenAddress = cyToken.underlying();
        return tokenAddress;
    }

    function assetsLength() public view returns (uint256) {
        address[] memory allMarkets = getAllMarkets();
        return allMarkets.length;
    }

    function assetsAddresses() public view returns (address[] memory) {
        address[] memory allMarkets = getAllMarkets();
        return allMarkets;
    }

    function asset(address assetAddress) public view returns (Asset memory) {
        CyToken cyToken = CyToken(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        IERC20 token = IERC20(tokenAddress);
        // AssetMetadata memory metadata =
        //     AssetMetadata({
        //         symbol: vault.symbol(),
        //         pricePerShare: pricePerShare,
        //         migrationAvailable: migrationAvailable,
        //         latestVaultAddress: latestVaultAddress,
        //         depositLimit: vault.depositLimit(),
        //         emergencyShutdown: vault.emergencyShutdown()
        //     });

        Asset memory _asset =
            Asset({
                id: assetAddress,
                typeId: adapterInfo().typeId,
                name: token.name(),
                version: "2.0.0",
                balance: assetBalance(assetAddress),
                balanceUsdc: assetTvl(assetAddress),
                token: tokenMetadata(tokenAddress)
                // metadata: metadata
            });
        return _asset;
    }

    function assetBalance(address assetAddress) public view returns (uint256) {
        CyToken cyToken = CyToken(assetAddress);
        uint256 cash = cyToken.getCash();
        uint256 totalBorrows = cyToken.totalBorrows();
        uint256 totalReserves = cyToken.totalReserves();
        uint256 totalSupplied = (cash + totalBorrows - totalReserves);
        return totalSupplied;
    }

    function assetTvl(address assetAddress) public view returns (uint256) {
        CyToken cyToken = CyToken(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        IERC20 token = IERC20(tokenAddress);
        uint256 totalSupplied = assetBalance(assetAddress);
        uint256 tokenDecimals = token.decimals();
        uint256 usdcDecimals = 6;
        uint256 decimalsAdjustment;
        if (tokenDecimals >= usdcDecimals) {
            decimalsAdjustment = tokenDecimals - usdcDecimals;
        } else {
            decimalsAdjustment = usdcDecimals - tokenDecimals;
        }
        uint256 price = oracle.getPriceUsdcRecommended(tokenAddress);
        uint256 tvl;
        if (decimalsAdjustment > 0) {
            tvl =
                (totalSupplied * price * (10**decimalsAdjustment)) /
                10**(decimalsAdjustment + tokenDecimals);
        } else {
            tvl = (totalSupplied * price) / 10**usdcDecimals;
        }
        return tvl;
    }

    function positionOf(address accountAddress, address assetAddress)
        public
        view
        returns (Position memory)
    {
        IERC20 _asset = IERC20(assetAddress);
        address tokenAddress = underlyingTokenAddress(assetAddress);
        IERC20 token = IERC20(tokenAddress);
        uint256 balance = _asset.balanceOf(accountAddress);
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
                typeId: "borrow",
                balance: balance,
                balanceUsdc: balanceUsdc,
                tokenPosition: tokenPosition,
                allowances: _positionAllowances
            });
        return position;
    }

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

    function getAllMarkets() public view returns (address[] memory) {
        return Unitroller(registryAddress).getAllMarkets();
    }
}
