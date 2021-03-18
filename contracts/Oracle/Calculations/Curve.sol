// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

import "../../../interfaces/Common/Oracle.sol";
import "../../../interfaces/Common/IERC20.sol";
import "../../../interfaces/Curve/Registry.sol";

contract CalculationsCurve {
    address public curveRegistryAddress;
    CurveRegistry curveRegistry;
    address zeroAddress = 0x0000000000000000000000000000000000000000;

    constructor(address _curveRegistryAddress) {
        curveRegistry = CurveRegistry(_curveRegistryAddress);
    }

    function getUsdcAddressFromSender() internal view returns (address) {
        Oracle oracle = Oracle(msg.sender);
        return oracle.usdcAddress();
    }

    function getCurvePriceUsdc(address curveLpTokenAddress)
        public
        view
        returns (uint256)
    {
        uint256 basePrice = getBasePrice(curveLpTokenAddress);
        uint256 virtualPrice = getVirtualPrice(curveLpTokenAddress);
        IERC20 usdc = IERC20(getUsdcAddressFromSender());
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
        address firstUnderlyingCoinAddress =
            getFirstUnderlyingCoinFromPool(poolAddress);
        (, bytes memory data) =
            address(msg.sender).staticcall(
                abi.encodeWithSignature(
                    "getPriceFromRouterUsdc(address)",
                    firstUnderlyingCoinAddress
                )
            );
        uint256 basePrice = abi.decode(data, (uint256));
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
        bool tokenHasCurvePool = poolAddress != zeroAddress;
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

    function getPriceUsdc(address assetAddress) public view returns (uint256) {
        if (isCurveLpToken(assetAddress)) {
            return getCurvePriceUsdc(assetAddress);
        }
        revert();
    }
}
