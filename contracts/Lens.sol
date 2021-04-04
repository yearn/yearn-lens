// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

import "./Utilities/Manageable.sol";

// Interfaces and helpers
interface IAdapter {
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

    struct AdapterInfo {
        address id;
        string typeId;
        string categoryId;
        string subcategoryId;
    }

    function adapterInfo() external view returns (AdapterInfo memory);

    function assets() external view returns (Asset[] memory);

    function positionsOf(address account)
        external
        view
        returns (Position[] memory);

    function asset() external view returns (Asset memory);

    function assetsLength() external view returns (uint256);

    function assetsAddresses() external view returns (address[] memory);
}

// Main contract
contract Lens is Manageable {
    uint256 public adaptersLength;
    mapping(address => uint256) private adapterIdxByAddress;
    mapping(uint256 => address) private adapterAddressByIdx;

    constructor(address _managementListAddress)
        Manageable(_managementListAddress)
    {}

    function addAdapter(address adapterAddress) public onlyManagers {
        bool adapterDoesntExist = adapterIdxByAddress[adapterAddress] == 0;
        if (adapterDoesntExist) {
            adaptersLength += 1;
            adapterAddressByIdx[adaptersLength] = adapterAddress;
            adapterIdxByAddress[adapterAddress] = adaptersLength;
        }
    }

    function addAdapters(address[] memory adapterAddresses)
        public
        onlyManagers
    {
        for (
            uint256 adapterIdx = 0;
            adapterIdx < adapterAddresses.length;
            adapterIdx++
        ) {
            address adapterAddress = adapterAddresses[adapterIdx];
            addAdapter(adapterAddress);
        }
    }

    // TODO: Implement
    // function replaceAdapter(address oldAddress, address newAddress) public {}

    function removeAdapter(address adapterAddress) external onlyManagers {
        bool adapterExists = adapterIdxByAddress[adapterAddress] != 0;
        if (adapterExists) {
            uint256 adapterIndex = adapterIdxByAddress[adapterAddress];
            delete adapterAddressByIdx[adapterIndex];
            delete adapterIdxByAddress[adapterAddress];
            adaptersLength -= 1;
        }
    }

    function adaptersInfo()
        external
        view
        returns (IAdapter.AdapterInfo[] memory)
    {
        IAdapter.AdapterInfo[] memory _adaptersInfo =
            new IAdapter.AdapterInfo[](adaptersLength);
        for (
            uint256 adapterIdx = 0;
            adapterIdx < adaptersLength;
            adapterIdx++
        ) {
            address adapterAddress = adapterAddressByIdx[adapterIdx + 1];
            IAdapter.AdapterInfo memory adapterInfo =
                IAdapter(adapterAddress).adapterInfo();
            _adaptersInfo[adapterIdx] = adapterInfo;
        }
        return _adaptersInfo;
    }

    function adaptersAddresses() external view returns (address[] memory) {
        address[] memory adapterList = new address[](adaptersLength);
        for (
            uint256 adapterIdx = 0;
            adapterIdx < adaptersLength;
            adapterIdx++
        ) {
            address adapterAddress = adapterAddressByIdx[adapterIdx + 1];
            adapterList[adapterIdx] = adapterAddress;
        }
        return adapterList;
    }

    function assetsFromAdapter(IAdapter adapterAddress)
        external
        view
        returns (IAdapter.Asset[] memory)
    {
        IAdapter adapter = IAdapter(adapterAddress);
        return adapter.assets();
    }

    function assetsLength() public view returns (uint256) {
        uint256 _assetsLength;
        for (
            uint256 adapterIdx = 0;
            adapterIdx < adaptersLength;
            adapterIdx++
        ) {
            address adapterAddress = adapterAddressByIdx[adapterIdx + 1];
            IAdapter adapter = IAdapter(adapterAddress);
            _assetsLength += adapter.assetsLength();
        }
        return _assetsLength;
    }

    function assetsAddresses() public view returns (address[] memory) {
        uint256 assetsLength = assetsLength();
        address[] memory assetsAddresses = new address[](assetsLength);
        uint256 assetIdx;
        for (
            uint256 adapterIdx = 0;
            adapterIdx < adaptersLength;
            adapterIdx++
        ) {
            address adapterAddress = adapterAddressByIdx[adapterIdx + 1];
            IAdapter adapter = IAdapter(adapterAddress);
            address[] memory assetAddresses = adapter.assetsAddresses();
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

    function assets() external view returns (IAdapter.Asset[] memory) {
        uint256 _assetsLength = assetsLength();
        IAdapter.Asset[] memory assetsList =
            new IAdapter.Asset[](_assetsLength);
        uint256 assetIdx;
        for (
            uint256 adapterIdx = 0;
            adapterIdx < adaptersLength;
            adapterIdx++
        ) {
            address adapterAddress = adapterAddressByIdx[adapterIdx + 1];
            IAdapter adapter = IAdapter(adapterAddress);
            IAdapter.Asset[] memory adapterAssets = adapter.assets();
            for (
                uint256 adapterAssetIdx = 0;
                adapterAssetIdx < adapterAssets.length;
                adapterAssetIdx++
            ) {
                assetsList[assetIdx] = adapterAssets[adapterAssetIdx];
                assetIdx++;
            }
        }
        return assetsList;
    }

    function positionsFromAdapter(address account, IAdapter adapterAddress)
        external
        view
        returns (IAdapter.Position[] memory)
    {
        IAdapter adapter = IAdapter(adapterAddress);
        return adapter.positionsOf(account);
    }

    function positionsOf(address account)
        external
        view
        returns (IAdapter.Position[] memory)
    {
        uint256 _assetsLength = assetsLength();
        IAdapter.Position[] memory positionsList =
            new IAdapter.Position[](_assetsLength);
        uint256 assetIdx;
        for (
            uint256 adapterIdx = 0;
            adapterIdx < adaptersLength;
            adapterIdx++
        ) {
            address adapterAddress = adapterAddressByIdx[adapterIdx + 1];
            IAdapter adapter = IAdapter(adapterAddress);
            IAdapter.Position[] memory adapterPositions =
                adapter.positionsOf(account);
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
