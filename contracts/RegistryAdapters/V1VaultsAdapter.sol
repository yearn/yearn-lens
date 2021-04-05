// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

import "../../interfaces/Yearn/V1Vault.sol";
import "../../interfaces/Yearn/V1Registry.sol";
import "../../interfaces/Common/IERC20.sol";

contract RegisteryAdapterV1Vault {
    address public registryAddress;

    struct AdapterInfo {
        address id;
        string typeId;
        string categoryId;
    }

    struct Asset {
        string name;
        address id;
        string version;
        AssetMetadata metadata;
    }

    // TODO: Inherit from standardized interface?
    struct Position {
        address assetId;
        string typeId;
        uint256 depositedBalance;
        uint256 tokenBalance;
        uint256 tokenAllowance;
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

    function adapterInfo() public view returns (AdapterInfo memory) {
        return
            AdapterInfo({
                id: address(this),
                typeId: "v1Vault",
                categoryId: "vault"
            });
    }

    function assetsAddresses() public view returns (address[] memory) {
        return V1Registry(registryAddress).getVaults();
    }

    function asset(address id) public view returns (Asset memory) {
        V1Vault vault = V1Vault(id);
        string memory name = vault.name();
        uint256 totalAssets = vault.balance();
        uint256 totalSupply = vault.totalSupply();
        string memory version = "0.00";
        uint256 pricePerShare = 0;
        bool vaultHasShares = totalSupply != 0;
        if (vaultHasShares) {
            pricePerShare = vault.getPricePerFullShare();
        }

        AssetMetadata memory metadata =
            AssetMetadata({
                controller: id,
                totalAssets: totalAssets,
                totalSupply: totalSupply,
                pricePerShare: pricePerShare
            });
        return
            Asset({id: id, name: name, version: version, metadata: metadata});
    }

    function assetsLength() public view returns (uint256) {
        return V1Registry(registryAddress).getVaultsLength();
    }

    function assets() external view returns (Asset[] memory) {
        address[] memory _assetsAddresses = assetsAddresses();
        uint256 numberOfVaults = _assetsAddresses.length;
        Asset[] memory _assets = new Asset[](numberOfVaults);
        for (uint256 i = 0; i < numberOfVaults; i++) {
            address assetAddress = _assetsAddresses[i];
            Asset memory _asset = asset(assetAddress);
            _assets[i] = _asset;
        }
        return _assets;
    }

    function positionOf(address accountAddress, address assetAddress)
        public
        view
        returns (Position memory)
    {
        V1Vault _asset = V1Vault(assetAddress);
        address tokenAddress = _asset.token();
        IERC20 token = IERC20(tokenAddress);
        uint256 depositedBalance =
            (_asset.balanceOf(accountAddress) * _asset.getPricePerFullShare()) /
                10**18;
        uint256 tokenBalance = token.balanceOf(accountAddress);
        uint256 tokenAllowance = token.allowance(accountAddress, assetAddress);
        Position memory position =
            Position({
                assetId: assetAddress,
                typeId: "deposit",
                depositedBalance: depositedBalance,
                tokenBalance: tokenBalance,
                tokenAllowance: tokenAllowance
            });
        return position;
    }

    function positionsOf(address accountAddress)
        external
        view
        returns (Position[] memory)
    {
        address[] memory vaultAddresses = assetsAddresses();
        uint256 numberOfVaults = vaultAddresses.length;
        Position[] memory positions = new Position[](numberOfVaults);
        for (uint256 i = 0; i < numberOfVaults; i++) {
            address vaultAddress = vaultAddresses[i];
            Position memory position = positionOf(accountAddress, vaultAddress);

            positions[i] = position;
        }
        return positions;
    }
}
