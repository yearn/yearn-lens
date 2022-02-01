// SPDX-License-Identifier: MIT

pragma solidity >=0.8.2;

interface IHelper {
  // Addresses merge helper
  function mergeAddresses(address[][] memory addressesSets)
    external
    view
    returns (address[] memory);

  // Strategies helper
  function assetStrategiesDelegatedBalance(address)
    external
    view
    returns (uint256);

  function assetsStrategiesDelegatedBalance() external view returns (uint256);

  function assetStrategiesLength(address) external view returns (uint256);

  function assetsStrategiesLength() external view returns (uint256);

  // Allowances helper
  struct Allowance {
    address owner;
    address spender;
    uint256 amount;
    address token;
  }

  function allowances(
    address ownerAddress,
    address[] memory tokensAddresses,
    address[] memory spenderAddresses
  ) external view returns (Allowance[] memory);
}
