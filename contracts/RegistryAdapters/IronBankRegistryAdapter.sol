// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

import "../../interfaces/Yearn/V1Vault.sol";
import "../../interfaces/Cream/Unitroller.sol";

contract RegistryAdapterIronBank {
    address public registryAddress;

    struct Asset {
        string name;
        address id;
        string version;
        uint256 balanceUsd;
        AssetMetadata metadata;
    }

    struct AssetMetadata {
        address controller;
        uint256 totalAssets;
        uint256 totalSupply;
        uint256 pricePerShare;
    }

    constructor(address _registryAddress) {
        require(_registryAddress != address(0), "Missing registry address");
        registryAddress = _registryAddress;
    }

    function getAllMarkets() public view returns (address[] memory) {
        return Unitroller(registryAddress).getAllMarkets();
    }
}
