import pytest
import brownie
from operator import itemgetter

from brownie import interface, ZERO_ADDRESS

yfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

cyUsdcAddress = "0x76Eb2FE28b36B3ee97F3Adae0C69606eeDB2A37c"
daiAddress = "0x6B175474E89094C44Da98b954EedeAC495271d0F"


@pytest.fixture
def ironBankAdapter(
    RegistryAdapterIronBank,
    oracle,
    managementList,
    helper,
    ironBankAddressesGenerator,
    gov,
):
    comptrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
    ironBankAdapter = RegistryAdapterIronBank.deploy(
        oracle, managementList, helper, ironBankAddressesGenerator, {"from": gov}
    )
    return ironBankAdapter


# def test_interface(
#     ironBankAdapter, introspection, management, registryAdapterCommonInterface
# ):
#     adapterImplementsCommonInterface = introspection.implementsInterface(
#         ironBankAdapter, registryAdapterCommonInterface
#     )
#     assert adapterImplementsCommonInterface


# def test_adapter_info(ironBankAdapter):
#     adapterInfo = ironBankAdapter.adapterInfo()
#     assert adapterInfo[0] == ironBankAdapter
#     assert adapterInfo[1] == "IRON_BANK_MARKET"
#     assert adapterInfo[2] == "LENDING"


# def test_registry_address(ironBankAdapter):
#     assert not ironBankAdapter.registry() == ZERO_ADDRESS


# def test_assets_length(ironBankAdapter):
#     assetsLength = ironBankAdapter.assetsLength()
#     assert assetsLength > 0


# # test_set_asset_deprecated


# def test_assets_addresses(ironBankAdapter):
#     assetsAddresses = ironBankAdapter.assetsAddresses()
#     assert len(assetsAddresses) > 0
#     assert not assetsAddresses[0] == ZERO_ADDRESS


def test_asset_static(ironBankAdapter):
    assetStatic = ironBankAdapter.assetStatic(cyUsdcAddress)
    assetId = assetStatic[0]
    assetTypeId = assetStatic[1]
    name = assetStatic[2]
    version = assetStatic[3]
    assert assetId == cyUsdcAddress
    assert name == "Yearn USD Coin"
    assert version == "2.0.0"

    # Test token metadata
    token = assetStatic[4]
    tokenId = token[0]
    tokenName = token[1]
    tokenSymbol = token[2]
    tokenDecimals = token[3]

    assert tokenId == usdcAddress
    assert tokenName == "USD Coin"
    assert tokenSymbol == "USDC"
    assert tokenDecimals == 6


def test_asset_dynamic(ironBankAdapter, oracle):
    assetDynamic = ironBankAdapter.assetDynamic(cyUsdcAddress)
    assetId = assetDynamic[0]
    typeId = assetDynamic[1]
    tokenId = assetDynamic[2]
    underlyingTokenBalance = assetDynamic[3]
    # metadata = assetDynamic[4]

    # Test vault underlying balances
    tokenPriceUsdc = oracle.getPriceUsdcRecommended(tokenId)
    balance = underlyingTokenBalance[0]
    balanceUsdc = underlyingTokenBalance[1]
    tolerance = 5000000  # $5.00
    estimatedBalanceUsdc = tokenPriceUsdc * balance / 10 ** 6
    assert tokenPriceUsdc > 900000
    assert tokenPriceUsdc < 1100000
    assert balance > 0
    assert estimatedBalanceUsdc >= balanceUsdc - tolerance
    assert estimatedBalanceUsdc <= balanceUsdc + tolerance

    # Test market metadata


def test_assets_static(ironBankAdapter):
    assets = ironBankAdapter.assetsStatic()
    assert len(assets) > 1
    firstAsset = assets[0]
    assetId = firstAsset[0]
    assetTypeId = firstAsset[1]
    assetName = firstAsset[2]
    assetVersion = firstAsset[3]
    assert assetId == yfiVaultAddress
    assert assetName == "YFI yVault"
    assert assetTypeId == "VAULT_V2"
    assert assetVersion == "0.3.2"
    # print(assets)


# assets dynamic

# def test_assets_dynamic(ironBankAdapter):
#     assets = ironBankAdapter.assetsStatic()
#     assert len(assets) > 1
#     firstAsset = assets[0]
#     assetId = firstAsset[0]
#     assetTypeId = firstAsset[1]
#     assetName = firstAsset[2]
#     assetVersion = firstAsset[3]
#     assert assetId == yfiVaultAddress
#     assert assetName == "YFI yVault"
#     assert assetTypeId == "VAULT_V2"
#     assert assetVersion == "0.3.2"
#     # print(assets)


# def test_tokens(ironBankAdapter):
#     tokens = ironBankAdapter.tokens()
#     assetsLength = ironBankAdapter.assetsLength()
#     tokensLength = len(tokens)
#     assert tokensLength > 0
#     assert tokensLength < assetsLength


# def test_assets(ironBankAdapter):
#     assets = ironBankAdapter.assets()
#     assert len(assets) > 0
#     firstAsset = assets[0]
#     assetId = firstAsset[0]
#     assetName = firstAsset[1]
#     assetVersion = firstAsset[2]
#     assert assetId == yfiVaultAddress
#     assert assetName == "YFI yVault"
#     assert assetVersion == "0.3.2"
#     # print(assets)


# def test_position_of(ironBankAdapter, accounts):
#     # Deposit into YFI vault
#     v2YfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
#     vestedYfiAddress = "0x42A28ADDC15E627d19e780c89043b4B1d3629D34"
#     yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
#     yfiAccount = accounts.at(vestedYfiAddress, force=True)
#     yfi = interface.IERC20(yfiAddress)
#     yfi.approve(v2YfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
#     yfiVault = interface.V2Vault(v2YfiVaultAddress)
#     yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
#     userVaultBalance = yfiVault.balanceOf(vestedYfiAddress)
#     assert userVaultBalance > 0

#     # Test position
#     position = ironBankAdapter.positionOf(vestedYfiAddress, v2YfiVaultAddress)
#     assetId = position[0]
#     balance = position[1]
#     balanceUsdc = position[2]
#     assert assetId == v2YfiVaultAddress
#     assert balance == userVaultBalance
#     assert balanceUsdc > balance / 10 ** 18

#     # Test token position
#     tokenPosition = position[3]
#     tokenAddress = tokenPosition[0]
#     tokenBalance = tokenPosition[1]
#     tokenBalanceUsdc = tokenPosition[2]
#     assert tokenAddress == yfiAddress
#     assert tokenBalance > 0
#     assert tokenBalanceUsdc > tokenBalance / 10 ** 18

#     # Test token allowances
#     allowances = tokenPosition[3]
#     owner = allowances[0][0]
#     spender = allowances[0][1]
#     allowance = allowances[0][2]
#     assert owner == vestedYfiAddress
#     assert spender == v2YfiVaultAddress
#     assert allowance > 0


# def test_positions_of(ironBankAdapter, accounts):
#     # Deposit into YFI vault
#     v2YfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
#     vestedYfiAddress = "0x42A28ADDC15E627d19e780c89043b4B1d3629D34"
#     yfiAccount = accounts.at(vestedYfiAddress, force=True)
#     yfi = interface.IERC20(yfiAddress)
#     yfi.approve(v2YfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
#     yfiVault = interface.V2Vault(v2YfiVaultAddress)
#     yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
#     userVaultBalance = yfiVault.balanceOf(vestedYfiAddress)
#     assert userVaultBalance > 0

#     # Test positions
#     positions = ironBankAdapter.positionsOf(vestedYfiAddress)
#     position = positions[0]
#     assetId = position[0]
#     assert len(positions) > 0
#     assert assetId == v2YfiVaultAddress
