// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

interface Oracle {
    function getPriceUsdc(address tokenAddress) external view returns (uint256);
}
