// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface IGenericRegistry {
  function assets() external view returns (address[] memory);
}
