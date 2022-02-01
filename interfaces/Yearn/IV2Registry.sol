// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface IV2Registry {
    function numTokens() external view returns (uint256);

    function numVaults(address token) external view returns (uint256);

    function tokens(uint256 tokenIdx) external view returns (address);

    function latestVault(address token) external view returns (address);

    function vaults(address token, uint256 tokenIdx)
        external
        view
        returns (address);
}
