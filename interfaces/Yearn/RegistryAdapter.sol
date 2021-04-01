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

    function assets() external view returns (Asset[] memory);

    function positionsOf(address account)
        external
        view
        returns (Position[] memory);

    function asset() external view returns (Asset memory);

    function assetsLength() external view returns (uint256);

    function assetsAddresses() external view returns (address[] memory);
}
