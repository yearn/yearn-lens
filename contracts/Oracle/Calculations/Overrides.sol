// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

import "../../Utilities/Ownable.sol";

interface ICalculations {
    function getPriceUsdc(address tokenAddress)
        external
        view
        returns (uint256);
}

interface IYearnAddressesProvider {
    function addressById(string memory) external view returns (address);
}

contract CalculationsOverrides is Ownable {
    mapping(address => string) public calculationOverrides;
    address public addressesProviderAddress;

    constructor(address _addressesProviderAddress) {
        addressesProviderAddress = _addressesProviderAddress;
    }

    function setOverrideForToken(address tokenAddress, string memory addressesProviderId) public onlyOwner {
        calculationOverrides[tokenAddress] = addressesProviderId;
    }

    function setAddressesProviderAddress(address _addressesProviderAddress) public onlyOwner {
        addressesProviderAddress = _addressesProviderAddress;
    }

    function getPriceUsdc(address tokenAddress) public view returns (uint256) {
        string memory overrideId = calculationOverrides[tokenAddress];
        bool overrideSet = bytes(overrideId).length > 0;
        if (overrideSet) {
            address overrideAddress = IYearnAddressesProvider(addressesProviderAddress).addressById(overrideId);
            return ICalculations(overrideAddress).getPriceUsdc(tokenAddress);
        }
        revert();
    }
}
