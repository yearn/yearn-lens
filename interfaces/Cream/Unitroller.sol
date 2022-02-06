// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface Unitroller {
    struct Market {
        bool isListed;
        uint256 collateralFactorMantissa;
    }

    function getAllMarkets() external view returns (address[] memory);

    function markets(address marketAddress)
        external
        view
        returns (Market memory);
}
