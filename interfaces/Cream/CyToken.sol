// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface CyToken {
    function underlying() external view returns (address);

    function exchangeRateStored() external view returns (uint256);

    function decimals() external view returns (uint8);
}
