import pytest
import brownie
from brownie import interface, ZERO_ADDRESS
from operator import itemgetter

yfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
v2UsdcVaultV1Address = "0xe2F6b9773BF3A015E2aA70741Bde1498bdB9425b"
v2UsdcVaultV2Address = "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9"
ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"
v2YfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
vestedYfiAddress = "0x42A28ADDC15E627d19e780c89043b4B1d3629D34"
yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
zapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"


@pytest.fixture
def v2VaultsAdapter(
    RegisteryAdapterV2Vault, managementList, oracle, helper, management
):
    v2RegistryAddress = "0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804"
    trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
    positionSpenderAddresses = [trustedMigratorAddress]
    adapter = RegisteryAdapterV2Vault.deploy(
        v2RegistryAddress, oracle, managementList, helper, {"from": management},
    )
    adapter.setPositionSpenderAddresses(positionSpenderAddresses, {"from": management})
    return adapter


def test_interface(
    v2VaultsAdapter, introspection, management, registryAdapterCommonInterface
):
    adapterImplementsCommonInterface = introspection.implementsInterface(
        v2VaultsAdapter, registryAdapterCommonInterface
    )
    assert adapterImplementsCommonInterface


def test_adapter_info(v2VaultsAdapter):
    adapterInfo = v2VaultsAdapter.adapterInfo()
    assert adapterInfo[0] == v2VaultsAdapter
    assert adapterInfo[1] == "VAULT_V2"
    assert adapterInfo[2] == "VAULT"


def test_registry_address(v2VaultsAdapter):
    assert not v2VaultsAdapter.registry() == ZERO_ADDRESS


def test_assets_length(v2VaultsAdapter):
    assetsLength = v2VaultsAdapter.assetsLength()
    assert assetsLength > 0


def test_set_asset_deprecated(v2VaultsAdapter, management):
    originalAssetsLength = v2VaultsAdapter.assetsLength()
    assert originalAssetsLength > 0
    v2VaultsAdapter.setAssetDeprecated(v2YfiVaultAddress, True, {"from": management})
    newAssetsLength = v2VaultsAdapter.assetsLength()
    v2VaultsAdapter.assetDeprecated(v2YfiVaultAddress) == True
    assert newAssetsLength == originalAssetsLength - 1
    v2VaultsAdapter.setAssetDeprecated(v2YfiVaultAddress, False, {"from": management})
    newAssetsLength = v2VaultsAdapter.assetsLength()
    assert newAssetsLength == originalAssetsLength
    v2VaultsAdapter.assetDeprecated(v2YfiVaultAddress) == False


def test_assets_addresses(v2VaultsAdapter):
    assetsAddresses = v2VaultsAdapter.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_asset_static(v2VaultsAdapter):
    # test vault data
    assetStatic = v2VaultsAdapter.assetStatic(v2UsdcVaultV2Address)
    assetId = assetStatic[0]
    assetTypeId = assetStatic[1]
    name = assetStatic[2]
    version = assetStatic[3]
    assert assetId == v2UsdcVaultV2Address
    assert name == "USDC yVault"
    assert version == "0.3.0"

    # # Test token
    token = assetStatic[4]
    tokenId = token[0]
    tokenName = token[1]
    tokenSymbol = token[2]
    tokenDecimals = token[3]

    assert tokenId == usdcAddress
    assert tokenName == "USD Coin"
    assert tokenSymbol == "USDC"
    assert tokenDecimals == 6


def test_asset_dynamic(v2VaultsAdapter, oracle):
    assetDynamic = v2VaultsAdapter.assetDynamic(v2UsdcVaultV1Address)
    assetId = assetDynamic[0]
    typeId = assetDynamic[1]
    tokenId = assetDynamic[2]
    underlyingTokenBalance = assetDynamic[3]
    delegatedBalance = assetDynamic[4]
    metadata = assetDynamic[5]

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
    # assert balanceUsdc > balance / 10 ** 6 # This assumes the price of USDC >= 1

    # Test vault metadata
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


def test_assets_static(v2VaultsAdapter):
    assets = v2VaultsAdapter.assetsStatic()
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


def test_assets_dynamic(v2VaultsAdapter):
    assets = v2VaultsAdapter.assetsStatic()
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


def test_position_of(v2VaultsAdapter, oracle, management, accounts):
    # Deposit into YFI vault
    yfiAccount = accounts.at(vestedYfiAddress, force=True)
    yfi = interface.IERC20(yfiAddress)
    yfi.approve(v2YfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
    yfiVault = interface.IV2Vault(v2YfiVaultAddress)
    yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
    yfiVault.approve(trustedMigratorAddress, 100, {"from": vestedYfiAddress})
    pricePerShare = yfiVault.pricePerShare()
    decimals = yfiVault.decimals()
    userVaultBalanceShares = yfiVault.balanceOf(vestedYfiAddress)
    userVaultBalance = userVaultBalanceShares * pricePerShare / 10 ** decimals
    userVaultBalanceUsdc = oracle.getNormalizedValueUsdc(yfiAddress, userVaultBalance)
    assert userVaultBalanceShares > 0
    position = v2VaultsAdapter.positionOf(vestedYfiAddress, v2YfiVaultAddress)

    # Test basic info
    assetId = position[0]
    tokenId = position[1]
    typeId = position[2]
    balance = position[3]
    assert assetId == v2YfiVaultAddress
    assert tokenId == yfiAddress
    assert typeId == "deposit"
    assert balance == userVaultBalanceShares

    # Test account asset balance
    underlyingTokenBalance = position[4]
    underlyingTokenBalanceAmount = underlyingTokenBalance[0]
    underlyingTokenBalanceAmountUsdc = underlyingTokenBalance[1]
    assert userVaultBalanceUsdc >= underlyingTokenBalanceAmountUsdc - 100
    assert userVaultBalanceUsdc <= underlyingTokenBalanceAmountUsdc + 100
    assert underlyingTokenBalanceAmountUsdc > underlyingTokenBalanceAmount / 10 ** 18

    # Test account token balance
    accountTokenBalance = position[5]
    accountTokenBalanceAmount = accountTokenBalance[0]
    accountTokenBalanceAmountUsdc = accountTokenBalance[1]
    assert accountTokenBalanceAmount == yfi.balanceOf(vestedYfiAddress)
    assert accountTokenBalanceAmountUsdc == oracle.getNormalizedValueUsdc(
        yfiAddress, accountTokenBalanceAmount
    )

    # Test token allowances
    tokenAllowances = position[6]
    owner = tokenAllowances[0][0]
    spender = tokenAllowances[0][1]
    allowance = tokenAllowances[0][2]
    assert owner == vestedYfiAddress
    assert spender == v2YfiVaultAddress
    assert allowance > 0

    # Position allowances
    positionAllowances = position[7]
    owner = positionAllowances[0][0]
    spender = positionAllowances[0][1]
    allowance = positionAllowances[0][2]
    assert owner == vestedYfiAddress
    assert spender == trustedMigratorAddress
    assert allowance == 100


def test_positions_of(v2VaultsAdapter, oracle, accounts):
    # Deposit into YFI vault
    yfiAccount = accounts.at(vestedYfiAddress, force=True)
    yfi = interface.IERC20(yfiAddress)
    yfi.approve(v2YfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
    yfiVault = interface.IV2Vault(v2YfiVaultAddress)
    yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
    yfiVault.approve(trustedMigratorAddress, 100, {"from": vestedYfiAddress})
    pricePerShare = yfiVault.pricePerShare()
    decimals = yfiVault.decimals()
    userVaultBalanceShares = yfiVault.balanceOf(vestedYfiAddress)
    userVaultBalance = userVaultBalanceShares * pricePerShare / 10 ** decimals
    userVaultBalanceUsdc = oracle.getNormalizedValueUsdc(yfiAddress, userVaultBalance)
    assert userVaultBalanceShares > 0

    # Test positionsOf(address)
    positions = v2VaultsAdapter.positionsOf(vestedYfiAddress)
    position = positions[0]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == v2YfiVaultAddress

    # Test positionsOf(address, [...address])
    positions = v2VaultsAdapter.positionsOf(
        vestedYfiAddress, [v2YfiVaultAddress, v2UsdcVaultV2Address]
    )
    position = positions[0]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == v2YfiVaultAddress


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


def test_set_position_spender_addresses(v2VaultsAdapter, management, rando):
    with brownie.reverts():
        v2VaultsAdapter.setPositionSpenderAddresses([ethZapAddress], {"from": rando})
    v2VaultsAdapter.setPositionSpenderAddresses([ethZapAddress], {"from": management})
    assert v2VaultsAdapter.positionSpenderAddresses(0) == ethZapAddress
