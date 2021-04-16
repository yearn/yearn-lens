// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.2;

import "../Utilities/Manageable.sol";

contract DelegatedBalanceMapping is Manageable {
    mapping(address => bool) public assetBalanceIsDelegated;

    event DelegatedBalanceMappingUpdated(
        address assetAddress,
        bool delegationEnabled
    );

    constructor(address _managementListAddress)
        Manageable(_managementListAddress)
    {}

    function updateDelegationStatusForAsset(
        address tokenAddress,
        bool delegationEnabled
    ) public onlyManagers {
        assetBalanceIsDelegated[tokenAddress] = delegationEnabled;
        emit DelegatedBalanceMappingUpdated(tokenAddress, delegationEnabled);
    }
}
