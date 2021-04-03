// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.2;

import "../Manageable.sol";

contract Helper is Manageable {
    address[] private _helpers;

    constructor(address _managementListAddress)
        Manageable(_managementListAddress)
    {}

    function setHelpers(address[] memory helperAddresses)
        external
        onlyManagers
    {
        _helpers = helperAddresses;
    }

    function helpers() external view returns (address[] memory) {
        return (_helpers);
    }

    fallback() external {
        for (uint256 i = 0; i < _helpers.length; i++) {
            address helper = _helpers[i];
            assembly {
                calldatacopy(0, 0, calldatasize())
                let success := staticcall(
                    gas(),
                    helper,
                    0,
                    calldatasize(),
                    0,
                    0
                )
                returndatacopy(0, 0, returndatasize())
                if success {
                    return(0, returndatasize())
                }
            }
        }
        revert("Helper: Fallback proxy failed to return data");
    }
}
