// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface CyToken {
    function underlying() external view returns (address);

    function name() external view returns (string memory);

    function exchangeRateStored() external view returns (uint256);

    function getCash() external view returns (uint256);

    function totalBorrows() external view returns (uint256);

    function totalReserves() external view returns (uint256);

    function balanceOf() external view returns (uint256);

    function borrowBalanceStored() external view returns (uint256);

    function decimals() external view returns (uint8);
}
