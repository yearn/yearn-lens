import pytest


@pytest.fixture
def oracle(Oracle, gov):
    return gov.deploy(Oracle)


def test_v2_vaults_adapter(oracle, V2Registry, RegisteryAdapterV2Vault, gov):
    v2Registry = V2Registry.deploy({"from": gov})

    v2UsdcVaultV1Address = "0xe2F6b9773BF3A015E2aA70741Bde1498bdB9425b"
    v2UsdcVaultV2Address = "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9"
    v2WethVaultAddress = "0x19D3364A399d251E894aC732651be8B0E4e85001"
    v2YfiVaultAddress = "0xe11ba472F74869176652C35D30dB89854b5ae84D"

    v2VaultsAdapter = RegisteryAdapterV2Vault.deploy(v2Registry, oracle, {"from": gov})

    # 0.3.0
    v2Registry.newRelease(v2UsdcVaultV1Address, ({"from": gov}))
    v2Registry.endorseVault(v2UsdcVaultV1Address, ({"from": gov}))

    # 0.3.2
    v2Registry.newRelease(v2UsdcVaultV2Address, ({"from": gov}))
    v2Registry.endorseVault(v2UsdcVaultV2Address, ({"from": gov}))
    v2Registry.endorseVault(v2WethVaultAddress, ({"from": gov}))
    v2Registry.endorseVault(v2YfiVaultAddress, ({"from": gov}))

    v2VaultsAdapter = RegisteryAdapterV2Vault.deploy(v2Registry, oracle, {"from": gov})
    print("v2UsdcVaultV1Address", v2VaultsAdapter.getAssetTvl(v2UsdcVaultV1Address))
    print("v2UsdcVaultV2Address", v2VaultsAdapter.getAssetTvl(v2UsdcVaultV2Address))
    print("v2WethVaultAddress", v2VaultsAdapter.getAssetTvl(v2WethVaultAddress))
    print("v2YfiVaultAddress", v2VaultsAdapter.getAssetTvl(v2YfiVaultAddress))
