// SPDX-License-Identifier: MIT

pragma solidity <0.8.0;

import "../../Utilities/Ownable.sol";
import {OracleLibrary} from "@uniswap/v3-periphery/contracts/libraries/OracleLibrary.sol";

interface IERC20 {
    function decimals() external view returns (uint8);
}

interface IUniswapV3Factory {
    function getPool(
        address tokenA,
        address tokenB,
        uint24 fee
    ) external view returns (address pool);
}

contract CalculationsUniswapV3 is Ownable {
    address public uniswapV3FactoryAddress;
    address public usdcAddress;
    uint24[] public fees = [500, 3000, 10000];
    uint32 public period = 10; // seconds

    IUniswapV3Factory private uniswapV3Factory;

    constructor(address _uniswapV3FactoryAddress, address _usdcAddress) {
        uniswapV3FactoryAddress = _uniswapV3FactoryAddress;
        usdcAddress = _usdcAddress;
        uniswapV3Factory = IUniswapV3Factory(_uniswapV3FactoryAddress);
    }

    function setPeriod(uint32 _period) external onlyOwner {
        require(_period > 0, "Period should be greater than zero");
        period = _period;
    }

    // adjust fee if new fee is added by uniswap governance
    function setFees(uint24[] calldata _fees) external onlyOwner {
        require(_fees.length > 0, "Should provide at least one fee");
        fees = _fees;
    }

    function getPriceUsdc(address tokenAddress) public view returns (uint256) {
        // attempt to find the first pool that can provide a price
        for (uint256 i = 0; i < fees.length; i++) {
            address pool = uniswapV3Factory.getPool(
                tokenAddress,
                usdcAddress,
                fees[i]
            );
            if (pool == address(0)) continue;
            IERC20 tokenIn = IERC20(tokenAddress);
            uint256 amountIn = 10**tokenIn.decimals();
            return
                getAmountOut(
                    pool,
                    tokenAddress,
                    toUint128(amountIn),
                    usdcAddress
                );
        }
        revert();
    }

    function getAmountOut(
        address _pair, // uniswapv3 pool
        address _tokenIn,
        uint128 _amountIn,
        address _tokenOut
    ) public view returns (uint256 _amountOut) {
        (int24 twapTick, ) = OracleLibrary.consult(_pair, period);
        return
            OracleLibrary.getQuoteAtTick(
                twapTick,
                _amountIn,
                _tokenIn,
                _tokenOut
            );
    }

    // revert if overflow
    function toUint128(uint256 y) internal pure returns (uint128 z) {
        require((z = uint128(y)) == y);
    }
}
