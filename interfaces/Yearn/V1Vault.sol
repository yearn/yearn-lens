// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface IV1Vault {
    function token() external view returns (address);

    function underlying() external view returns (address);

    function name() external view returns (string memory);

    function symbol() external view returns (string memory);

    function decimals() external view returns (uint8);

    function controller() external view returns (address);

    function governance() external view returns (address);

    function getPricePerFullShare() external view returns (uint256);

    function balance() external view returns (uint256);

    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function deposit(uint256 amount) external;

    function approve(address spender, uint256 amount) external;

    function allowance(address spender, address owner)
        external
        view
        returns (uint256);
}
