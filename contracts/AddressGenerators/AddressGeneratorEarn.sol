// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

import "../Utilities/Ownable.sol";

/*******************************************************
 *                       Interfaces                    *
 *******************************************************/
interface IEarnRegistry {
    function assets() external view returns (address[] memory);

    function numAssets() external view returns (uint256);
}

/*******************************************************
 *                    Generator Logic                  *
 *******************************************************/
contract AddressesGeneratorEarn is Ownable {
    mapping(address => bool) public assetDeprecated; // Support for deprecating assets. If an asset is deprecated it will not appear is results
    uint256 public numberOfDeprecatedAssets; // Used to keep track of the number of deprecated assets for an adapter
    address[] public positionSpenderAddresses; // A settable list of spender addresses with which to fetch asset allowances
    IEarnRegistry public registry; // The registry is used to fetch the list of assets

    /**
     * Information about the generator
     */
    struct GeneratorInfo {
        address id; // Generator address
        string typeId; // Generator typeId (for example "VAULT_V2" or "IRON_BANK_MARKET")
        string categoryId; // Generator categoryId (for example "VAULT")
    }

    /**
     * Configure generator
     */
    constructor(address _registryAddress) {
        require(_registryAddress != address(0), "Missing registry address");
        registry = IEarnRegistry(_registryAddress);
    }

    /**
     * Deprecate or undeprecate an asset. Deprecated assets will not appear in any adapter or generator method call responses
     */
    function setAssetDeprecated(address assetAddress, bool newDeprecationStatus)
        public
        onlyOwner
    {
        bool currentDeprecationStatus = assetDeprecated[assetAddress];
        if (currentDeprecationStatus == newDeprecationStatus) {
            revert("Generator: Unable to change asset deprecation status");
        }
        if (newDeprecationStatus == true) {
            numberOfDeprecatedAssets++;
        } else {
            numberOfDeprecatedAssets--;
        }
        assetDeprecated[assetAddress] = newDeprecationStatus;
    }

    /**
     * Set position spender addresses. Used by `adapter.assetAllowances(address,address)`.
     */
    function setPositionSpenderAddresses(address[] memory addresses)
        public
        onlyOwner
    {
        positionSpenderAddresses = addresses;
    }

    /**
     * Set registry address
     */
    function setRegistryAddress(address _registryAddress) public onlyOwner {
        require(_registryAddress != address(0), "Missing registry address");
        registry = IEarnRegistry(_registryAddress);
    }

    /**
     * Fetch a list of position spender addresses
     */
    function getPositionSpenderAddresses()
        external
        view
        returns (address[] memory)
    {
        return positionSpenderAddresses;
    }

    /**
     * Fetch generator info
     */
    function generatorInfo() public view returns (GeneratorInfo memory) {
        return
            GeneratorInfo({
                id: address(this),
                typeId: "EARN",
                categoryId: "SAFE"
            });
    }

    /**
     * Fetch the total number of assets
     */
    function assetsLength() public view returns (uint256) {
        return registry.numAssets() - numberOfDeprecatedAssets;
    }

    /**
     * Fetch all asset addresses
     */
    function assetsAddresses() public view returns (address[] memory) {
        uint256 _numberOfAssets = registry.numAssets();
        uint256 _filteredAssetsLength = assetsLength();
        address[] memory originalAddresses = registry.assets();
        if (_numberOfAssets == _filteredAssetsLength) {
            return originalAddresses;
        }
        uint256 currentAssetIdx;
        for (uint256 assetIdx = 0; assetIdx < _numberOfAssets; assetIdx++) {
            address currentAssetAddress = originalAddresses[assetIdx];
            bool assetIsNotDeprecated =
                assetDeprecated[currentAssetAddress] == false;
            if (assetIsNotDeprecated) {
                originalAddresses[currentAssetIdx] = currentAssetAddress;
                currentAssetIdx++;
            }
        }
        bytes memory encodedAddresses = abi.encode(originalAddresses);
        assembly {
            // Manually truncate the filtered list
            mstore(add(encodedAddresses, 0x40), _filteredAssetsLength)
        }
        address[] memory filteredAddresses =
            abi.decode(encodedAddresses, (address[]));

        return filteredAddresses;
    }
}
