import pytest
import brownie

from ..addresses import *
from brownie import interface, ZERO_ADDRESS
from operator import itemgetter


def test_generator_info(v2VaultsTvlAdapter):
    adapterInfo = v2VaultsTvlAdapter.adapterInfo()
    assert adapterInfo[0] == v2VaultsTvlAdapter
    assert adapterInfo[1] == "VAULT_V2"
    assert adapterInfo[2] == "VAULT"


def test_asset_tvl_usdc(v2VaultsTvlAdapter):
    assetsAddresses = v2VaultsTvlAdapter.assetsAddresses()
    # for address in assetsAddresses:
    #     tvl = v2VaultsTvlAdapter.assetTvlUsdc(address) / 10 ** 12
    #     assert tvl > 0

    # Print TVL per asset
    print("-------------")
    print("V2 Vaults TVL")
    print("-------------")
    totalTvl = 0
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        tvl = v2VaultsTvlAdapter.assetTvlUsdc(address) / 10 ** 6
        totalTvl += tvl
        tvlList.append({"symbol": token.symbol(), "tvl": tvl})
    sortedTvlItems = sorted(tvlList, key=itemgetter("tvl"), reverse=True)
    for item in sortedTvlItems:
        print(item.get("symbol"), item.get("tvl"))

    calculatedTotalTvl = v2VaultsTvlAdapter.assetsTvlUsdc() / 10 ** 6
    assert round(calculatedTotalTvl) == round(totalTvl)
    print("Total tvl", totalTvl)


def test_asset_tvl(v2VaultsTvlAdapter):
    assetsAddresses = v2VaultsTvlAdapter.assetsAddresses()
    # for address in assetsAddresses:
    #     tvl = v2VaultsTvlAdapter.assetTvlUsdc(address) / 10 ** 12
    #     assert tvl > 0

    # Print TVL per asset
    print("-------------")
    print("V2 Vaults TVL")
    print("-------------")
    totalTvl = 0
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        print("address", address)
        print(v2VaultsTvlAdapter.assetTvlBreakdown(address))
        print("")


def test_assets_tvl(v2VaultsTvlAdapter):
    tvl = v2VaultsTvlAdapter.assetsTvlBreakdown()
    print(tvl)
