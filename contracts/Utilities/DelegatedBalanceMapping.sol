// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.2;

import "../Utilities/Ownable.sol";

contract DelegatedBalanceMapping is Ownable {
  mapping(address => bool) public assetBalanceIsDelegated;

  event DelegatedBalanceMappingUpdated(
    address assetAddress,
    bool delegationEnabled
  );

  function updateDelegationStatusForAsset(
    address tokenAddress,
    bool delegationEnabled
  ) public onlyOwner {
    assetBalanceIsDelegated[tokenAddress] = delegationEnabled;
    emit DelegatedBalanceMappingUpdated(tokenAddress, delegationEnabled);
  }
}
