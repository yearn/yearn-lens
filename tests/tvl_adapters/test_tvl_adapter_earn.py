import pytest

from ..addresses import *
from brownie import interface
from operator import itemgetter


@pytest.fixture
def earnTvlAdapter(
    TvlAdapterEarn,
    earnAddressesGenerator,
    delegationMapping,
    oracle,
    management,
):
    return TvlAdapterEarn.deploy(
        oracle,
        earnAddressesGenerator,
        delegationMapping,
        {"from": management},
    )


def test_generator_info(earnTvlAdapter):
    adapterInfo = earnTvlAdapter.adapterInfo()
    assert adapterInfo[0] == earnTvlAdapter
    assert adapterInfo[1] == "EARN"
    assert adapterInfo[2] == "SAFE"


def test_asset_tvl_usdc(earnTvlAdapter, earnAddressesGenerator, delegationMapping):
    # delegationMapping.updateDelegationStatusForAsset(
    #     cyDaiAddress, True, {"from": management}
    # )
    # earnAddressesGenerator.setAssetDeprecated(
    #     cyDaiAddress, True, {"From": management}
    # )
    assetsAddresses = earnTvlAdapter.assetsAddresses()
    # for address in assetsAddresses:
    #     tvl = v2VaultsTvlAdapter.assetTvlUsdc(address) / 10 ** 12
    #     assert tvl > 0

    # Print TVL per asset

    print("--------")
    print("Earn TVL")
    print("--------")
    totalTvl = 0
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        tvl = earnTvlAdapter.assetTvlUsdc(address) / 10**6
        totalTvl += tvl
        tvlList.append({"symbol": token.symbol(), "tvl": tvl})
    sortedTvlItems = sorted(tvlList, key=itemgetter("tvl"), reverse=True)
    for item in sortedTvlItems:
        print(item.get("symbol"), item.get("tvl"))

    calculatedTotalTvl = earnTvlAdapter.assetsTvlUsdc() / 10**6
    assert round(calculatedTotalTvl) == round(totalTvl)
    print("Total tvl", totalTvl)


def test_asset_tvl(earnTvlAdapter, delegationMapping):
    # delegationMapping.updateDelegationStatusForAsset(
    #     cyDaiAddress, True, {"from": management}
    # )
    assetsAddresses = earnTvlAdapter.assetsAddresses()
    # for address in assetsAddresses:
    #     tvl = earnAdapter.assetTvlUsdc(address) / 10 ** 12
    #     assert tvl > 0

    # Print TVL per asset
    print("------------------")
    print("Earn TVL Breakdown")
    print("------------------")
    totalTvl = 0
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        print("address", address)
        print(earnTvlAdapter.assetTvlBreakdown(address))
        print("")


def test_assets_tvl(earnTvlAdapter):
    tvl = earnTvlAdapter.assetsTvlBreakdown()
    print(tvl)
