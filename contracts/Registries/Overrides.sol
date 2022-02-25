// SPDX-License-Identifier: MIT

pragma solidity 0.8.11;

import "../Utilities/Ownable.sol";

interface ICurveRegistry {
    function get_pool_from_lp_token(address) external view returns (address);

    function pool_list(uint256) external view returns (address);

    function pool_count() external view returns (uint256);
}

interface ICurveAddressesProvider {
    function max_id() external view returns (uint256);

    function get_address(uint256) external view returns (address);
}

contract CurveRegistryOverrides is Ownable {
    ICurveAddressesProvider public curveAddressesProvider;
    ICurveRegistry public curveRegistry;
    mapping(address => address) public poolByLpOverride;
    address[] public poolAddresses;

    constructor(
        address _curveAddressesProviderAddress,
        address _curveRegistryAddress
    ) {
        require(
            _curveAddressesProviderAddress != address(0),
            "Missing Curve Addresses Provider address"
        );
        require(
            _curveRegistryAddress != address(0),
            "Missing Curve Registry address"
        );
        curveAddressesProvider = ICurveAddressesProvider(
            _curveAddressesProviderAddress
        );
        curveRegistry = ICurveRegistry(_curveRegistryAddress);
    }

    /// @notice Updates Curve Registry Address
    function addCurveRegistry(address _curveRegistryAddress) public onlyOwner {
        require(
            _curveRegistryAddress != address(0),
            "Missing Curve Registry Address"
        );
        curveRegistry = ICurveRegistry(_curveRegistryAddress);
    }

    /// @notice Returns both override and curve registry pools as list
    function curveRegistriesList() public view returns (address[] memory) {
        uint256 poolOverrideCount = poolAddresses.length;
        uint256 poolRegistryCount = curveRegistry.pool_count();
        uint256 numRegistries = poolOverrideCount + poolRegistryCount;
        address[] memory _registries = new address[](numRegistries);
        for (uint256 i; i < poolOverrideCount; i++) {
            _registries[i] = poolAddresses[i];
        }
        for (uint256 i; i < poolRegistryCount; i++) {
            _registries[i + poolOverrideCount] = curveRegistry.pool_list(i);
        }
        return _registries;
    }

    /// @notice Adds an override pool address for an LP
    /// @dev Maintains an additional pool address list for indexing
    function setPoolForLp(address _poolAddress, address _lpAddress)
        public
        onlyOwner
    {
        poolByLpOverride[_lpAddress] = _poolAddress;
        poolAddresses.push(_poolAddress);
    }

    /// @notice Search through pool registry overrides and curve registries for a LP Pool
    function poolByLp(address _lpAddress) public view returns (address) {
        address pool = poolByLpOverride[_lpAddress];
        if (pool != address(0)) {
            return pool;
        }
        pool = executeSelectorOnCurveRegistries(_lpAddress);
        return pool;
    }

    /// @notice Cycle through all curve registries and try to staticcall each one using manual selector
    /// @dev return type is inconsistent across curve registres
    function executeSelectorOnCurveRegistries(address _lpAddress)
        public
        view
        returns (address)
    {
        uint256 numRegistries = curveAddressesProvider.max_id() + 1;
        address curveRegistryAddress;
        address pool;
        bool success;
        bytes memory data;
        for (uint256 i; i < numRegistries; i++) {
            curveRegistryAddress = curveAddressesProvider.get_address(i);
            (success, data) = address(curveRegistryAddress).staticcall(
                abi.encodeWithSignature(
                    "get_pool_from_lp_token(address)",
                    _lpAddress
                )
            );
            if (success && data.length > 0) {
                pool = abi.decode(data, (address));
                if (pool != address(0)) {
                    return pool;
                }
            }
        }
        revert("Pool not found");
    }
}
