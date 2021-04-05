import pytest
import brownie
from brownie import interface, ZERO_ADDRESS
from operator import itemgetter

yDaiV3Address = "0xC2cB1040220768554cf699b0d863A3cd4324ce32"
yDaiV2Address = "0x16de59092dAE5CcF4A1E6439D611fd0653f0Bd01"
daiAddress = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
daiWhaleAddress = "0x19D3364A399d251E894aC732651be8B0E4e85001"  # DAI vault
trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"


def test_interface(
    earnAdapter, introspection, management, registryAdapterCommonInterface
):
    adapterImplementsCommonInterface = introspection.implementsInterface(
        earnAdapter, registryAdapterCommonInterface
    )
    assert adapterImplementsCommonInterface


def test_adapter_info(earnAdapter):
    adapterInfo = earnAdapter.adapterInfo()
    assert adapterInfo[0] == earnAdapter
    assert adapterInfo[1] == "earn"
    assert adapterInfo[2] == "safe"


def test_registry_address(earnAdapter):
    assert not earnAdapter.registryAddress() == ZERO_ADDRESS


def test_assets_length(earnAdapter):
    assert earnAdapter.assetsLength() > 0


def test_assets_addresses(earnAdapter):
    assetsAddresses = earnAdapter.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_asset(earnAdapter):
    # test earn data
    asset = earnAdapter.asset(yDaiV3Address)
    assetId = asset[0]
    assetTypeId = asset[1]
    name = asset[2]
    version = asset[3]
    balance = asset[4]
    balanceUsdc = asset[5]

    assert assetId == yDaiV3Address
    assert name == "iearn DAI"
    assert version == "2.0.0"
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
    estimatedBalanceUsdc = tokenPriceUsdc * balance / 10 ** tokenDecimals
    assert tokenId == daiAddress
    assert tokenName == "Dai Stablecoin"
    assert tokenSymbol == "DAI"
    assert tokenDecimals == 18
    assert tokenPriceUsdc > 900000
    assert tokenPriceUsdc < 1100000
    assert estimatedBalanceUsdc >= balanceUsdc - tolerance
    assert estimatedBalanceUsdc <= balanceUsdc + tolerance

    # Test asset metadata
    metadata = asset[7]
    pricePerShare = metadata[0]
    assert pricePerShare > 1 * 10 ** 18


def test_assets(earnAdapter):
    assets = earnAdapter.assets()
    assert len(assets) > 1
    firstAsset = assets[0]
    assetId = firstAsset[0]
    assetTypeId = firstAsset[1]
    assetName = firstAsset[2]
    assetVersion = firstAsset[3]
    assert assetId == yDaiV2Address
    assert assetName == "iearn DAI"
    assert assetTypeId == "earn"
    assert assetVersion == "2.0.0"


def test_position_of(earnAdapter, management, accounts):
    # Deposit into YFI vault
    daiWhale = accounts.at(daiWhaleAddress, force=True)
    dai = interface.IERC20(daiAddress)
    dai.approve(yDaiV3Address, 2 ** 256 - 1, {"from": daiWhaleAddress})
    daiSafe = interface.IEarnToken(yDaiV3Address)
    daiSafe.deposit(1 * 10 ** 18, {"from": daiWhale})
    daiSafe.approve(trustedMigratorAddress, 100, {"from": daiWhaleAddress})
    userSafeBalance = daiSafe.balanceOf(daiWhaleAddress)
    assert userSafeBalance > 0

    # Test position
    position = earnAdapter.positionOf(daiWhaleAddress, yDaiV3Address)
    assetId = position[0]
    categoryId = position[1]
    balance = position[2]
    balanceUsdc = position[2]
    assert assetId == yDaiV3Address
    assert categoryId == "deposit"
    assert balance == userSafeBalance
    assert balanceUsdc > balance / 10 ** 18

    # Test token position
    tokenPosition = position[4]
    tokenAddress = tokenPosition[0]
    tokenBalance = tokenPosition[1]
    tokenBalanceUsdc = tokenPosition[2]
    assert tokenAddress == daiAddress
    assert tokenBalance > 0
    assert tokenBalanceUsdc > tokenBalance / 10 ** 18

    # Test token allowances
    tokenAllowances = tokenPosition[3]
    owner = tokenAllowances[0][0]
    spender = tokenAllowances[0][1]
    allowance = tokenAllowances[0][2]
    assert owner == daiWhaleAddress
    assert spender == yDaiV3Address
    assert allowance > 0

    # Position allowances
    positionAllowances = position[5]
    owner = positionAllowances[0][0]
    spender = positionAllowances[0][1]
    allowance = positionAllowances[0][2]
    assert owner == daiWhaleAddress
    assert spender == trustedMigratorAddress
    assert allowance == 100


def test_positions_of(earnAdapter, accounts):
    # Deposit into YFI vault
    daiWhale = accounts.at(daiWhaleAddress, force=True)
    dai = interface.IERC20(daiAddress)
    dai.approve(yDaiV2Address, 2 ** 256 - 1, {"from": daiWhaleAddress})
    daiSafe = interface.IEarnToken(yDaiV2Address)
    daiSafe.deposit(1 * 10 ** 18, {"from": daiWhale})
    userSafeBalance = daiSafe.balanceOf(daiWhaleAddress)
    assert userSafeBalance > 0

    # Test positions
    positions = earnAdapter.positionsOf(daiWhaleAddress)
    position = positions[0]
    assetId = position[0]
    balance = position[1]
    assert len(positions) > 1
    assert assetId == yDaiV2Address
    assert balance == userSafeBalance


def test_asset_tvl(earnAdapter):
    assetsAddresses = earnAdapter.assetsAddresses()
    for address in assetsAddresses:
        tvl = earnAdapter.assetTvl(address) / 10 ** 12
        assert tvl > 0

    # # Print TVL per asset
    # print("--------")
    # print("Earn TVL")
    # print("--------")
    # tvlList = []
    # for address in assetsAddresses:
    #     token = interface.IERC20(address)
    #     tvl = earnAdapter.assetTvl(address) / 10 ** 6
    #     tvlList.append({"symbol": token.symbol(), "tvl": tvl})
    # sortedTvlItems = sorted(tvlList, key=itemgetter("tvl"), reverse=True)
    # for item in sortedTvlItems:
    #     print(item.get("symbol"), item.get("tvl"))


def test_assets_tvl(earnAdapter):
    tvl = earnAdapter.assetsTvl()
    assert tvl > 0
    # print("Total tvl", tvl / 10 ** 12)


def test_set_position_spender_addresses(earnAdapter, management, rando):
    with brownie.reverts():
        earnAdapter.setPositionSpenderAddresses([ethZapAddress], {"from": rando})
    earnAdapter.setPositionSpenderAddresses([ethZapAddress], {"from": management})
    assert earnAdapter.positionSpenderAddresses(0) == ethZapAddress

