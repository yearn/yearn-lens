import pytest


def test_v2_vaults_adapter(oracle, V2Registry, RegisteryAdapterV2Vault, gov):
    v2RegistryAddress = "0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804"
    v2UsdcVaultV1Address = "0xe2F6b9773BF3A015E2aA70741Bde1498bdB9425b"
    v2UsdcVaultV2Address = "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9"
    v2DaiVaultAddress = "0x19D3364A399d251E894aC732651be8B0E4e85001"
    v2HegicVaultAddress = "0xe11ba472F74869176652C35D30dB89854b5ae84D"

    v2VaultsAdapter = RegisteryAdapterV2Vault.deploy(
        v2RegistryAddress, oracle, {"from": gov}
    )
    # print(v2VaultsAdapter.getAssetsTvl())
    # print(v2VaultsAdapter.getAssetsTvl())
    print(v2VaultsAdapter.getAsset(v2UsdcVaultV2Address))
    # print("v2UsdcVaultV1Address", v2VaultsAdapter.getAssetTvl(v2UsdcVaultV1Address))
    # print("v2UsdcVaultV2Address", v2VaultsAdapter.getAssetTvl(v2UsdcVaultV2Address))
    # print("v2WethVaultAddress", v2VaultsAdapter.getAssetTvl(v2WethVaultAddress))
    # print(
    #     "v2YfiVauv2HegicVaultAddressltAddress",
    #     v2VaultsAdapter.getAssetTvl(v2HegicVaultAddress),
    # )
