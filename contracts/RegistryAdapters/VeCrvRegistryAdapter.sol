// // SPDX-License-Identifier: MIT

// pragma solidity ^0.8.2;
// pragma experimental ABIEncoderV2;

// import "../../interfaces/Yearn/V1Registry.sol";

// contract VeCrvRegistryAdapter {
//     address public registryAddress;

//     struct Asset {
//         string name;
//         address id;
//         string version;
//         AssetMetadata metadata;
//     }

//     struct AssetMetadata {
//         address controller;
//         uint256 totalAssets;
//         uint256 totalSupply;
//         uint256 pricePerShare;
//     }

//     constructor(address _registryAddress) {
//         require(_registryAddress != address(0), "Missing registry address");
//         registryAddress = _registryAddress;
//     }

//     function getVaultAddresses() public view returns (address[] memory) {
//         return V1Registry(registryAddress).getVaults();
//     }

//     function getAsset(address id) public view returns (Asset memory) {
//         IV1Vault vault = IV1Vault(id);
//         string memory name = vault.name();
//         uint256 totalAssets = vault.balance();
//         uint256 totalSupply = vault.totalSupply();
//         string memory version = "0.00";
//         uint256 pricePerShare = 0;
//         bool vaultHasShares = totalSupply != 0;
//         if (vaultHasShares) {
//             pricePerShare = vault.getPricePerFullShare();
//         }

//         AssetMetadata memory metadata =
//             AssetMetadata({
//                 controller: id,
//                 totalAssets: totalAssets,
//                 totalSupply: totalSupply,
//                 pricePerShare: pricePerShare
//             });
//         Asset memory asset =
//             Asset({id: id, name: name, version: version, metadata: metadata});
//         return asset;
//     }

//     function getAssets() external view returns (Asset[] memory) {
//         address[] memory vaultAddresses = getVaultAddresses();
//         uint256 numberOfVaults = vaultAddresses.length;
//         Asset[] memory assets = new Asset[](numberOfVaults);
//         for (uint256 i = 0; i < numberOfVaults; i++) {
//             address vaultAddress = vaultAddresses[i];
//             Asset memory asset = getAsset(vaultAddress);
//             assets[i] = asset;
//         }
//         return assets;
//     }
// }
