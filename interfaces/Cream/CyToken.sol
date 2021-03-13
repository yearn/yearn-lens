// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface CyToken {
    // string public name;
    // string public symbol;
    // uint8 public decimals;
    // address public underlying;

    function supplyRatePerBlock() external view returns (uint256);

    function getCash() external view returns (uint256);

    function borrowRatePerBlock() external view returns (uint256);
}
