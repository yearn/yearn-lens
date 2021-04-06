import pytest
import brownie
from brownie import interface, ZERO_ADDRESS
from operator import itemgetter

yfiVaultAddress = "0xBA2E7Fed597fd0E3e70f5130BcDbbFE06bB94fe1"
yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
usdcVaultAddress = "0x597ad1e0c13bfe8025993d9e79c69e1c0233522e"
v1UsdcVaultV1Address = "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9"
ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"
vestedYfiAddress = "0x42A28ADDC15E627d19e780c89043b4B1d3629D34"
trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
zapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"


@pytest.fixture
def v1VaultsAdapter(RegisteryAdapterV1Vault, managementList, oracle, management):
    v1RegistryAddress = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0"
    trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
    positionSpenderAddresses = [trustedMigratorAddress]
    adapter = RegisteryAdapterV1Vault.deploy(
        v1RegistryAddress, oracle, managementList, {"from": management},
    )
    adapter.setPositionSpenderAddresses(positionSpenderAddresses, {"from": management})
    return adapter


def test_interface(
    v1VaultsAdapter, introspection, management, registryAdapterCommonInterface
):
    adapterImplementsCommonInterface = introspection.implementsInterface(
        v1VaultsAdapter, registryAdapterCommonInterface
    )
    assert adapterImplementsCommonInterface


def test_adapter_info(v1VaultsAdapter):
    adapterInfo = v1VaultsAdapter.adapterInfo()
    assert adapterInfo[0] == v1VaultsAdapter
    assert adapterInfo[1] == "v1Vault"
    assert adapterInfo[2] == "vault"


def test_registry_address(v1VaultsAdapter):
    assert not v1VaultsAdapter.registryAddress() == ZERO_ADDRESS


def test_assets_length(v1VaultsAdapter):
    assetsLength = v1VaultsAdapter.assetsLength()
    assert assetsLength > 0


def test_assets_addresses(v1VaultsAdapter):
    assetsAddresses = v1VaultsAdapter.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_asset(v1VaultsAdapter):
    # test vault data
    asset = v1VaultsAdapter.asset(usdcVaultAddress)
    assetId = asset[0]
    assetTypeId = asset[1]
    name = asset[2]
    version = asset[3]
    balance = asset[4]
    balanceUsdc = asset[5]
    assert assetId == usdcVaultAddress
    assert name == "yearn USD//C"
    assert version == "1.0.0"
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


def test_asset_metadata(v1VaultsAdapter):
    # Test vault metadata
    asset = v1VaultsAdapter.asset(usdcVaultAddress)
    metadata = asset[7]
    symbol = metadata[0]
    pricePerShare = metadata[1]
    migrationAvailable = metadata[2]
    latestVaultAddress = metadata[3]
    depositLimit = metadata[4]
    emergencyShutdown = metadata[5]
    assert migrationAvailable == True
    assert latestVaultAddress != usdcVaultAddress
    assert latestVaultAddress != ZERO_ADDRESS
    assert depositLimit > 0
    assert emergencyShutdown == False


def test_assets(v1VaultsAdapter):
    assets = v1VaultsAdapter.assets()
    assert len(assets) > 1
    usdcVault = assets[2]
    assetId = usdcVault[0]
    assetTypeId = usdcVault[1]
    assetName = usdcVault[2]
    assetVersion = usdcVault[3]
    assert assetId == usdcVaultAddress
    assert assetName == "yearn USD//C"
    assert assetTypeId == "v1Vault"
    assert assetVersion == "1.0.0"
    print(assets)


def test_position_of(v1VaultsAdapter, management, accounts):
    # Deposit into YFI vault
    yfiAccount = accounts.at(vestedYfiAddress, force=True)
    yfi = interface.IERC20(yfiAddress)
    yfi.approve(yfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
    yfiVault = interface.V1Vault(yfiVaultAddress)
    yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
    yfiVault.approve(trustedMigratorAddress, 100, {"from": vestedYfiAddress})
    pricePerShare = yfiVault.getPricePerFullShare()
    decimals = yfiVault.decimals()
    userVaultBalance = (
        yfiVault.balanceOf(vestedYfiAddress) * pricePerShare / 10 ** decimals
    )
    assert userVaultBalance > 0

    # Test position
    position = v1VaultsAdapter.positionOf(vestedYfiAddress, yfiVaultAddress)
    assetId = position[0]
    categoryId = position[1]
    balance = position[2]
    balanceUsdc = position[3]
    assert assetId == yfiVaultAddress
    assert categoryId == "deposit"
    assert userVaultBalance >= balance - 100
    assert userVaultBalance <= balance + 100
    assert balanceUsdc > balance / 10 ** 18

    # Test token position
    tokenPosition = position[4]
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
    assert spender == yfiVaultAddress
    assert allowance > 0

    # Position allowances
    positionAllowances = position[5]
    owner = positionAllowances[0][0]
    spender = positionAllowances[0][1]
    allowance = positionAllowances[0][2]
    assert owner == vestedYfiAddress
    assert spender == trustedMigratorAddress
    assert allowance == 100


def test_positions_of(v1VaultsAdapter, accounts):
    # Deposit into YFI vault
    yfiAccount = accounts.at(vestedYfiAddress, force=True)
    yfi = interface.IERC20(yfiAddress)
    yfi.approve(yfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
    yfiVault = interface.V1Vault(yfiVaultAddress)
    yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
    pricePerShare = yfiVault.getPricePerFullShare()
    decimals = yfiVault.decimals()
    userVaultBalance = (
        yfiVault.balanceOf(vestedYfiAddress) * pricePerShare / 10 ** decimals
    )
    assert userVaultBalance > 0

    # Test positionsOf(address)
    positions = v1VaultsAdapter.positionsOf(vestedYfiAddress)
    position = positions[0]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == yfiVaultAddress

    # Test positionsOf(address, [...address])
    positions = v1VaultsAdapter.positionsOf(
        vestedYfiAddress, [yfiVaultAddress, v1UsdcVaultV1Address]
    )
    position = positions[0]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == yfiVaultAddress


def test_asset_tvl(v1VaultsAdapter, oracle):
    assetsAddresses = v1VaultsAdapter.assetsAddresses()
    # for address in assetsAddresses:
    #     tvl = v1VaultsAdapter.assetTvl(address) / 10 ** 12
    #     assert tvl > 0
    print(
        "token: ",
        v1VaultsAdapter.underlyingTokenAddress(
            "0x98B058b2CBacF5E99bC7012DF757ea7CFEbd35BC"
        ),
    )
    print(
        "price: ",
        oracle.getPriceUsdcRecommended(
            v1VaultsAdapter.underlyingTokenAddress(
                "0x98B058b2CBacF5E99bC7012DF757ea7CFEbd35BC"
            )
        ),
    )
    print(
        "tvl: ", v1VaultsAdapter.assetTvl("0x98B058b2CBacF5E99bC7012DF757ea7CFEbd35BC")
    )

    # Print TVL per asset
    print("-------------")
    print("V1 Vaults TVL")
    print("-------------")
    assetsAddresses = v1VaultsAdapter.assetsAddresses()
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        tvl = v1VaultsAdapter.assetTvl(address) / 10 ** 6
        tvlList.append({"symbol": token.symbol(), "tvl": tvl})
    sortedTvlItems = sorted(tvlList, key=itemgetter("tvl"), reverse=True)
    for item in sortedTvlItems:
        print(item.get("symbol"), item.get("tvl"))


def test_assets_tvl(v1VaultsAdapter):
    tvl = v1VaultsAdapter.assetsTvl()
    assert tvl > 0
    print("Total tvl", tvl / 10 ** 12)


def test_set_position_spender_addresses(v1VaultsAdapter, management, rando):
    with brownie.reverts():
        v1VaultsAdapter.setPositionSpenderAddresses([ethZapAddress], {"from": rando})
    v1VaultsAdapter.setPositionSpenderAddresses([ethZapAddress], {"from": management})
    assert v1VaultsAdapter.positionSpenderAddresses(0) == ethZapAddress
