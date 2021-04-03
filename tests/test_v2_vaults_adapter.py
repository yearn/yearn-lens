import pytest
import brownie
from operator import itemgetter

from brownie import interface, ZERO_ADDRESS

yfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"


@pytest.fixture
def v2VaultsAdapter(RegisteryAdapterV2Vault, managementList, oracle, management):
    v2RegistryAddress = "0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804"
    trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
    positionSpenderAddresses = [trustedMigratorAddress]
    v2VaultsAdapter = RegisteryAdapterV2Vault.deploy(
        v2RegistryAddress,
        oracle,
        managementList,
        positionSpenderAddresses,
        {"from": management},
    )
    return v2VaultsAdapter


def test_set_position_spender_addresses(v2VaultsAdapter, management, rando):
    ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"
    with brownie.reverts():
        v2VaultsAdapter.setPositionSpenderAddresses([ethZapAddress], {"from": rando})
    v2VaultsAdapter.setPositionSpenderAddresses([ethZapAddress], {"from": management})
    assert v2VaultsAdapter.positionSpenderAddresses(0) == ethZapAddress


def test_registry_address(v2VaultsAdapter):
    assert not v2VaultsAdapter.registryAddress() == ZERO_ADDRESS


def test_adapter_info(v2VaultsAdapter):
    adapterInfo = v2VaultsAdapter.adapterInfo()
    assert adapterInfo[0] == v2VaultsAdapter
    assert adapterInfo[1] == "v2Vault"
    assert adapterInfo[2] == "deposit"
    assert adapterInfo[3] == "vault"


def test_assets_addresses(v2VaultsAdapter):
    assetsAddresses = v2VaultsAdapter.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_assets_length(v2VaultsAdapter):
    assetsLength = v2VaultsAdapter.assetsLength()
    assert assetsLength > 0


def test_interface(
    v2VaultsAdapter, introspection, management, registryAdapterCommonInterface
):
    adapterImplementsCommonInterface = introspection.implementsInterface(
        v2VaultsAdapter, registryAdapterCommonInterface
    )
    assert adapterImplementsCommonInterface


def test_asset(v2VaultsAdapter):
    v2UsdcVaultV2Address = "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9"

    # test vault data
    asset = v2VaultsAdapter.asset(v2UsdcVaultV2Address)
    assetId = asset[0]
    assetTypeId = asset[1]
    name = asset[2]
    version = asset[3]
    balance = asset[4]
    balanceUsdc = asset[5]
    assert assetId == v2UsdcVaultV2Address
    assert name == "USDC yVault"
    assert version == "0.3.0"
    assert balance > 0
    assert balanceUsdc > balance / 10 ** 18

    # Test token metadata
    token = asset[6]
    tokenId = token[0]
    tokenName = token[1]
    tokenSymbol = token[2]
    tokenDecimals = token[3]
    tokenPriceUsdc = token[4]
    tolerance = 5000000  # $5.00
    estimatedBalanceUsdc = tokenPriceUsdc * balance / 10 ** 6
    assert tokenId == usdcAddress
    assert tokenName == "USD Coin"
    assert tokenSymbol == "USDC"
    assert tokenDecimals == 6
    assert tokenPriceUsdc > 900000
    assert tokenPriceUsdc < 1100000
    assert estimatedBalanceUsdc >= balanceUsdc - tolerance
    assert estimatedBalanceUsdc <= balanceUsdc + tolerance


def test_asset_metadata(v2VaultsAdapter):
    # Test vault metadata
    v2UsdcVaultV1Address = "0xe2F6b9773BF3A015E2aA70741Bde1498bdB9425b"
    asset = v2VaultsAdapter.asset(v2UsdcVaultV1Address)
    metadata = asset[7]
    symbol = metadata[0]
    pricePerShare = metadata[1]
    migrationAvailable = metadata[2]
    latestVaultAddress = metadata[3]
    depositLimit = metadata[4]
    emergencyShutdown = metadata[5]
    assert migrationAvailable == True
    assert latestVaultAddress != v2UsdcVaultV1Address
    assert latestVaultAddress != ZERO_ADDRESS
    assert depositLimit > 0
    assert emergencyShutdown == False


def test_asset_tvl(v2VaultsAdapter):
    assetsAddresses = v2VaultsAdapter.assetsAddresses()
    for address in assetsAddresses:
        tvl = v2VaultsAdapter.assetTvl(address) / 10 ** 12
        assert tvl > 0

    # Print TVL per asset
    # print("-------------")
    # print("V2 Vaults TVL")
    # print("-------------")
    # assetsAddresses = v2VaultsAdapter.assetsAddresses()
    # tvlList = []
    # for address in assetsAddresses:
    #     token = interface.IERC20(address)
    #     tvl = v2VaultsAdapter.assetTvl(address) / 10 ** 6
    #     tvlList.append({"symbol": token.symbol(), "tvl": tvl})
    # sortedTvlItems = sorted(tvlList, key=itemgetter("tvl"), reverse=True)
    # for item in sortedTvlItems:
    #     print(item.get("symbol"), item.get("tvl"))


def test_assets_tvl(v2VaultsAdapter):
    tvl = v2VaultsAdapter.assetsTvl()
    assert tvl > 0
    # print("Total tvl", tvl / 10 ** 12)


def test_tokens(v2VaultsAdapter):
    tokens = v2VaultsAdapter.tokens()
    assetsLength = v2VaultsAdapter.assetsLength()
    tokensLength = len(tokens)
    assert tokensLength > 0
    assert tokensLength < assetsLength


def test_assets(v2VaultsAdapter):
    assets = v2VaultsAdapter.assets()
    assert len(assets) > 0
    firstAsset = assets[0]
    assetId = firstAsset[0]
    assetTypeId = firstAsset[1]
    assetName = firstAsset[2]
    assetVersion = firstAsset[3]
    assert assetId == yfiVaultAddress
    assert assetName == "YFI yVault"
    assert assetTypeId == "v2Vault"
    assert assetVersion == "0.3.2"
    # print(assets)


def test_position_of(v2VaultsAdapter, management, accounts):
    # Deposit into YFI vault
    v2YfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
    vestedYfiAddress = "0x42A28ADDC15E627d19e780c89043b4B1d3629D34"
    yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
    trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
    zapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"
    yfiAccount = accounts.at(vestedYfiAddress, force=True)
    yfi = interface.IERC20(yfiAddress)
    yfi.approve(v2YfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
    yfiVault = interface.V2Vault(v2YfiVaultAddress)
    yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
    yfiVault.approve(trustedMigratorAddress, 100, {"from": vestedYfiAddress})
    userVaultBalance = yfiVault.balanceOf(vestedYfiAddress)
    assert userVaultBalance > 0

    # Test position
    position = v2VaultsAdapter.positionOf(vestedYfiAddress, v2YfiVaultAddress)
    assetId = position[0]
    balance = position[1]
    balanceUsdc = position[2]
    assert assetId == v2YfiVaultAddress
    assert balance == userVaultBalance
    assert balanceUsdc > balance / 10 ** 18

    # Test token position
    tokenPosition = position[3]
    tokenAddress = tokenPosition[0]
    tokenBalance = tokenPosition[1]
    tokenBalanceUsdc = tokenPosition[2]
    assert tokenAddress == yfiAddress
    assert tokenBalance > 0
    assert tokenBalanceUsdc > tokenBalance / 10 ** 18

    # Test token allowances
    tokenAllowances = tokenPosition[3]
    owner = tokenAllowances[0][0]
    spender = tokenAllowances[0][1]
    allowance = tokenAllowances[0][2]
    assert owner == vestedYfiAddress
    assert spender == v2YfiVaultAddress
    assert allowance > 0

    # Position allowances
    positionAllowances = position[4]
    owner = positionAllowances[0][0]
    spender = positionAllowances[0][1]
    allowance = positionAllowances[0][2]
    assert owner == vestedYfiAddress
    assert spender == trustedMigratorAddress
    assert allowance == 100


def test_positions_of(v2VaultsAdapter, accounts):
    # Deposit into YFI vault
    v2YfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
    vestedYfiAddress = "0x42A28ADDC15E627d19e780c89043b4B1d3629D34"
    yfiAccount = accounts.at(vestedYfiAddress, force=True)
    yfi = interface.IERC20(yfiAddress)
    yfi.approve(v2YfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
    yfiVault = interface.V2Vault(v2YfiVaultAddress)
    yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
    userVaultBalance = yfiVault.balanceOf(vestedYfiAddress)
    assert userVaultBalance > 0

    # Test positions
    positions = v2VaultsAdapter.positionsOf(vestedYfiAddress)
    position = positions[0]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == v2YfiVaultAddress
