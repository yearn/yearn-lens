// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

import "../Utilities/Ownable.sol";

contract GenericRegistry is Ownable {
    mapping(uint256 => address) private _assets;
    uint256 public numAssets;
    mapping(address => uint256) private isRegistered;

    constructor(address[] memory _initialAddresses) {
        if (_initialAddresses.length > 0) {
            addAssets(_initialAddresses);
        }
    }

    function addAsset(address assetAddress) public onlyOwner {
        if (isRegistered[assetAddress] == 0) {
            numAssets += 1;
            _assets[numAssets] = assetAddress;
            isRegistered[assetAddress] = numAssets;
        }
    }

    function addAssets(address[] memory assetAddresses) public onlyOwner {
        for (uint256 i = 0; i < assetAddresses.length; i++) {
            address assetAddress = assetAddresses[i];
            addAsset(assetAddress);
        }
    }

    function removeAsset(address assetAddress) external onlyOwner {
        if (isRegistered[assetAddress] != 0) {
            uint256 registryIndex = isRegistered[assetAddress];
            delete _assets[registryIndex];
            delete isRegistered[assetAddress];
            numAssets -= 1;
        }
    }

    function assets() external view returns (address[] memory) {
        address[] memory assetList = new address[](numAssets);
        for (uint256 i = 0; i < numAssets; i++) {
            address assetAddress = _assets[i + 1];
            assetList[i] = assetAddress;
        }
        return assetList;
    }
}
