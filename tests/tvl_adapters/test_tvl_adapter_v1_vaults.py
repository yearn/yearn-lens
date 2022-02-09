from operator import itemgetter

import brownie
import pytest
from brownie import ZERO_ADDRESS, interface

from ..addresses import *


def test_generator_info(v1VaultTvlAdapter):
    adapterInfo = v1VaultTvlAdapter.adapterInfo()
    assert adapterInfo[0] == v1VaultTvlAdapter
    assert adapterInfo[1] == "VAULT_V1"
    assert adapterInfo[2] == "VAULT"


def test_asset_tvl_usdc(
    v1VaultTvlAdapter, v1VaultsAddressesGenerator, delegationMapping
):
    # delegationMapping.updateDelegationStatusForAsset(
    #     cyDaiAddress, True, {"from": management}
    # )
    # v1VaultsAddressesGenerator.setAssetDeprecated(
    #     cyDaiAddress, True, {"From": management}
    # )
    assetsAddresses = v1VaultTvlAdapter.assetsAddresses()
    # for address in assetsAddresses:
    #     tvl = v2VaultsTvlAdapter.assetTvlUsdc(address) / 10 ** 12
    #     assert tvl > 0

    # Print TVL per asset

    print("------------")
    print("V1 Vaults TVL")
    print("-------------")
    totalTvl = 0
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        tvl = v1VaultTvlAdapter.assetTvlUsdc(address) / 10 ** 6
        totalTvl += tvl
        tvlList.append({"symbol": token.symbol(), "tvl": tvl})
    sortedTvlItems = sorted(tvlList, key=itemgetter("tvl"), reverse=True)
    for item in sortedTvlItems:
        print(item.get("symbol"), item.get("tvl"))

    calculatedTotalTvl = v1VaultTvlAdapter.assetsTvlUsdc() / 10 ** 6
    assert round(calculatedTotalTvl) == round(totalTvl)
    print("Total tvl", totalTvl)


def test_asset_tvl(v1VaultTvlAdapter, delegationMapping):
    # delegationMapping.updateDelegationStatusForAsset(
    #     cyDaiAddress, True, {"from": management}
    # )
    assetsAddresses = v1VaultTvlAdapter.assetsAddresses()
    # for address in assetsAddresses:
    #     tvl = v1VaultTvlAdapter.assetTvlUsdc(address) / 10 ** 12
    #     assert tvl > 0

    # Print TVL per asset
    print("-----------------------")
    print("V1 Vaults TVL Breakdown")
    print("-----------------------")
    totalTvl = 0
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        print("address", address)
        print(v1VaultTvlAdapter.assetTvlBreakdown(address))
        print("")


def test_assets_tvl(v1VaultTvlAdapter):
    tvl = v1VaultTvlAdapter.assetsTvlBreakdown()
    print(tvl)
