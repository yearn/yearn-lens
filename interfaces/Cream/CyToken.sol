// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface CyToken {
    function underlying() external view returns (address);

    function name() external view returns (string memory);

    function symbol() external view returns (string memory);

    function supplyRatePerBlock() external view returns (uint256);

    function borrowRatePerBlock() external view returns (uint256);

    function exchangeRateStored() external view returns (uint256);

    function reserveFactorMantissa() external view returns (uint256);

    function getCash() external view returns (uint256);

    function totalBorrows() external view returns (uint256);

    function borrowBalanceStored(address accountAddress)
        external
        view
        returns (uint256);

    function totalReserves() external view returns (uint256);

    function balanceOf(address accountAddress) external view returns (uint256);

    function decimals() external view returns (uint8);
}
