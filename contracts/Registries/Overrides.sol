// SPDX-License-Identifier: MIT

pragma solidity 0.8.11;

import "../Utilities/Ownable.sol";

interface ICurveRegistry {
    function get_pool_from_lp_token(address) external view returns (address);
}

interface ICurveAddressesProvider {
    function max_id() external view returns (uint256);

    function get_address(uint256) external view returns (address);
}

contract CurveRegistryOverrides is Ownable {
    ICurveAddressesProvider public curveAddressesProvider;
    mapping(address => address) public poolByLpOverride;

    constructor(address _curveAddressesProviderAddress) {
        require(
            _curveAddressesProviderAddress != address(0),
            "Missing Curve Addresses Provider address"
        );
        curveAddressesProvider = ICurveAddressesProvider(
            _curveAddressesProviderAddress
        );
    }

    /// @notice Returns all curve registries
    /// @dev only the 0th and 5th registries have LP --> pool mappings
    function curveRegistriesList() public view returns (address[] memory) {
        uint256 numCurveRegistries = curveAddressesProvider.max_id() + 1;
        address[] memory _registries = new address[](numCurveRegistries);
        for (uint256 i; i < numCurveRegistries; i++) {
            _registries[i] = curveAddressesProvider.get_address(i);
        }
        return _registries;
    }

    /// @notice Helper function to return registries from the provider
    function getCurveRegistry(uint256 _idx)
        public
        view
        returns (ICurveRegistry)
    {
        return ICurveRegistry(curveAddressesProvider.get_address(_idx));
    }

    /// @notice Adds an override pool address for an LP
    /// @dev Maintains an additional pool address list for indexing
    function setPoolForLp(address _poolAddress, address _lpAddress)
        public
        onlyOwner
    {
        poolByLpOverride[_lpAddress] = _poolAddress;
    }

    /// @notice Search through pool registry overrides and curve registries for a LP Pool
    /// @dev the 0th and 5th curve registry addresses contain LP -> pool mappings
    function poolByLp(address _lpAddress) public view returns (address) {
        address pool = poolByLpOverride[_lpAddress];
        if (pool != address(0)) {
            return pool;
        }
        // check 1st pool from registry provider
        pool = getCurveRegistry(0).get_pool_from_lp_token(_lpAddress);
        if (pool != address(0)) {
            return pool;
        }
        // check 6th pool from registry provider
        pool = getCurveRegistry(5).get_pool_from_lp_token(_lpAddress);
        if (pool != address(0)) {
            return pool;
        }
        revert("Pool not found");
    }
}
