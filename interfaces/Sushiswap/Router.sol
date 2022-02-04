// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface PriceRouter {
    function getAmountsOut(uint256 amountIn, address[] calldata path)
        external
        view
        returns (uint256[] memory amounts);

    function WETH() external view returns (address);
}
