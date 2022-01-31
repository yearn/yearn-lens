import pytest
import brownie
from brownie import Contract, interface, ZERO_ADDRESS
from operator import itemgetter

cyDaiAddress = "0x8e595470Ed749b85C6F7669de83EAe304C2ec68F"
ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"
cyWethAddress = "0x41c84c0e2EE0b740Cf0d31F63f3B6F627DC6b393"


@pytest.fixture
def ironBankTvlAdapter(
    TvlAdapterIronBank,
    ironBankAddressesGenerator,
    delegationMapping,
    managementList,
    oracle,
    management,
):
    return TvlAdapterIronBank.deploy(
        oracle, ironBankAddressesGenerator, delegationMapping, {
            "from": management},
    )


def test_generator_info(ironBankTvlAdapter):
    adapterInfo = ironBankTvlAdapter.adapterInfo()
    assert adapterInfo[0] == ironBankTvlAdapter
    assert adapterInfo[1] == "IRON_BANK_MARKET"
    assert adapterInfo[2] == "LENDING"


def test_asset_tvl_breakdown(ironBankTvlAdapter, oracle):
    cyDaiToken = Contract(cyDaiAddress)
    tokenAddress = ironBankTvlAdapter.underlyingTokenAddress(cyDaiAddress)
    underlyingTokenBalanceAmount = ironBankTvlAdapter.assetBalance(
        cyDaiAddress)
    delegatedBalanceAmount = ironBankTvlAdapter.assetDelegatedBalance(
        cyDaiAddress)
    cyDaiAdjustedBalance = underlyingTokenBalanceAmount - delegatedBalanceAmount
    cyDaiPriceUsdc = oracle.getPriceUsdcRecommended(tokenAddress)
    breakdown = ironBankTvlAdapter.assetTvlBreakdown(cyDaiAddress)

    cyDaiAdjustedBalanceUsdc = oracle.getNormalizedValueUsdc(
        tokenAddress, cyDaiAdjustedBalance, cyDaiPriceUsdc)

    assetId = breakdown[0]
    tokenId = breakdown[1]
    tokenPriceUsdc = breakdown[2]
    underlyingTokenBalance = breakdown[3]
    delegatedBalance = breakdown[4]
    adjustedBalance = breakdown[5]
    adjustedBalanceUsdc = breakdown[6]

    assert assetId == cyDaiAddress
    assert tokenId == tokenAddress
    assert tokenPriceUsdc == cyDaiPriceUsdc
    assert underlyingTokenBalance == underlyingTokenBalanceAmount
    assert adjustedBalance == cyDaiAdjustedBalance
    assert delegatedBalance == delegatedBalanceAmount
    assert adjustedBalanceUsdc == cyDaiAdjustedBalanceUsdc


def test_assets_tvl_breakdown(ironBankTvlAdapter, oracle):
    cyDaiUnderlyingTokenAddress = ironBankTvlAdapter.underlyingTokenAddress(
        cyDaiAddress)
    cyDaiUnderlyingTokenBalanceAmount = ironBankTvlAdapter.assetBalance(
        cyDaiAddress)
    cyDaiDelegatedBalanceAmount = ironBankTvlAdapter.assetDelegatedBalance(
        cyDaiAddress)
    cyDaiAdjustedBalance = cyDaiUnderlyingTokenBalanceAmount - cyDaiDelegatedBalanceAmount
    cyDaiPriceUsdc = oracle.getPriceUsdcRecommended(
        cyDaiUnderlyingTokenAddress)

    cyDaiAdjustedBalanceUsdc = oracle.getNormalizedValueUsdc(
        cyDaiUnderlyingTokenAddress, cyDaiAdjustedBalance, cyDaiPriceUsdc)

    cyWethUnderlyingTokenAddress = ironBankTvlAdapter.underlyingTokenAddress(
        cyWethAddress)
    cyWethUnderlyingTokenBalanceAmount = ironBankTvlAdapter.assetBalance(
        cyWethAddress)
    cyWethDelegatedBalanceAmount = ironBankTvlAdapter.assetDelegatedBalance(
        cyWethAddress)
    cyWethAdjustedBalance = cyWethUnderlyingTokenBalanceAmount - \
        cyWethDelegatedBalanceAmount
    cyWethPriceUsdc = oracle.getPriceUsdcRecommended(
        cyWethUnderlyingTokenAddress)

    cyWethAdjustedBalanceUsdc = oracle.getNormalizedValueUsdc(
        cyWethUnderlyingTokenAddress, cyWethAdjustedBalance, cyWethPriceUsdc)

    breakdown = ironBankTvlAdapter.assetsTvlBreakdown(
        [cyDaiAddress, cyWethAddress])

    cyDaiTvlBreakdown = breakdown[0]
    cyWethBreakdown = breakdown[1]

    cyDaiAssetId = cyDaiTvlBreakdown[0]
    cyDaiTokenId = cyDaiTvlBreakdown[1]
    cyDaiTokenPriceUsdc = cyDaiTvlBreakdown[2]
    cyDaiUnderlyingTokenBalance = cyDaiTvlBreakdown[3]
    cyDaiDelegatedBalance = cyDaiTvlBreakdown[4]
    cyDaAdjustedBalance = cyDaiTvlBreakdown[5]
    cyDaAdjustedBalanceUsdc = cyDaiTvlBreakdown[6]

    cyWethAssetId = cyWethBreakdown[0]
    cyWethTokenId = cyWethBreakdown[1]
    cyWethTokenPriceUsdc = cyWethBreakdown[2]
    cyWethUnderlyingTokenBalance = cyWethBreakdown[3]
    cyWethDelegatedBalance = cyWethBreakdown[4]
    cyWetAdjustedBalance = cyWethBreakdown[5]
    cyWetAdjustedBalanceUsdc = cyWethBreakdown[6]

    assert cyDaiAssetId == cyDaiAddress
    assert cyDaiTokenId == cyDaiUnderlyingTokenAddress
    assert cyDaiTokenPriceUsdc == cyDaiPriceUsdc
    assert cyDaiUnderlyingTokenBalance == cyDaiUnderlyingTokenBalanceAmount
    assert cyDaAdjustedBalance == cyDaiAdjustedBalance
    assert cyDaiDelegatedBalance == cyDaiDelegatedBalanceAmount
    assert cyDaAdjustedBalanceUsdc == cyDaiAdjustedBalanceUsdc

    assert cyWethAssetId == cyWethAddress
    assert cyWethTokenId == cyWethUnderlyingTokenAddress
    assert cyWethTokenPriceUsdc == cyWethPriceUsdc
    assert cyWethUnderlyingTokenBalance == cyWethUnderlyingTokenBalanceAmount
    assert cyWetAdjustedBalance == cyWethAdjustedBalance
    assert cyWethDelegatedBalance == cyWethDelegatedBalanceAmount
    assert cyWetAdjustedBalanceUsdc == cyWethAdjustedBalanceUsdc


def test_asset_tvl_usdc(ironBankTvlAdapter, oracle):
    tokenAddress = ironBankTvlAdapter.underlyingTokenAddress(cyDaiAddress)
    underlyingTokenBalanceAmount = ironBankTvlAdapter.assetBalance(
        cyDaiAddress)
    delegatedBalanceAmount = ironBankTvlAdapter.assetDelegatedBalance(
        cyDaiAddress)
    cyDaiAdjustedBalanceAmount = underlyingTokenBalanceAmount - delegatedBalanceAmount
    cyDaiAdjustedBalanceUsdc = oracle.getNormalizedValueUsdc(
        tokenAddress, cyDaiAdjustedBalanceAmount)

    cyDaiTvlUsdc = ironBankTvlAdapter.assetTvlUsdc(cyDaiAddress)

    assert cyDaiTvlUsdc == cyDaiAdjustedBalanceUsdc


# def test_assets_tvl_usdc(ironBankTvlAdapter, oracle):
#     cyDaiTokenAddress = ironBankTvlAdapter.underlyingTokenAddress(cyDaiAddress)
#     cyDaiUnderlyingTokenBalanceAmount = ironBankTvlAdapter.assetBalance(
#         cyDaiAddress)
#     delegatedBalanceAmount = ironBankTvlAdapter.assetDelegatedBalance(
#         cyDaiAddress)
#     cyDaiAdjustedBalanceAmount = cyDaiUnderlyingTokenBalanceAmount - delegatedBalanceAmount
#     cyDaiAdjustedBalanceUsdc = oracle.getNormalizedValueUsdc(
#         cyDaiTokenAddress, cyDaiAdjustedBalanceAmount)

#     cyWethTokenAddress = ironBankTvlAdapter.underlyingTokenAddress(
#         cyDaiAddress)
#     cyWethUnderlyingTokenBalanceAmount = ironBankTvlAdapter.assetBalance(
#         cyDaiAddress)
#     cyWethDelegatedBalanceAmount = ironBankTvlAdapter.assetDelegatedBalance(
#         cyDaiAddress)
#     cyWethAdjustedBalanceAmount = cyWethUnderlyingTokenBalanceAmount - \
#         cyWethDelegatedBalanceAmount
#     cyWethAdjustedBalanceUsdc = oracle.getNormalizedValueUsdc(
#         cyWethTokenAddress, cyWethAdjustedBalanceAmount)

#     assetsTvlUsdc = ironBankTvlAdapter.assetsTvlUsdc(
#         [cyDaiAddress, cyWethAddress])

#     assert assetsTvlUsdc[0] == cyDaiAdjustedBalanceUsdc
#     assert assetsTvlUsdc[1] == cyDaiAdjustedBalanceUsdc
