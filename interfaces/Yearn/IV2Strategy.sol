// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface IV2Strategy {
    function name() external view returns (string memory);

    function apiVersion() external view returns (string memory);

    function strategist() external view returns (address);

    function rewards() external view returns (address);

    function vault() external view returns (address);

    function keeper() external view returns (address);

    function want() external view returns (address);

    function emergencyExit() external view returns (bool);

    function isActive() external view returns (bool);

    function delegatedAssets() external view returns (uint256);

    function estimatedTotalAssets() external view returns (uint256);
}
