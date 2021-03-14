// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

import "../../interfaces/Sushiswap/Factory.sol";
import "../../interfaces/Sushiswap/Router.sol";
import "../../interfaces/Common/IERC20.sol";
import "../../interfaces/Curve/Registry.sol";

contract Oracle {
    address public primaryRouterAddress;
    address public secondaryRouterAddress;
    // address public primaryFactoryAddress;
    // address public secondaryFactoryAddress;
    address public curveRegistryAddress;
    address public usdcAddress;
    address public wethAddress;

    PriceRouter primaryRouter;
    PriceRouter secondaryRouter;

    // Factories
    // address secondaryFactoryAddress =
    //     0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac;
    // address primaryFactoryAddress = 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f;
    // PriceFactory primaryFactory = PriceFactory(primaryFactoryAddress);
    // PriceFactory secondaryFactory = PriceFactory(secondaryFactoryAddress);

    // Constants
    address ethAddress = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;
    address nullAddress = 0x0000000000000000000000000000000000000000;

    constructor(
        address _primaryRouterAddress,
        address _secondaryRouterAddress,
        // address _primaryFactoryAddress,
        // address _secondaryFactoryAddress,
        address _curveRegistryAddress,
        address _usdcAddress
    ) {
        primaryRouterAddress = _primaryRouterAddress;
        secondaryRouterAddress = _secondaryRouterAddress;
        curveRegistryAddress = _curveRegistryAddress;
        usdcAddress = _usdcAddress;
        primaryRouter = PriceRouter(primaryRouterAddress);
        secondaryRouter = PriceRouter(secondaryRouterAddress);
        wethAddress = primaryRouter.WETH();
    }

    function getPriceFromRouter(address token0Address, address token1Address)
        public
        view
        returns (uint256)
    {
        // Convert ETH address (0xEeee...) to WETH
        if (token0Address == ethAddress) {
            token0Address = wethAddress;
        }
        if (token1Address == ethAddress) {
            token1Address = wethAddress;
        }

        address[] memory path;
        if (token0Address == wethAddress || token1Address == wethAddress) {
            // If WETH is already in the path, create a simple path ...
            path = new address[](2);
            path[0] = token0Address;
            path[1] = token1Address;
        } else {
            // ... otherwise add WETH in the middle of the path.
            path = new address[](3);
            path[0] = token0Address;
            path[1] = wethAddress;
            path[2] = token1Address;
        }

        IERC20 token0 = IERC20(token0Address);
        uint256 amountIn = 10**uint256(token0.decimals());
        uint256[] memory amountsOut;

        bool fallbackRouterExists = secondaryRouterAddress != nullAddress;
        if (fallbackRouterExists) {
            try primaryRouter.getAmountsOut(amountIn, path) returns (
                uint256[] memory _amountsOut
            ) {
                amountsOut = _amountsOut;
            } catch {
                amountsOut = secondaryRouter.getAmountsOut(amountIn, path);
            }
        } else {
            amountsOut = primaryRouter.getAmountsOut(amountIn, path);
        }

        uint256 amountOut = amountsOut[amountsOut.length - 1];
        return amountOut;
    }

    function getPriceFromRouterUsdc(address tokenAddress)
        public
        view
        returns (uint256)
    {
        return getPriceFromRouter(tokenAddress, usdcAddress);
    }

    function getPriceUsdc(address tokenAddress) public view returns (uint256) {
        bool useCurveCalculation = isCurveLpToken(tokenAddress);
        if (useCurveCalculation) {
            return getCurvePriceUsdc(tokenAddress);
        }
        return getPriceFromRouterUsdc(tokenAddress);
    }

    // Curve
    CurveRegistry curveRegistry = CurveRegistry(curveRegistryAddress);

    function getCurvePriceUsdc(address curveLpTokenAddress)
        public
        view
        returns (uint256)
    {
        uint256 basePrice = getBasePrice(curveLpTokenAddress);
        uint256 virtualPrice = getVirtualPrice(curveLpTokenAddress);
        IERC20 usdc = IERC20(usdcAddress);
        uint256 decimals = usdc.decimals();
        uint256 decimalsAdjustment = 18 - decimals;
        uint256 price =
            (virtualPrice * basePrice * (10**decimalsAdjustment)) /
                10**(decimalsAdjustment + 18);
        return price;
    }

    function getBasePrice(address curveLpTokenAddress)
        public
        view
        returns (uint256)
    {
        address poolAddress =
            curveRegistry.get_pool_from_lp_token(curveLpTokenAddress);
        address firstUnderlyingCoin =
            getFirstUnderlyingCoinFromPool(poolAddress);
        uint256 basePrice = getPriceFromRouterUsdc(firstUnderlyingCoin);
        return basePrice;
    }

    function getVirtualPrice(address curveLpTokenAddress)
        public
        view
        returns (uint256)
    {
        return
            curveRegistry.get_virtual_price_from_lp_token(curveLpTokenAddress);
    }

    function isCurveLpToken(address tokenAddress) public view returns (bool) {
        address poolAddress =
            curveRegistry.get_pool_from_lp_token(tokenAddress);
        bool tokenHasCurvePool = poolAddress != nullAddress;
        return tokenHasCurvePool;
    }

    function getFirstUnderlyingCoinFromPool(address poolAddress)
        public
        view
        returns (address)
    {
        address[8] memory coins =
            curveRegistry.get_underlying_coins(poolAddress);
        address firstCoin = coins[0];
        return firstCoin;
    }
}
