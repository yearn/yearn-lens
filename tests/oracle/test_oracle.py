import pytest
import brownie

from ..addresses import *
from brownie import Contract, ZERO_ADDRESS, chain


# Fixtures
@pytest.fixture
def oracleProxyIronBank(oracle, CalculationsIronBank):
    return Contract.from_abi("", oracle, CalculationsIronBank.abi)


@pytest.fixture
def oracleProxySushiswap(oracle, CalculationsSushiswap):
    return Contract.from_abi("", oracle, CalculationsSushiswap.abi)


@pytest.fixture
def oracleProxyCurve(oracle, CalculationsCurve):
    return Contract.from_abi("", oracle, CalculationsCurve.abi)


# General
def test_update_prices_helper_oracle_address(pricesHelper, management):
    chain.snapshot()
    oracleAddress = pricesHelper.oracleAddress()
    # TODO: what address is this?
    newOracleAddress = "0x6951b5Bd815043E3F842c1b026b0Fa888Cc2DD85"
    assert newOracleAddress != oracleAddress
    pricesHelper.updateOracleAddress(newOracleAddress, {"from": management})
    assert pricesHelper.oracleAddress() == newOracleAddress
    chain.revert()


def test_add_and_remove_token_alias(oracle, management):
    assert oracle.tokenAliases(ethAddress) != ZERO_ADDRESS
    oracle.removeTokenAlias(ethAddress, {"from": management})
    assert oracle.tokenAliases(ethAddress) == ZERO_ADDRESS
    oracle.addTokenAlias(ethAddress, wethAddress, {"from": management})
    assert oracle.tokenAliases(ethAddress) == wethAddress


def test_add_token_aliases(oracle, management):
    oracle.addTokenAliases([[ethAddress, yfiAddress]], {"from": management})
    assert oracle.tokenAliases(ethAddress) == yfiAddress


def test_set_calculations(Oracle, CalculationsCurve, gov, management, rando):
    oracle = Oracle.deploy(usdcAddress, {"from": management})
    calculationsCurve = CalculationsCurve.deploy(
        curveAddressProviderAddress, oracle, {"from": gov}
    )

    # Oracles with no calculations should revert
    proxyOracle = Contract.from_abi("", oracle, CalculationsCurve.abi)
    with brownie.reverts():
        proxyOracle.getPriceUsdc(usdcAddress)

    # Randos cannot set calculations
    with brownie.reverts():
        oracle.setCalculations(
            [calculationsCurve],
            {"from": rando},
        )

    # Managers can set calculations
    oracle.setCalculations(
        [calculationsCurve],
        {"from": management},
    )

    # Oracle should return managementList address

    # TODO: what should this test be evaluating now that it is onlyOwner
    # assert not oracle.managementList() == ZERO_ADDRESS


def test_get_price_usdc_sushiswap(oracle):
    price = oracle.getPriceUsdcRecommended(yfiAddress)
    assert price > 0


def test_get_price_usdc_curve(oracle):
    price = oracle.getPriceUsdcRecommended(threeCrvAddress)
    assert price > 0


def test_get_price_usdc_lp_token(oracle):
    price = oracle.getPriceUsdcRecommended(uniswapLpTokenAddress)
    assert price > 0


def test_get_price_usdc_iron_bank(oracle):
    price = oracle.getPriceUsdcRecommended(cyDaiAddress)
    assert price > 0


# Iron Bank
def test_get_iron_bank_markets(oracleProxyIronBank):
    markets = oracleProxyIronBank.getIronBankMarkets(unitrollerAddress)
    assert len(markets) > 0


def test_get_iron_bank_market_price_usdc(oracleProxyIronBank):
    price = oracleProxyIronBank.getIronBankMarketPriceUsdc(cyDaiAddress)
    assert price > 0


def test_is_iron_bank_market(oracleProxyIronBank):
    assert oracleProxyIronBank.isIronBankMarket(unitrollerAddress, cyDaiAddress)
    assert not oracleProxyIronBank.isIronBankMarket(unitrollerAddress, yfiAddress)


# Curve
def test_is_curve_lp_token(oracleProxyCurve):
    assert oracleProxyCurve.isCurveLpToken(threeCrvAddress)


def test_get_curve_price_usdc(oracleProxyCurve):
    price = oracleProxyCurve.getCurvePriceUsdc(threeCrvAddress)
    assert price > 0


def test_base_price(oracleProxyCurve):
    price = oracleProxyCurve.getBasePrice(threeCrvAddress)
    assert price > 0


def test_virtual_price(oracleProxyCurve):
    price = oracleProxyCurve.getVirtualPrice(threeCrvAddress)
    assert price > 0


def test_get_first_underlying_coin_from_pool(oracleProxyCurve):
    token = oracleProxyCurve.getUnderlyingCoinFromPool(threeCrvPoolAddress)
    assert token != ZERO_ADDRESS


def test_ib_eur_pool_price(oracle):
    price = oracle.getPriceUsdcRecommended(ibEurPoolAddress)
    assert price > 0


def test_ib_eur_pool_not_lp_token(oracleProxyCurve):
    is_curve_token = oracleProxyCurve.isCurveLpToken(ibEurPoolAddress)
    assert not is_curve_token


def test_cvx_crv_pool_price(oracle):
    price = oracle.getPriceUsdcRecommended(cvxCrvAddress)
    assert price > 0


# Calculations overrides
def test_calculations_overrides(oracle, calculationsOverrides, management):
    yvBOOSTPriceBefore = oracle.getPriceUsdcRecommended(yvBOOSTAddress)
    calculationsOverrides.setOverrideForToken(
        yvBOOSTAddress, "CALCULATIONS_SUSHISWAP", {"from": management}
    )
    yvBOOSTPriceAfter = oracle.getPriceUsdcRecommended(yvBOOSTAddress)
    assert yvBOOSTPriceBefore != yvBOOSTPriceAfter


def test_tri_crypto_price(curve_calculations):
    price = curve_calculations.getPriceUsdc(triCryptoAddress)
    assert price > 0


def test_curv_eurs_usdc_underlying_coins(curve_calculations):
    coins = curve_calculations.cryptoPoolUnderlyingTokensAddressesByPoolAddress(
        eursUsdcPool
    )
    assert coins == [usdc, eurs]


def test_curve_eurs_usdc_pool_is_crypto_pool(curve_calculations):
    assert curve_calculations.isLpCryptoPool(crvEURSUSDCAddress)


def test_curve_eurs_usdc_pool_totalValue(curve_calculations):
    assert curve_calculations.cryptoPoolLpTotalValueUsdc(crvEURSUSDCAddress) > 0


def test_curve_eurs_usdc_price(curve_calculations):
    assert curve_calculations.getPriceUsdc(crvEURSUSDCAddress) > 0


def test_curve_eurt_usd_price(curve_calculations):
    assert curve_calculations.getPriceUsdc(crvEURTUSDAddress) > 0


def test_curve_tri_crypto_price(curve_calculations):
    assert curve_calculations.isLpCryptoPool(triCryptoAddress)
    assert curve_calculations.isCurveLpToken(triCryptoAddress)
    assert curve_calculations.getPriceUsdc(triCryptoAddress) > 0


def test_update_yearn_addresses_provider(curve_calculations, management):
    chain.snapshot()
    old_address = curve_calculations.yearnAddressesProviderAddress()
    # TODO: what is this address?
    new_address = "0x12360e44C676ed0246c6Fb4c44B26191A5171B55"
    curve_calculations.updateYearnAddressesProviderAddress(
        new_address, {"from": management}
    )
    assert curve_calculations.yearnAddressesProviderAddress() == new_address
    assert curve_calculations.yearnAddressesProviderAddress() != old_address
    chain.revert()


def test_update_yearn_addresses_provider_only_possible_by_owner(
    curve_calculations, rando
):
    # TODO: what is this address?
    new_address = "0x12360e44C676ed0246c6Fb4c44B26191A5171B55"
    with brownie.reverts():
        curve_calculations.updateYearnAddressesProviderAddress(
            new_address, {"from": rando}
        )


def test_update_curve_addresses_provider(curve_calculations, management):
    chain.snapshot()
    old_address = curve_calculations.curveAddressesProviderAddress()
    # TODO: what is this address?
    new_address = "0x12360e44C676ed0246c6Fb4c44B26191A5171B55"
    curve_calculations.updateCurveAddressesProviderAddress(
        new_address, {"from": management}
    )
    assert curve_calculations.curveAddressesProviderAddress() == new_address
    assert curve_calculations.curveAddressesProviderAddress() != old_address
    chain.revert()


def test_update_curve_addresses_provider_only_possible_by_owner(
    curve_calculations, rando
):
    # TODO: what is this address?
    new_address = "0x12360e44C676ed0246c6Fb4c44B26191A5171B55"
    with brownie.reverts():
        curve_calculations.updateCurveAddressesProviderAddress(
            new_address, {"from": rando}
        )


# Sushiswap
def test_router_override(calculationsSushiswap):
    yveCRVPriceBefore = calculationsSushiswap.getPriceUsdc(yveCRVAddress)
    calculationsSushiswap.setRouterOverrideForToken(yveCRVAddress, uniswapRouterAddress)
    yveCRVPriceAfter = calculationsSushiswap.getPriceUsdc(yveCRVAddress)
    assert yveCRVPriceBefore != yveCRVPriceAfter
    calculationsSushiswap.setRouterOverrideForToken(
        yveCRVAddress, sushiswapRouterAddress
    )


def test_get_lp_token_price_usdc(oracleProxySushiswap):
    lpTokenPrice = oracleProxySushiswap.getLpTokenPriceUsdc(uniswapLpTokenAddress)
    assert lpTokenPrice > 0


def test_is_lp_token(oracleProxySushiswap):
    tokenIsLp = oracleProxySushiswap.isLpToken(uniswapLpTokenAddress)
    assert tokenIsLp


def test_eth_is_not_lp_token(oracleProxySushiswap):
    is_lp_token = oracleProxySushiswap.isLpToken(ethAddress)
    assert is_lp_token == False


def test_get_price_from_router(oracleProxySushiswap):
    ethPrice = oracleProxySushiswap.getPriceFromRouter(ethAddress, usdcAddress)
    wethPrice = oracleProxySushiswap.getPriceFromRouter(wethAddress, usdcAddress)
    # wethPriceAfterFees = oracleProxySushiswap.getPriceFromRouter(
    #     wethAddress, usdcAddress
    # )
    assert ethPrice == wethPrice
    # assert wethPrice > wethPriceAfterFees
    usdcPriceInEth = oracleProxySushiswap.getPriceFromRouter(usdcAddress, ethAddress)
    usdcPriceInWeth = oracleProxySushiswap.getPriceFromRouter(usdcAddress, wethAddress)
    assert usdcPriceInEth == usdcPriceInWeth


def test_get_lp_token_total_liquidity_usdc(oracleProxySushiswap):
    totalLiquidity = oracleProxySushiswap.getLpTokenTotalLiquidityUsdc(
        uniswapLpTokenAddress
    )
    assert totalLiquidity > 0


# Synth
"""
def test_synth_calculations(oracle, synth_calculations):
    sEUR = "0xD71eCFF9342A5Ced620049e616c5035F1dB98620"
    synth_calculations.setEurSynth(sEUR, True)
    assert oracle.getPriceUsdcRecommended(sEUR) > 0
"""

# Chainlink


def test_chainlink(chainlink_calculations, management):
    with brownie.reverts():
        chainlink_calculations.getPriceUsdc(eurt)
    chainlink_calculations.setNamehash(eurt, eurt_namehash, {"from": management})
    assert chainlink_calculations.getPriceUsdc(eurt) > 0
