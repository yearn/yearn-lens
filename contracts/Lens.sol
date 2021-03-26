// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

import "../interfaces/Yearn/RegistryAdapter.sol";
import "./Utilities/Manageable.sol";

// TODO: Implement authentication
contract Lens is Manageable {
    mapping(uint256 => address) private registries;
    uint256 public numRegistries;
    mapping(address => uint256) private isRegistered;

    constructor(address _managementListAddress)
        Manageable(_managementListAddress)
    {}

    function addAdapter(address registryAddress) public onlyManagers {
        if (isRegistered[registryAddress] == 0) {
            numRegistries += 1;
            registries[numRegistries] = registryAddress;
            isRegistered[registryAddress] = numRegistries;
        }
    }

    function addAdapters(address[] memory registryAddresses)
        public
        onlyManagers
    {
        for (uint256 i = 0; i < registryAddresses.length; i++) {
            address registryAddress = registryAddresses[i];
            addAdapter(registryAddress);
        }
    }

    // TODO: Implement
    // function replaceRegistry(address oldAddress, address newAddress) public {}

    function removeAdapter(address registryAddress) public onlyManagers {
        if (isRegistered[registryAddress] != 0) {
            uint256 registryIndex = isRegistered[registryAddress];
            delete registries[registryIndex];
            delete isRegistered[registryAddress];
            numRegistries -= 1;
        }
    }

    function getAdapters() external view returns (address[] memory) {
        address[] memory registryList = new address[](numRegistries);
        for (uint256 i = 0; i < numRegistries; i++) {
            address registryAddress = registries[i + 1];
            registryList[i] = registryAddress;
        }
        return registryList;
    }

    function getAssetsFromAdapter(RegistryAdapter registryAdapterAddress)
        external
        view
        returns (RegistryAdapter.Asset[] memory)
    {
        RegistryAdapter registryAdapter =
            RegistryAdapter(registryAdapterAddress);
        return registryAdapter.getAssets();
    }

    function getAssetsLength() public view returns (uint256) {
        uint256 assetsLength;
        for (
            uint256 registryIdx = 0;
            registryIdx < numRegistries;
            registryIdx++
        ) {
            address registryAdapterAddress = registries[registryIdx + 1];
            RegistryAdapter registryAdapter =
                RegistryAdapter(registryAdapterAddress);
            assetsLength += registryAdapter.getAssetsLength();
        }
        return assetsLength;
    }

    // TODO: Implement array concat.. memcpy..?
    function getAssetsAddresses() public view returns (address[] memory) {
        uint256 assetsLength = getAssetsLength();
        address[] memory assetsAddresses = new address[](assetsLength);
        uint256 assetIdx;
        for (
            uint256 registryIdx = 0;
            registryIdx < numRegistries;
            registryIdx++
        ) {
            address registryAdapterAddress = registries[registryIdx + 1];
            RegistryAdapter registryAdapter =
                RegistryAdapter(registryAdapterAddress);
            address[] memory assetAddresses =
                registryAdapter.getAssetsAddresses();
            for (
                uint256 registryAssetIdx = 0;
                registryAssetIdx < assetAddresses.length;
                registryAssetIdx++
            ) {
                assetsAddresses[assetIdx] = assetAddresses[registryAssetIdx];
                assetIdx++;
            }
        }
        return assetsAddresses;
    }

    // TODO: Is there a better way to do this?
    function getAssets()
        external
        view
        returns (RegistryAdapter.Asset[] memory)
    {
        uint256 assetsLength = getAssetsLength();
        RegistryAdapter.Asset[] memory assetsList =
            new RegistryAdapter.Asset[](assetsLength);
        uint256 assetIdx;
        for (
            uint256 registryIdx = 0;
            registryIdx < numRegistries;
            registryIdx++
        ) {
            address registryAdapterAddress = registries[registryIdx + 1];
            RegistryAdapter registryAdapter =
                RegistryAdapter(registryAdapterAddress);
            RegistryAdapter.Asset[] memory registryAssets =
                registryAdapter.getAssets();

            // TODO: Can this be moved into a separate function? Dislike nested for loops..
            for (
                uint256 registryAssetIdx = 0;
                registryAssetIdx < registryAssets.length;
                registryAssetIdx++
            ) {
                assetsList[assetIdx] = registryAssets[registryAssetIdx];
                assetIdx++;
            }
        }
        return assetsList;
    }

    function getPositionsFromAdapter(
        address account,
        RegistryAdapter registryAdapterAddress
    ) external view returns (RegistryAdapter.Position[] memory) {
        RegistryAdapter registryAdapter =
            RegistryAdapter(registryAdapterAddress);
        return registryAdapter.getPositionsOf(account);
    }

    // TODO: Refactor..
    function getPositionsOf(address account)
        external
        view
        returns (RegistryAdapter.Position[] memory)
    {
        uint256 assetsLength = getAssetsLength();
        RegistryAdapter.Position[] memory positionsList =
            new RegistryAdapter.Position[](assetsLength);
        uint256 assetIdx;
        for (
            uint256 registryIdx = 0;
            registryIdx < numRegistries;
            registryIdx++
        ) {
            address registryAdapterAddress = registries[registryIdx + 1];
            RegistryAdapter registryAdapter =
                RegistryAdapter(registryAdapterAddress);
            RegistryAdapter.Position[] memory adapterPositions =
                registryAdapter.getPositionsOf(account);
            // TODO: Can this be moved into a separate function? Dislike nested for loops..
            for (
                uint256 registryAssetIdx = 0;
                registryAssetIdx < adapterPositions.length;
                registryAssetIdx++
            ) {
                positionsList[assetIdx] = adapterPositions[registryAssetIdx];
                assetIdx++;
            }
        }
        return positionsList;
    }
}
