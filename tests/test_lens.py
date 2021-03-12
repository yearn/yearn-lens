import pytest
import brownie
from brownie import V2Registry

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
    gov,
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
    v2VaultsAdapter = RegisteryAdapterV2Vault.deploy(v2Registry, {"from": gov})

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

    print("lll", lens.getAssetsAddresses())


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

############### EARN
# earnRegistry = GenericRegistry.deploy({"from": gov})
# # Earn v1
# yDaiV1Address = "0x16de59092dAE5CcF4A1E6439D611fd0653f0Bd01"
# yUsdV1Address = "0xd6aD7a6750A7593E092a9B218d66C0A814a3436e"
# yUsdtV1Address = "0x83f798e925BcD4017Eb265844FDDAbb448f1707D"
# yTusdV1Address = "0x73a052500105205d34daf004eab301916da8190f"
# ySusdV1Address = "0xF61718057901F84C4eEC4339EF8f0D86D2B45600"

# # Earn v2
# yDaiV2Address = "0xC2cB1040220768554cf699b0d863A3cd4324ce32"
# yUsdcV2Address = "0x26EA744E5B887E5205727f55dFBE8685e3b21951"
# yUsdtV2Address = "0xE6354ed5bC4b393a5Aad09f21c46E101e692d447"
# yBusdV2Address = "0x04bC0Ab673d88aE9dbC9DA2380cB6B79C4BCa9aE"
# yWbtcV2Address = "0x04Aa51bbcB46541455cCF1B8bef2ebc5d3787EC9"

# earnRegistry.addAssets(
#     [
#         # yDaiV1Address,
#         # yUsdV1Address,
#         # yTusdV1Address,
#         # yUsdtV1Address,
#         # ySusdV1Address,
#         # yDaiV2Address,
#         # yUsdcV2Address,
#         yUsdtV2Address,
#         yBusdV2Address,
#     ]
# )
# oracle = Oracle.deploy({"from": gov})
# earnAdapter = RegistryAdapterEarn.deploy(earnRegistry, oracle, {"from": gov})
# # print("Earn assets", earnAdapter.getAssets())
# print("Earn assets", earnAdapter.getAssetTvl(yDaiV2Address))
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

