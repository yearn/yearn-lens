import pytest
import brownie
from brownie import interface, ZERO_ADDRESS
from operator import itemgetter

cyDaiAddress = "0x8e595470Ed749b85C6F7669de83EAe304C2ec68F"
ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"


# @pytest.fixture
# def ironBankTvlAdapter(
#     TvlAdapterIronBank,
#     ironBankAddressesGenerator,
#     delegationMapping,
#     managementList,
#     oracle,
#     management,
# ):
#     return TvlAdapterIronBank.deploy(
#         oracle, ironBankAddressesGenerator, delegationMapping, {"from": management},
#     )


def test_generator_info(ironBankTvlAdapter):
    adapterInfo = ironBankTvlAdapter.adapterInfo()
    assert adapterInfo[0] == ironBankTvlAdapter
    assert adapterInfo[1] == "IRON_BANK_MARKET"
    assert adapterInfo[2] == "LENDING"


def test_asset_tvl_usdc(
    ironBankTvlAdapter, ironBankAddressesGenerator, delegationMapping, management
):
    # delegationMapping.updateDelegationStatusForAsset(
    #     cyDaiAddress, True, {"from": management}
    # )
    # ironBankAddressesGenerator.setAssetDeprecated(
    #     cyDaiAddress, True, {"From": management}
    # )
    assetsAddresses = ironBankTvlAdapter.assetsAddresses()
    # for address in assetsAddresses:
    #     tvl = v2VaultsTvlAdapter.assetTvlUsdc(address) / 10 ** 12
    #     assert tvl > 0

    # Print TVL per asset

    print("-------------")
    print("Iron Bank TVL")
    print("-------------")
    totalTvl = 0
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        tvl = ironBankTvlAdapter.assetTvlUsdc(address) / 10 ** 6
        totalTvl += tvl
        tvlList.append({"symbol": token.symbol(), "tvl": tvl})
    sortedTvlItems = sorted(tvlList, key=itemgetter("tvl"), reverse=True)
    for item in sortedTvlItems:
        print(item.get("symbol"), item.get("tvl"))

    calculatedTotalTvl = ironBankTvlAdapter.assetsTvlUsdc() / 10 ** 6
    assert round(calculatedTotalTvl) == round(totalTvl)
    print("Total tvl", totalTvl)


def test_asset_tvl(ironBankTvlAdapter, delegationMapping, management):
    delegationMapping.updateDelegationStatusForAsset(
        cyDaiAddress, True, {"from": management}
    )
    assetsAddresses = ironBankTvlAdapter.assetsAddresses()
    # for address in assetsAddresses:
    #     tvl = ironBankTvlAdapter.assetTvlUsdc(address) / 10 ** 12
    #     assert tvl > 0

    # Print TVL per asset
    print("-----------------")
    print("Iron Bank Markets")
    print("-----------------")
    totalTvl = 0
    tvlList = []
    for address in assetsAddresses:
        token = interface.IERC20(address)
        print("address", address)
        print(ironBankTvlAdapter.assetTvlBreakdown(address))
        print("")


def test_assets_tvl(ironBankTvlAdapter):
    tvl = ironBankTvlAdapter.assetsTvlBreakdown()
    print(tvl)
