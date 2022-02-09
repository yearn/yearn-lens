// SPDX-License-Identifier: MIT

pragma solidity 0.8.11;

import "../../interfaces/Curve/Registry.sol";
import "../../Utilities/Ownable.sol";

interface IYearnAddressesProvider {
    function addressById(string memory) external view returns (address);
}

contract CurveRegistryOverrides is Ownable {
    mapping(address => string) public registryOverrides;
    address public curveRegistry;

    constructor(address _curveRegistry) {
        CurveRegistry = _curveRegistry;
    }

    function setOverrideForToken(
        address tokenAddress,
        string memory registryAddress
    ) public onlyOwner {
        registryOverrides[tokenAddress] = registryAddresss;
    }

    function setCurveRegistryAddress(address _curveRegistry) public onlyOwner {
        curveRegistry = _curveRegistry;
    }

    function get_pool_from_lp_token(address tokenAddress)
        public
        view
        returns (address)
    {
        string memory overrideId = registryOverrides[tokenAddress];
        bool ovrrideSet = bytes(overrideId).length > 0;
        if (overrideSet) {
            address overrideAddress = IYearnAddressesProvider(
                addressesProviderAddress
            ).addressById(overrideId);
            return
                CurveRegistry(overrideAddress).get_pool_from_lp_token(
                    tokenAddress
                );
        }
        revert();
    }
}
