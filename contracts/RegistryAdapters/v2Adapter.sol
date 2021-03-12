pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;
import "../../interfaces/Yearn/V2Vault.sol";

contract RegisteryAdapterV2Vault {
    address public registryAddress;
    string public constant registryType = "v2Adapter";

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

    constructor(address _registryAddress) {
        require(_registryAddress != address(0), "Missing registry address");
        registryAddress = _registryAddress;
    }

    function getVaultAddresses() public view returns (address[] memory) {
        address[] memory vaultAddresses = new address[](2);
        vaultAddresses[0] = 0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1;
        vaultAddresses[1] = 0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9;
        return vaultAddresses;
    }

    function getAssetsLength() public view returns (uint256) {
        address[] memory vaultAddresses = getVaultAddresses();
        return vaultAddresses.length;
    }

    function getAsset(address vaultAddress) public view returns (Asset memory) {
        V2Vault vault = V2Vault(vaultAddress);
        string memory vaultName = vault.name();
        uint256 totalAssets = vault.totalAssets();
        uint256 totalSupply = vault.totalSupply();
        uint256 pricePerShare = 0;
        string memory version = "0.00";
        bool vaultHasShares = totalSupply != 0;
        if (vaultHasShares) {
            pricePerShare = vault.pricePerShare();
        }

        AssetMetadata memory metadata =
            AssetMetadata({
                controller: vaultAddress,
                totalAssets: totalAssets,
                totalSupply: totalSupply,
                pricePerShare: pricePerShare
            });
        Asset memory asset =
            Asset({
                name: vaultName,
                id: vaultAddress,
                version: version,
                metadata: metadata
            });
        return asset;
    }

    function getAssets() external view returns (Asset[] memory) {
        address[] memory vaultAddresses = getVaultAddresses();
        uint256 numberOfVaults = vaultAddresses.length;
        Asset[] memory assets = new Asset[](numberOfVaults);
        for (uint256 i = 0; i < numberOfVaults; i++) {
            address vaultAddress = vaultAddresses[i];
            Asset memory asset = getAsset(vaultAddress);
            assets[i] = asset;
        }
        return assets;
    }
}
