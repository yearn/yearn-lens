// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface V2Vault {
    function token() external view returns (address);

    function name() external view returns (string memory);

    function symbol() external view returns (string memory);

    function decimals() external view returns (uint8);

    function pricePerShare() external view returns (uint256);

    function totalAssets() external view returns (uint256);

    function apiVersion() external view returns (string memory);

    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function emergencyShutdown() external view returns (bool);

    function depositLimit() external view returns (uint256);

    function deposit(uint256 amount) external;

    function approve(address spender, uint256 amount) external;

    function allowance(address spender, address owner)
        external
        view
        returns (uint256);
}
