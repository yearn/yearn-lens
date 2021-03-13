// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

import "../../interfaces/Sushiswap/Factory.sol";
import "../../interfaces/Sushiswap/Router.sol";
import "../../interfaces/Common/IERC20.sol";
import "../../interfaces/Curve/Registry.sol";

contract Oracle {
    // Factories
    address sushiswapFactoryAddress =
        0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac;
    address uniswapFactoryAddress = 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f;

    PriceFactory sushiswapFactory = PriceFactory(sushiswapFactoryAddress);
    PriceFactory uniswapFactory = PriceFactory(uniswapFactoryAddress);

    // Routers
    address sushiswapRouterAddress = 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F;
    address uniswapRouterAddress = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    PriceRouter sushiswapRouter = PriceRouter(sushiswapRouterAddress);
    PriceRouter uniswapRouter = PriceRouter(uniswapRouterAddress);

    // Constants
    address USDCAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address WETHAddress = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address ETHAddress = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    function getPriceFromRouter(address token0Address, address token1Address)
        public
        view
        returns (uint256)
    {
        // Convert ETH address (0xEeee...) to WETH
        if (token0Address == ETHAddress) {
            token0Address = WETHAddress;
        }
        if (token1Address == ETHAddress) {
            token1Address = WETHAddress;
        }

        address[] memory path;
        if (token0Address == WETHAddress || token1Address == WETHAddress) {
            // If WETH is already in the path, create a simple path ...
            path = new address[](2);
            path[0] = token0Address;
            path[1] = token1Address;
        } else {
            // ... otherwise add WETH in the middle of the path.
            path = new address[](3);
            path[0] = token0Address;
            path[1] = WETHAddress;
            path[2] = token1Address;
        }

        IERC20 token0 = IERC20(token0Address);
        uint256 amountIn = 10**uint256(token0.decimals());
        uint256[] memory amountsOut;

        try uniswapRouter.getAmountsOut(amountIn, path) returns (
            uint256[] memory _amountsOut
        ) {
            amountsOut = _amountsOut;
        } catch {
            amountsOut = sushiswapRouter.getAmountsOut(amountIn, path);
        }

        uint256 amountOut = amountsOut[amountsOut.length - 1];
        return amountOut;
    }

    function getPriceFromRouterUsdc(address tokenAddress)
        public
        view
        returns (uint256)
    {
        return getPriceFromRouter(tokenAddress, USDCAddress);
    }

    function getPriceUsdc(address tokenAddress) public view returns (uint256) {
        bool useCurveCalculation = isCurveLpToken(tokenAddress);
        if (useCurveCalculation) {
            return getCurvePriceUsdc(tokenAddress);
        }
        return getPriceFromRouterUsdc(tokenAddress);
    }

    // Curve
    address CurveRegistryAddress = 0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c;
    address NULLAddress = 0x0000000000000000000000000000000000000000;
    CurveRegistry curveRegistry = CurveRegistry(CurveRegistryAddress);

    function getCurvePriceUsdc(address curveLpTokenAddress)
        public
        view
        returns (uint256)
    {
        uint256 basePrice = getBasePrice(curveLpTokenAddress);
        uint256 virtualPrice = getVirtualPrice(curveLpTokenAddress);
        IERC20 usdc = IERC20(USDCAddress);
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
        bool tokenHasCurvePool = poolAddress != NULLAddress;
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
