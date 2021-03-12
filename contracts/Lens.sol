pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;
import "../../interfaces/Yearn/V1Vault.sol";
import "../../interfaces/Yearn/V1Registry.sol";
import "../../interfaces/Yearn/RegistryAdapter.sol";

contract Lens {
    mapping(uint256 => address) private registries;
    uint256 public numRegistries;
    mapping(address => uint256) private isRegistered;

    constructor() public {}

    function addRegistry(address registryAddress) public {
        if (isRegistered[registryAddress] == 0) {
            numRegistries += 1;
            registries[numRegistries] = registryAddress;
            isRegistered[registryAddress] = numRegistries;
        }
    }

    function addRegistries(address[] memory registryAddresses) public {
        for (uint256 i = 0; i < registryAddresses.length; i++) {
            address registryAddress = registryAddresses[i];
            addRegistry(registryAddress);
        }
    }

    function removeRegistry(address registryAddress) public {
        if (isRegistered[registryAddress] != 0) {
            uint256 registryIndex = isRegistered[registryAddress];
            delete registries[registryIndex];
            delete isRegistered[registryAddress];
            numRegistries -= 1;
        }
    }

    function getRegistries() external view returns (address[] memory) {
        address[] memory registryList = new address[](numRegistries);
        for (uint256 i = 0; i < numRegistries; i++) {
            address registryAddress = registries[i + 1];
            registryList[i] = registryAddress;
        }
        return registryList;
    }

    function getAssetsFromAdapter(RegistryAdapter registryAdapterAddress)
        external
        view
        returns (RegistryAdapter.Asset[] memory)
    {
        RegistryAdapter registryAdapter =
            RegistryAdapter(registryAdapterAddress);
        return registryAdapter.getAssets();
    }

    function getAssetsLength() internal view returns (uint256) {
        uint256 assetsLength;
        for (uint256 i = 0; i < numRegistries; i++) {
            address registryAdapterAddress = registries[i + 1];
            RegistryAdapter registryAdapter =
                RegistryAdapter(registryAdapterAddress);
            assetsLength += registryAdapter.getAssetsLength();
        }
        return assetsLength;
    }

    function getAssets()
        external
        view
        returns (RegistryAdapter.Asset[] memory)
    {
        uint256 assetsLength = getAssetsLength();
        RegistryAdapter.Asset[] memory assetsList =
            new RegistryAdapter.Asset[](assetsLength);
        uint256 currentIdx;
        for (uint256 i = 0; i < numRegistries; i++) {
            address registryAdapterAddress = registries[i + 1];
            RegistryAdapter registryAdapter =
                RegistryAdapter(registryAdapterAddress);
            RegistryAdapter.Asset[] memory registryAssets =
                registryAdapter.getAssets();
            for (uint256 c = 0; c < registryAssets.length; c++) {
                assetsList[currentIdx] = registryAssets[c];
                currentIdx++;
            }
        }
        return assetsList;
    }
}
