import pytest
import brownie

from brownie import *

# def test_v1_adapter(RegisteryAdapterV1Vault, gov):
#     v1RegistryAddress = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0"
#     v1VaultsAdapter = RegisteryAdapterV1Vault.deploy(v1RegistryAddress, {"from": gov})
#     # print("Assets", v1VaultsAdapter.getAssets())
#     print("Addresses", v1VaultsAdapter.getVaultAddresses())


# def test_v2_adapter(RegisteryAdapterV2Vault, gov):
#     v2RegistryAddress = "0xE15461B18EE31b7379019Dc523231C57d1Cbc18c"
#     v2VaultsAdapter = RegisteryAdapterV2Vault.deploy(v2RegistryAddress, {"from": gov})
#     # print("Addresses", v2VaultsAdapter.getVaultAddresses())
#     print("Assets", v2VaultsAdapter.getAssets())


def test_lens(
    interface,
    Lens,
    RegisteryAdapterV1Vault,
    RegisteryAdapterV2Vault,
    RegistryAdapterIronBank,
    RegistryAdapterEarn,
    Oracle,
    oracle,
    gov,
    V2Registry,
    GenericRegistry,
):

    v1RegistryAddress = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0"
    v1VaultsAdapter = RegisteryAdapterV1Vault.deploy(v1RegistryAddress, {"from": gov})

    v2UsdcVaultV1Address = "0xe2F6b9773BF3A015E2aA70741Bde1498bdB9425b"
    v2UsdcVaultV2Address = "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9"
    v2WethVaultAddress = "0x19D3364A399d251E894aC732651be8B0E4e85001"
    v2YfiVaultAddress = "0xe11ba472F74869176652C35D30dB89854b5ae84D"
    v2Registry = V2Registry.deploy({"from": gov})

    # v2RegistryAddress = "0xE15461B18EE31b7379019Dc523231C57d1Cbc18c""
    v2VaultsAdapter = RegisteryAdapterV2Vault.deploy(v2Registry, oracle, {"from": gov})

    # 0.3.0
    v2Registry.newRelease(v2UsdcVaultV1Address, ({"from": gov}))
    v2Registry.endorseVault(v2UsdcVaultV1Address, ({"from": gov}))

    # 0.3.2
    v2Registry.newRelease(v2UsdcVaultV2Address, ({"from": gov}))
    v2Registry.endorseVault(v2UsdcVaultV2Address, ({"from": gov}))
    v2Registry.endorseVault(v2WethVaultAddress, ({"from": gov}))
    v2Registry.endorseVault(v2YfiVaultAddress, ({"from": gov}))

    lens = Lens.deploy({"from": gov})
    lens.addRegistry(v2VaultsAdapter)
    lens.addRegistry(v1VaultsAdapter)

    # print("lll", lens.getAssetsAddresses())


# # print(
# #     "balances",
# #     v1VaultsAdapter.getPositionsOf("0x4800C3b3B570bE4EeE918404d0f847c1Bf25826b"),
# # )

# print(
#     "lens balances",
#     lens.getPositionsOf("0x4800C3b3B570bE4EeE918404d0f847c1Bf25826b"),
# )

# print(lens.getRegistries())
# print(v2VaultsAdapter.getAssets())

# lens.removeRegistry(v2VaultsAdapter)
# print(lens.numRegistries())
# print("Combined assets", lens.getAssets())
# print("yyy", lens.getAssetsFromAdapter(v2VaultsAdapter))

# v2RegistryAddress = "0xE15461B18EE31b7379019Dc523231C57d1Cbc18c"
# ironBankRegistryAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"

# v2Adapter = RegisteryAdapterV2Vault.deploy(v2RegistryAddress, {"from": gov})

# ###################

# wethAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
# wbtcAddress = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"

# price = oracle.getPriceFromRouterUsdc(wbtcAddress)
# print("price", price)
# print(
#     "isCurveLpToken",
#     oracle.isCurveLpToken("0x6c3f90f043a72fa612cbac8115ee7e52bde6e490"),
# )
# print(
#     "underlying token",
#     oracle.getFirstUnderlyingCoinFromPool(
#         "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
#     ),
# )
# print("virt", oracle.getVirtualPrice("0x6c3f90f043a72fa612cbac8115ee7e52bde6e490"))
# print("base", oracle.getBasePrice("0x6c3f90f043a72fa612cbac8115ee7e52bde6e490"))
# print(
#     "virt * base",
#     oracle.getCurvePriceUsdc("0x6c3f90f043a72fa612cbac8115ee7e52bde6e490"),
# )


# ironBankAdapter = RegistryAdapterIronBank.deploy(
#     ironBankRegistryAddress, {"from": gov}
# )

# print("xxx", ironBankAdapter.getAllMarkets())


# usdcVaultAddress = "0xa9fE4601811213c340e850ea305481afF02f5b28"
# yCrvAddress = "0x5dbcF33D8c2E976c6b560249878e6F1491Bca25c"
# threeCrvAddress = "0x9cA85572E6A3EbF24dEDd195623F188735A5179f"
# vault = interface.Vault_v0_3_0(usdcVaultAddress, owner=gov)
# lens.addAsset(yCrvAddress, "vault")
# lens.addAsset(threeCrvAddress, "vault")
# print(lens.getVaultInfo(yCrvAddress))

# print(lens.getAssets())
# print(lens.getUserBalances())
# print(lens.getBump())
# vaultData = lens.getVault(vault)

# print('pps', vault.pricePerShare())
# print('vault data', vaultData)
# print('vault data', lens.getVaults())

