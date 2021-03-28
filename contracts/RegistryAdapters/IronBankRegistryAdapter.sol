// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

// Common imports
import "../../interfaces/Common/IERC20.sol";
import "../../interfaces/Common/IOracle.sol";

// Adapter-specific imports
import "../../interfaces/Cream/Unitroller.sol";
import "../../interfaces/Cream/CyToken.sol";

contract RegistryAdapterIronBank {
    /**
     * Common code shared by all adapters
     */
    address public registryAddress;
    IOracle public oracle;

    struct AdapterInfo {
        string typeId;
        string categoryId;
        string subcategoryId;
    }

    struct Position {
        address assetId;
        uint256 balance;
        uint256 balanceUsdc;
        TokenPosition tokenPosition;
    }

    struct Token {
        address id;
        string name;
        string symbol;
        uint8 decimals;
        uint256 priceUsdc;
    }

    struct TokenPosition {
        address tokenId;
        uint256 balance;
        uint256 balanceUsdc;
        Allowance[] allowances;
    }

    struct Allowance {
        address owner;
        address spender;
        uint256 allowance;
    }

    constructor(address _registryAddress, address _oracleAddress) {
        require(_registryAddress != address(0), "Missing registry address");
        require(_oracleAddress != address(0), "Missing oracle address");
        registryAddress = _registryAddress;
        oracle = IOracle(_oracleAddress);
    }

    function assets() external view returns (Asset[] memory) {
        address[] memory assetAddresses = assetsAddresses();
        uint256 numberOfAssets = assetAddresses.length;
        Asset[] memory _assets = new Asset[](numberOfAssets);
        for (uint256 i = 0; i < numberOfAssets; i++) {
            address assetAddress = assetAddresses[i];
            Asset memory _asset = asset(assetAddress);
            _assets[i] = _asset;
        }
        return _assets;
    }

    function token(address tokenAddress) internal view returns (Token memory) {
        IERC20 underlyingToken = IERC20(tokenAddress);
        Token memory _token =
            Token({
                id: tokenAddress,
                name: underlyingToken.name(),
                symbol: underlyingToken.symbol(),
                decimals: underlyingToken.decimals(),
                priceUsdc: oracle.getPriceUsdcRecommended(tokenAddress)
            });
        return _token;
    }

    function assetsTvl() external view returns (uint256) {
        uint256 tvl;
        address[] memory assetAddresses = assetsAddresses();
        uint256 numberOfAssets = assetAddresses.length;
        for (uint256 i = 0; i < numberOfAssets; i++) {
            address assetAddress = assetAddresses[i];
            uint256 _assetTvl = assetTvl(assetAddress);
            tvl += _assetTvl;
        }
        return tvl;
    }

    /**
     * Iron Bank Adapter
     */
    AdapterInfo public adapterInfo =
        AdapterInfo({
            typeId: "ironBank",
            categoryId: "deposit",
            subcategoryId: "lending"
        });

    struct Asset {
        address id;
        string name;
        string version;
        uint256 balance;
        uint256 balanceUsdc;
        Token token;
        // AssetMetadata metadata;
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

    function assetsLength() public view returns (uint256) {
        address[] memory allMarkets = getAllMarkets();
        return allMarkets.length;
    }

    function assetsAddresses() public view returns (address[] memory) {
        address[] memory allMarkets = getAllMarkets();
        return allMarkets;
    }

    function assetBalance(address assetAddress) public view returns (uint256) {
        CyToken cyToken = CyToken(assetAddress);
        address underlyingTokenAddress = cyToken.underlying();
        IERC20 underlyingToken = IERC20(underlyingTokenAddress);
        uint256 cash = cyToken.getCash();
        uint256 totalBorrows = cyToken.totalBorrows();
        uint256 totalReserves = cyToken.totalReserves();
        uint256 totalSupplied = (cash + totalBorrows - totalReserves);
        return totalSupplied;
    }

    function assetTvl(address assetAddress) public view returns (uint256) {
        CyToken cyToken = CyToken(assetAddress);
        address underlyingTokenAddress = cyToken.underlying();
        IERC20 underlyingToken = IERC20(underlyingTokenAddress);
        uint256 totalSupplied = assetBalance(assetAddress);
        uint256 underlyingDecimals = underlyingToken.decimals();
        uint256 usdcDecimals = 6;
        uint256 decimalsAdjustment;
        if (underlyingDecimals >= usdcDecimals) {
            decimalsAdjustment = underlyingDecimals - usdcDecimals;
        } else {
            decimalsAdjustment = usdcDecimals - underlyingDecimals;
        }
        uint256 price = oracle.getPriceUsdcRecommended(underlyingTokenAddress);
        uint256 tvl;
        if (decimalsAdjustment > 0) {
            tvl =
                (totalSupplied * price * (10**decimalsAdjustment)) /
                10**(decimalsAdjustment + underlyingDecimals);
        } else {
            tvl = (totalSupplied * price) / 10**usdcDecimals;
        }
        return tvl;
    }

    function asset(address assetAddress) public view returns (Asset memory) {
        CyToken cyToken = CyToken(assetAddress);
        address underlyingTokenAddress = cyToken.underlying();
        IERC20 underlyingToken = IERC20(underlyingTokenAddress);
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
                name: underlyingToken.name(),
                version: "1.0.0",
                balance: assetBalance(assetAddress),
                balanceUsdc: assetTvl(assetAddress),
                token: token(underlyingTokenAddress)
                // metadata: metadata
            });
        return _asset;
    }

    function tokens() public view returns (Token[] memory) {}

    function positionOf(address accountAddress, address vaultAddress)
        public
        view
        returns (Position memory)
    {}

    function positionsOf(address accountAddress)
        external
        view
        returns (Position[] memory)
    {}

    function getAllMarkets() public view returns (address[] memory) {
        return Unitroller(registryAddress).getAllMarkets();
    }
}
