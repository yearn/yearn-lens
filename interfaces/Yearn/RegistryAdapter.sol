pragma solidity ^0.8.2;

interface RegistryAdapter {
    struct Asset {
        string name;
        address id;
        string version;
    }

    function getAssets() external view returns (Asset[] memory);

    function getAsset() external view returns (Asset memory);

    function getAssetsLength() external view returns (uint256);
}
