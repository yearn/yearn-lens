// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface PriceFactory {
    function getAssets() external view returns (address[] memory);
}
