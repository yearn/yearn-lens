// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

import "../../interfaces/Yearn/EarnToken.sol";
import "../../interfaces/Yearn/GenericRegistry.sol";
import "../../interfaces/Aave/AToken.sol";
import "../../interfaces/Aave/AToken.sol";
import "../../interfaces/Common/Oracle.sol";

contract RegistryAdapterEarn {
    address public registryAddress;
    Oracle public oracle;

    struct Asset {
        string name;
        address id;
        string version;
        AssetMetadata metadata;
    }

    struct AssetMetadata {
        address controller;
        uint256 totalAssets;
        uint256 totalSupply;
        uint256 pricePerShare;
    }

    constructor(address _registryAddress, address _oracleAddress) {
        require(_registryAddress != address(0), "Missing registry address");
        registryAddress = _registryAddress;
        oracle = Oracle(_oracleAddress);
    }

    function getAssetsAddresses() public view returns (address[] memory) {
        return GenericRegistry(registryAddress).getAssets();
    }

    function getAssetTvl(address earnTokenAddress)
        public
        view
        returns (uint256)
    {
        EarnToken earnToken = EarnToken(earnTokenAddress);
        uint256 valueInToken = earnToken.calcPoolValueInToken();
        address underlyingTokenAddress =
            getUnderlyingAssetAddress(earnTokenAddress);
        uint256 price = oracle.getPriceUsdc(underlyingTokenAddress);
        uint256 tvl = valueInToken * price;
        return tvl;
    }

    function getUnderlyingAssetAddress(address earnTokenAddress)
        public
        view
        returns (address)
    {
        EarnToken earnToken = EarnToken(earnTokenAddress);
        address aaveTokenAddress = earnToken.aaveToken();
        AToken aaveToken = AToken(aaveTokenAddress);
        address underlyingAssetAddress = aaveToken.underlyingAssetAddress();
        return underlyingAssetAddress;
    }

    function getAsset(address id) public view returns (Asset memory) {
        EarnToken earnToken = EarnToken(id);
        string memory name = earnToken.name();
        uint256 totalAssets = earnToken.pool();
        uint256 totalSupply = earnToken.totalSupply();
        string memory version = "0.00";
        uint256 pricePerShare = 0;
        // uint256 tvl = getTvl(id);
        bool earnTokenHasShares = totalSupply != 0;
        if (earnTokenHasShares) {
            pricePerShare = earnToken.getPricePerFullShare();
        }
        AssetMetadata memory metadata =
            AssetMetadata({
                controller: id,
                totalAssets: totalAssets,
                totalSupply: totalSupply,
                pricePerShare: pricePerShare
            });
        Asset memory asset =
            Asset({id: id, name: name, version: version, metadata: metadata});
        return asset;
    }

    function getAssets() external view returns (Asset[] memory) {
        address[] memory assetAddresses = getAssetsAddresses();
        uint256 numberOfAssets = assetAddresses.length;
        Asset[] memory assets = new Asset[](numberOfAssets);
        for (uint256 i = 0; i < numberOfAssets; i++) {
            address assetAddress = assetAddresses[i];
            Asset memory asset = getAsset(assetAddress);
            assets[i] = asset;
        }
        return assets;
    }
}
