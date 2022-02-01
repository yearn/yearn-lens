// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface IEarnToken {
  function token() external view returns (address);

  function name() external view returns (string memory);

  function symbol() external view returns (string memory);

  function decimals() external view returns (uint8);

  function getPricePerFullShare() external view returns (uint256);

  function pool() external view returns (uint256);

  function totalSupply() external view returns (uint256);

  function calcPoolValueInToken() external view returns (uint256);

  function balanceOf(address account) external view returns (uint256);

  function deposit(uint256 amount) external;

  function approve(address spender, uint256 amount) external;

  function allowance(address spender, address owner)
    external
    view
    returns (uint256);
}
