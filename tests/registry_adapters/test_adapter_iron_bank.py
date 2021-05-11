import pytest
import brownie
from operator import itemgetter

from brownie import interface, Contract, ZERO_ADDRESS

yfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

cyUsdcAddress = "0x76Eb2FE28b36B3ee97F3Adae0C69606eeDB2A37c"
cyWethAddress = "0x41c84c0e2EE0b740Cf0d31F63f3B6F627DC6b393"
daiAddress = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
cyDaiAddress = "0x8e595470Ed749b85C6F7669de83EAe304C2ec68F"
cyYfiAddress = "0xFa3472f7319477c9bFEcdD66E4B948569E7621b9"
cyUsdtAddress = "0x48759f220ed983db51fa7a8c0d2aab8f3ce4166a"


@pytest.fixture
def ironBankAdapter(
    RegistryAdapterIronBank,
    oracle,
    managementList,
    helper,
    ironBankAddressesGenerator,
    ironBankTvlAdapter,
    gov,
):
    comptrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
    ironBankAdapter = RegistryAdapterIronBank.deploy(
        oracle,
        helper,
        ironBankAddressesGenerator,
        {"from": gov},
    )
    ironBankAdapter.setExtensionsAddresses([ironBankTvlAdapter], {"from": gov})
    return ironBankAdapter


def test_interface(
    ironBankAdapter, introspection, management, registryAdapterCommonInterface
):
    for method in registryAdapterCommonInterface:
        methodImplemented = introspection.implementsMethod(ironBankAdapter, method)
        if not methodImplemented:
            print(f"Missing method implementation: {method}")
        assert methodImplemented == True


def test_adapter_info(ironBankAdapter):
    adapterInfo = ironBankAdapter.adapterInfo()
    assert adapterInfo[0] == ironBankAdapter
    assert adapterInfo[1] == "IRON_BANK_MARKET"
    assert adapterInfo[2] == "LENDING"


def test_registry_address(ironBankAdapter):
    assert not ironBankAdapter.registryAddress() == ZERO_ADDRESS


def test_assets_length(ironBankAdapter):
    assetsLength = ironBankAdapter.assetsLength()
    assert assetsLength > 0


def test_assets_addresses(ironBankAdapter):
    assetsAddresses = ironBankAdapter.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_asset_static(ironBankAdapter):
    assetStatic = ironBankAdapter.assetStatic(cyUsdcAddress)
    assetId = assetStatic[0]
    typeId = assetStatic[1]
    tokenId = assetStatic[2]
    name = assetStatic[3]
    version = assetStatic[4]
    symbol = assetStatic[5]
    decimals = assetStatic[6]

    assert assetId == cyUsdcAddress
    assert name == "Yearn USD Coin"
    assert version == "2.0.0"
    assert tokenId == usdcAddress


def test_asset_dynamic(ironBankAdapter, oracle):
    assetDynamic = ironBankAdapter.assetDynamic(cyUsdcAddress)
    assetId = assetDynamic[0]
    typeId = assetDynamic[1]
    tokenId = assetDynamic[2]
    underlyingTokenBalance = assetDynamic[3]
    metadata = assetDynamic[4]

    # print("total supplied: ", metadata[0])
    # print("total borrowed: ", metadata[1])
    # print("lend apy bips: ", metadata[2])
    # print("borrow apy bips: ", metadata[3])
    # print("liquidity: ", metadata[4])
    # print("liquidity usdc: ", metadata[5])
    # print("collateral factor: ", metadata[6])
    # print("isactive: ", metadata[7])
    # print("exchange rate: ", metadata[8])


def test_assets_static(ironBankAdapter):
    assets = ironBankAdapter.assetsStatic()

    assert len(assets) > 1
    firstAsset = assets[0]
    assetId = firstAsset[0]
    assetTypeId = firstAsset[1]
    assetTokenId = firstAsset[2]
    assetName = firstAsset[3]
    assetVersion = firstAsset[4]
    assert assetId == cyWethAddress
    assert assetName == "Yearn Wrapped Ether"
    assert assetTypeId == "IRON_BANK_MARKET"
    assert assetVersion == "2.0.0"
    # print(assets)


def test_assets_dynamic(ironBankAdapter):
    assets = ironBankAdapter.assetsDynamic()
    assert len(assets) > 1
    for asset in assets:
        metadata = asset[4]
        supplyApyBips = metadata[2]
        borrowApyBips = metadata[3]
        liquidity = metadata[4]
        liquidityUsdc = metadata[5]
        collateralFactor = metadata[6]
        isActive = metadata[7]
        reserveFactor = metadata[8]
        exchangeRate = metadata[9]

        # print("asset: ", asset[0])
        # print("Supply apy: ", supplyApyBips)
        # print("Borrow apy: ", borrowApyBips)
        # print("Liquidity: ", liquidity)
        # print("Liquidity Usdc: ", liquidityUsdc)
        # print("Collateral factor: ", collateralFactor)
        # print("isActive; ", isActive)
        # print("reserveFactor: ", reserveFactor)
        # print("exchangeRate: ", exchangeRate)


def test_adapter_position_of(ironBankAdapter):
    adapterPosition = ironBankAdapter.adapterPositionOf(
        "0x48002Ca264076F85e7b22c9F650B7Ba168C90B87"
    )
    # print(adapterPosition)


def test_asset_user_metadata(ironBankAdapter, management):
    assetsUserMetadata = ironBankAdapter.assetsUserMetadata(
        "0x48002Ca264076F85e7b22c9F650B7Ba168C90B87"
    )
    for assetUserMetadata in assetsUserMetadata:
        assetId = assetUserMetadata[0]
        enteredMarket = assetUserMetadata[1]
        borrowlimitBips = assetUserMetadata[2]
        # print("assetId: ", assetId)
        # print("enteredMarket: ", enteredMarket)
        # print("borrowlimitBips: ", borrowlimitBips)
        # print("")


def test_assets_tokens_addresses(ironBankAdapter):
    tokens = ironBankAdapter.assetsTokensAddresses()
    assert len(tokens) > 0


def test_fallback_mechanism(ironBankAdapter, TvlAdapterIronBank):
    proxy = Contract.from_abi("", ironBankAdapter, TvlAdapterIronBank.abi)
    cyDaiTvl = proxy.assetTvlUsdc(cyDaiAddress)
    assert cyDaiTvl > 0


def print_position(position):
    assetId = position[0]
    tokenId = position[1]
    typeId = position[2]
    balance = position[3]
    underlyingTokenBalance = position[4]
    tokenAllowances = position[5]
    assetAllowances = position[6]
    assert balance > 0

    # print("assetId: ", assetId)
    # print("tokenId: ", tokenId)
    # print("typeId: ", typeId)
    # print("balance: ", balance)
    # print("underlyingTokenBalance: ", underlyingTokenBalance)
    # print("tokenAllowances: ", tokenAllowances)
    # print("assetAllowances: ", assetAllowances)
    # print("")


def test_asset_positions_of(ironBankAdapter, accounts):
    # Test position
    account = "0x48002Ca264076F85e7b22c9F650B7Ba168C90B87"
    positions = ironBankAdapter.assetsPositionsOf(account)

    for position in positions:
        print_position(position)


# numPositions = len(positions)
# firstPosition = positions[0]
# print_position(firstPosition)
# if numPositions > 1:
#     secondPosition = positions[1]
#     print_position(secondPosition)

# assetId = position[0]
# balance = position[1]
# balanceUsdc = position[2]
# assert assetId == v2YfiVaultAddress
# assert balance == userVaultBalance
# assert balanceUsdc > balance / 10 ** 18

# # Test token position
# tokenPosition = position[3]
# tokenAddress = tokenPosition[0]
# tokenBalance = tokenPosition[1]
# tokenBalanceUsdc = tokenPosition[2]
# assert tokenAddress == yfiAddress
# assert tokenBalance > 0
# assert tokenBalanceUsdc > tokenBalance / 10 ** 18

# # Test token allowances
# allowances = tokenPosition[3]
# owner = allowances[0][0]
# spender = allowances[0][1]
# allowance = allowances[0][2]
# assert owner == vestedYfiAddress
# assert spender == v2YfiVaultAddress
# assert allowance > 0


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
