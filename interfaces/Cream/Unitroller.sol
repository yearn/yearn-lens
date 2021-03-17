// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface Unitroller {
    function getAllMarkets() external view returns (address[] memory);
}
