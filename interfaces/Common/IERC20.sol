// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

interface IERC20 {
    function decimals() external view returns (uint8);

    function symbol() external view returns (string memory);

    function name() external view returns (string memory);

    function approve(address spender, uint256 amount) external;

    function balanceOf(address account) external view returns (uint256);

    function allowance(address spender, address owner)
        external
        view
        returns (uint256);
}
