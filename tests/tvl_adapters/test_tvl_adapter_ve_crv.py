import pytest
from brownie import interface
from operator import itemgetter


@pytest.fixture
def veCrvTvlAdapter(
    TvlAdapterVeCrv,
    oracle,
    management,
):
    return TvlAdapterVeCrv.deploy(
        oracle,
        {"from": management},
    )


def test_generator_info(veCrvTvlAdapter):
    adapterInfo = veCrvTvlAdapter.adapterInfo()
    assert adapterInfo[0] == veCrvTvlAdapter
    assert adapterInfo[1] == "VE_CRV"
    assert adapterInfo[2] == "SPECIAL"


def test_asset_tvl_usdc(veCrvTvlAdapter):
    assetsAddresses = veCrvTvlAdapter.assetsAddresses()
    print(
        "acab",
        veCrvTvlAdapter.underlyingTokenAddress(
            "0xD533a949740bb3306d119CC777fa900bA034cd52"
        ),
    )
    # for address in assetsAddresses:
    #     tvl = v2VaultsTvlAdapter.assetTvlUsdc(address) / 10 ** 12
    #     assert tvl > 0

    # Print TVL per asset

    print("---------")
    print("veCRV TVL")
    print("---------")
    totalTvl = 0
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        tvl = veCrvTvlAdapter.assetTvlUsdc(address) / 10**6
        totalTvl += tvl
        tvlList.append({"symbol": token.symbol(), "tvl": tvl})
    sortedTvlItems = sorted(tvlList, key=itemgetter("tvl"), reverse=True)
    for item in sortedTvlItems:
        print(item.get("symbol"), item.get("tvl"))

    calculatedTotalTvl = veCrvTvlAdapter.assetsTvlUsdc() / 10**6
    assert round(calculatedTotalTvl) == round(totalTvl)
    print("Total tvl", totalTvl)


def test_asset_tvl(veCrvTvlAdapter):
    assetsAddresses = veCrvTvlAdapter.assetsAddresses()
    # for address in assetsAddresses:
    #     tvl = veCrvTvlAdapter.assetTvlUsdc(address) / 10 ** 12
    #     assert tvl > 0
    print(veCrvTvlAdapter.assetsLength())

    # Print TVL per asset
    print("-------------------")
    print("veCRV TVL Breakdown")
    print("-------------------")
    totalTvl = 0
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        print("address", address)
        print(veCrvTvlAdapter.assetTvlBreakdown(address))
        print("")


def test_assets_tvl(veCrvTvlAdapter):
    tvl = veCrvTvlAdapter.assetsTvlBreakdown()
    print(tvl)
