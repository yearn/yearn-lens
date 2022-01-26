// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity 0.8.11;
import "../../Utilities/AddressesProviderConsumer.sol";

interface IFixedForexRegistry {
    function cy(address) external view returns (address);

    function price(address) external view returns (uint256);
}

contract CalculationsFixedForex is AddressesProviderConsumer {
    constructor(address _addressesProviderAddress)
        AddressesProviderConsumer(_addressesProviderAddress)
    {}

    function isFixedForex(address tokenAddress) public view returns (bool) {
        try fixedForexRegistry().cy(tokenAddress) {
            return true;
        } catch {
            return false;
        }
    }

    function fixedForexRegistry() public view returns (IFixedForexRegistry) {
        return IFixedForexRegistry(addressById("FIXED_FOREX_REGISTRY"));
    }

    function getPriceUsdc(address tokenAddress) public view returns (uint256) {
        bool _isFixedForex = isFixedForex(tokenAddress);
        require(_isFixedForex);
        return fixedForexRegistry().price(tokenAddress) / 10**12;
    }
}
