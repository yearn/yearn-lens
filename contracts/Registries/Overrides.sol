// SPDX-License-Identifier: MIT

pragma solidity 0.8.11;

import "../../Utilities/Ownable.sol";

// TODO: Should I redefine the interface here or just add methods to
//       interfaces/Curve/Registry.sol?
interface ICurveRegistry {
    function get_pool_from_lp_token(address) external view returns (address);
}

// Do I need both Address Provider and Registry?
interface ICurveAddressesProvider {
    function get_address(uint256) external view returns (address);
}

// Update CalculationsCurve to use this contract instead of get_pool_from_lp_token
// curve registry address: 0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5
// curveAddressProviderAddress: 0x0000000022D53366457F9d5E68Ec105046FC4383
contract CurveRegistryOverrides is Ownable {
    ICurveAddressesProvider public curveAddressesProvider;
    ICurveRegistry public curveRegistry;
    mapping(address => address) public poolByLpOverride;
    address[] public poolAddresses;

    constructor(address _curveAddressesProvider, address _curveRegistryAddress)
    {
        require(
            _curveAddressesProvider != address(0),
            "Missing Curve Addresses Provider address"
        );
        require(
            _curveRegistryAddress != address(0),
            "Missing Curve Registry address"
        );
        curveAddressesProvider = ICurveAddressesProvider(
            _curveAddressesProvider
        );
        curveRegistry = ICurveRegistry(_curveRegistryAddress);
    }

    /// @notice Updates ICurveRegistry
    function addCurveRegistry(address _curveRegistryAddress) onlyOwner {
        require(
            _curveRegistryAddress != address(0),
            "Missing Curve Registry Address"
        );
        curveRegistry = ICurveRegistry(_curveRegistryAddress);
    }

    /// @notice Returns both override and curve registry pools as list
    function curveRegistriesList() public view returns (address[]) {
        address[] registries;
        for (uint256 i; i < poolAddresses.length; i++) {
            registries.push(poolAddresses[i]);
        }
        for (uint256 i; i < curveRegistry.pool_count(); i++) {
            registries.push(curveRegistry.pool_list(i));
        }
        return registries;
    }

    /// @notice Adds an override pool address for an LP
    /// @dev Maintains an additional pool address list for indexing
    function setPoolForLp(address _poolAddress, address _lpAddress)
        public
        onlyOwner
    {
        poolByLpOverride[_lpAddress] = _poolAddress;
        poolAddress.push(_poolAddress);
    }

    // poolByLp(address) - first check poolByLpOverride to see if an override exists.. return if it does.
    // if not, loop through curve registries using get_pool_from_lp_token and try to find a pool
    /// @notice Search through pool registry overrides and curve registries for a LP Pool
    function poolByLp(address _lpAddress) public view returns (address) {
        address pool = poolByLpOverride[_lpAddress];
        if (pool != address(0)) {
            return pool;
        }
        // loop through registries
        // registry address provider?
        // --> curver address provider, interface
        for (uint256 i; i < curveAddressesProvider.max_id; i++) {
            address curveRegistryAddress = curveAddressesProvider.get_id_info(
                i
            );
            // create a new registry with above registy adderss?
            // -> not alll addresses returned from the address provider have the .get_pool_from_lp_token method
            // -> should I check if method exists somehow? try/catch?
            address pool = ICurveRegistry(curveRegistryAddress)
                .get_pool_from_lp_token(_lpAddress);
            if (pool != address(0)) {
                return pool;
            }
        }
        revert("Pool not found");
    }

    // executeSelectorOnCurveRegistries(bytes) - Loop through all curve registries and try to staticcall
    // each of them using the manual selector
    // --> maybe similar to the fallback in oracle.sol?
    /// @notice Cycle through all curve registries and try to staticcall each one using manual selector
    function executeSelectorOnCurveRegistries() {}
}
