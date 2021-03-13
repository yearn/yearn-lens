// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

contract GenericRegistry {
    mapping(uint256 => address) private assets;
    uint256 public numAssets;
    mapping(address => uint256) private isRegistered;

    constructor() public {}

    function addAsset(address assetAddress) public {
        if (isRegistered[assetAddress] == 0) {
            numAssets += 1;
            assets[numAssets] = assetAddress;
            isRegistered[assetAddress] = numAssets;
        }
    }

    function addAssets(address[] memory assetAddresses) public {
        for (uint256 i = 0; i < assetAddresses.length; i++) {
            address assetAddress = assetAddresses[i];
            addAsset(assetAddress);
        }
    }

    function removeAsset(address assetAddress) public {
        if (isRegistered[assetAddress] != 0) {
            uint256 registryIndex = isRegistered[assetAddress];
            delete assets[registryIndex];
            delete isRegistered[assetAddress];
            numAssets -= 1;
        }
    }

    function getAssets() external view returns (address[] memory) {
        address[] memory assetList = new address[](numAssets);
        for (uint256 i = 0; i < numAssets; i++) {
            address assetAddress = assets[i + 1];
            assetList[i] = assetAddress;
            return (assetList);
        }
    }
}
