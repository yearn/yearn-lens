// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

// Common interface all adapters must implement
interface RegistryAdapter {
    struct Asset {
        string name;
        address id;
        string version;
    }

    struct Position {
        address assetId;
        uint256 depositedBalance;
        uint256 tokenBalance;
        uint256 tokenAllowance;
    }

    function getAssets() external view returns (Asset[] memory);

    function getPositionsOf(address account)
        external
        view
        returns (Position[] memory);

    function getAsset() external view returns (Asset memory);

    function getAssetsLength() external view returns (uint256);

    function getAssetsAddresses() external view returns (address[] memory);
}
