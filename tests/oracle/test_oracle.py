import pytest
import brownie

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

def test_add_and_remove_token_alias(oracle, management, addresses):
    assert oracle.tokenAliases(addresses.tokens.ethAddress) != ZERO_ADDRESS
    oracle.removeTokenAlias(addresses.tokens.ethAddress, {"from": management})
    assert oracle.tokenAliases(addresses.tokens.ethAddress) == ZERO_ADDRESS
    oracle.addTokenAlias(
        addresses.tokens.ethAddress,
        addresses.tokens.wethAddress,
        {"from": management}
        )
    assert oracle.tokenAliases(addresses.tokens.ethAddress) == addresses.tokens.wethAddress


def test_add_token_aliases(oracle, management, addresses):
    oracle.addTokenAliases(
        [[addresses.tokens.ethAddress, addresses.tokens.yfiAddress]],
        {"from": management}
        )
    assert oracle.tokenAliases(addresses.tokens.ethAddress) == addresses.tokens.yfiAddress


def test_set_calculations(
    Oracle, CalculationsCurve, gov, management, addresses, rando
):
    oracle = Oracle.deploy(addresses.tokens.usdcAddress, {"from": management})
    calculationsCurve = CalculationsCurve.deploy(
        addresses.providers.curveAddressProviderAddress, oracle, {"from": gov}
    )

    # Oracles with no calculations should revert
    proxyOracle = Contract.from_abi("", oracle, CalculationsCurve.abi)
    with brownie.reverts():
        proxyOracle.getPriceUsdc(addresses.tokens.usdcAddress)

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


def test_get_price_usdc_sushiswap(oracle, addresses):
    price = oracle.getPriceUsdcRecommended(addresses.tokens.yfiAddress)
    assert price > 0


def test_get_price_usdc_curve(oracle, addresses):
    price = oracle.getPriceUsdcRecommended(addresses.tokens.threeCrvAddress)
    assert price > 0


def test_get_price_usdc_lp_token(oracle, addresses):
    price = oracle.getPriceUsdcRecommended(addresses.tokens.uniswapLpTokenAddress)
    assert price > 0


def test_get_price_usdc_iron_bank(oracle, addresses):
    price = oracle.getPriceUsdcRecommended(addresses.tokens.cyDaiAddress)
    assert price > 0


# Iron Bank
def test_get_iron_bank_markets(oracleProxyIronBank, addresses):
    markets = oracleProxyIronBank.getIronBankMarkets(addresses.misc.unitrollerAddress)
    assert len(markets) > 0


def test_get_iron_bank_market_price_usdc(oracleProxyIronBank, addresses):
    price = oracleProxyIronBank.getIronBankMarketPriceUsdc(addresses.tokens.cyDaiAddress)
    assert price > 0


def test_is_iron_bank_market(oracleProxyIronBank, addresses):
    assert oracleProxyIronBank.isIronBankMarket(addresses.misc.unitrollerAddress, addresses.tokens.cyDaiAddress)
    assert not oracleProxyIronBank.isIronBankMarket(addresses.misc.unitrollerAddress, addresses.tokens.yfiAddress)


# Curve
def test_is_curve_lp_token(oracleProxyCurve, addresses):
    assert oracleProxyCurve.isCurveLpToken(addresses.tokens.threeCrvAddress)


def test_get_curve_price_usdc(oracleProxyCurve, addresses):
    price = oracleProxyCurve.getCurvePriceUsdc(addresses.tokens.threeCrvAddress)
    assert price > 0

def test_base_price(oracleProxyCurve, addresses):
    price = oracleProxyCurve.getBasePrice(addresses.tokens.threeCrvAddress)
    assert price > 0


def test_virtual_price(oracleProxyCurve, addresses):
    price = oracleProxyCurve.getVirtualPrice(addresses.tokens.threeCrvAddress)
    assert price > 0


def test_get_first_underlying_coin_from_pool(oracleProxyCurve, addresses):
    token = oracleProxyCurve.getUnderlyingCoinFromPool(addresses.tokens.threeCrvPoolAddress)
    assert token != ZERO_ADDRESS


def test_ib_eur_pool_price(oracle, addresses):
    price = oracle.getPriceUsdcRecommended(addresses.tokens.ibEurPoolAddress)
    assert price > 0


def test_ib_eur_pool_not_lp_token(oracleProxyCurve, addresses):
    is_curve_token = oracleProxyCurve.isCurveLpToken(addresses.tokens.ibEurPoolAddress)
    assert not is_curve_token


def test_cvx_crv_pool_price(oracle, addresses):
    price = oracle.getPriceUsdcRecommended(addresses.tokens.cvxCrvAddress)
    assert price > 0


# Calculations overrides
def test_calculations_overrides(oracle, calculationsOverrides, management, addresses):
    yvBOOSTPriceBefore = oracle.getPriceUsdcRecommended(addresses.misc.yvBOOSTAddress)
    calculationsOverrides.setOverrideForToken(addresses.misc.yvBOOSTAddress, "CALCULATIONS_SUSHISWAP", {"from": management})
    yvBOOSTPriceAfter = oracle.getPriceUsdcRecommended(addresses.misc.yvBOOSTAddress)
    assert yvBOOSTPriceBefore != yvBOOSTPriceAfter


def test_tri_crypto_price(curve_calculations, addresses):
    price = curve_calculations.getPriceUsdc(addresses.tokens.triCryptoAddress)
    assert price > 0


def test_curv_eurs_usdc_underlying_coins(curve_calculations, addresses):
    coins = curve_calculations.cryptoPoolUnderlyingTokensAddressesByPoolAddress(
        addresses.tokens.eursUsdcPool
        )
    assert coins == [addresses.tokens.usdc, addresses.tokens.eurs]


def test_curve_eurs_usdc_pool_is_crypto_pool(curve_calculations, addresses):
    assert curve_calculations.isLpCryptoPool(addresses.tokens.crvEURSUSDCAddress)


def test_curve_eurs_usdc_pool_totalValue(curve_calculations, addresses):
    assert curve_calculations.cryptoPoolLpTotalValueUsdc(addresses.tokens.crvEURSUSDCAddress) > 0


def test_curve_eurs_usdc_price(curve_calculations, addresses):
    assert curve_calculations.getPriceUsdc(addresses.tokens.crvEURSUSDCAddress) > 0


def test_curve_eurt_usd_price(curve_calculations, addresses):
    assert curve_calculations.getPriceUsdc(addresses.tokens.crvEURTUSDAddress) > 0


def test_curve_tri_crypto_price(curve_calculations, addresses):
    assert curve_calculations.isLpCryptoPool(addresses.tokens.triCryptoAddress)
    assert curve_calculations.isCurveLpToken(addresses.tokens.triCryptoAddress)
    assert curve_calculations.getPriceUsdc(addresses.tokens.triCryptoAddress) > 0


def test_update_yearn_addresses_provider(curve_calculations, management):
    chain.snapshot()
    old_address = curve_calculations.yearnAddressesProviderAddress()
    # TODO: what is this address?
    new_address = "0x12360e44C676ed0246c6Fb4c44B26191A5171B55"
    curve_calculations.updateYearnAddressesProviderAddress(new_address, {"from": management})
    assert curve_calculations.yearnAddressesProviderAddress() == new_address
    assert curve_calculations.yearnAddressesProviderAddress() != old_address
    chain.revert()


def test_update_yearn_addresses_provider_only_possible_by_owner(curve_calculations, rando):
    # TODO: what is this address?
    new_address = "0x12360e44C676ed0246c6Fb4c44B26191A5171B55"
    with brownie.reverts():
        curve_calculations.updateYearnAddressesProviderAddress(new_address, {"from": rando})


def test_update_curve_addresses_provider(curve_calculations, management):
    chain.snapshot()
    old_address = curve_calculations.curveAddressesProviderAddress()
    # TODO: what is this address?
    new_address = "0x12360e44C676ed0246c6Fb4c44B26191A5171B55"
    curve_calculations.updateCurveAddressesProviderAddress(new_address, {"from": management})
    assert curve_calculations.curveAddressesProviderAddress() == new_address
    assert curve_calculations.curveAddressesProviderAddress() != old_address
    chain.revert()


def test_update_curve_addresses_provider_only_possible_by_owner(curve_calculations, rando):
    # TODO: what is this address?
    new_address = "0x12360e44C676ed0246c6Fb4c44B26191A5171B55"
    with brownie.reverts():
        curve_calculations.updateCurveAddressesProviderAddress(new_address, {"from": rando})

# Sushiswap
def test_router_override(calculationsSushiswap, addresses):
    yveCRVPriceBefore = calculationsSushiswap.getPriceUsdc(addresses.misc.yveCRVAddress)
    calculationsSushiswap.setRouterOverrideForToken(
        addresses.misc.yveCRVAddress,
        addresses.routers.uniswapRouterAddress
        )
    yveCRVPriceAfter = calculationsSushiswap.getPriceUsdc(addresses.misc.yveCRVAddress)
    assert yveCRVPriceBefore != yveCRVPriceAfter
    calculationsSushiswap.setRouterOverrideForToken(
        addresses.misc.yveCRVAddress,
        addresses.routers.sushiswapRouterAddress
        )


def test_get_lp_token_price_usdc(oracleProxySushiswap, addresses):
    lpTokenPrice = oracleProxySushiswap.getLpTokenPriceUsdc(
        addresses.tokens.uniswapLpTokenAddress
        )
    assert lpTokenPrice > 0


def test_is_lp_token(oracleProxySushiswap, addresses):
    tokenIsLp = oracleProxySushiswap.isLpToken(addresses.tokens.uniswapLpTokenAddress)
    assert tokenIsLp

def test_eth_is_not_lp_token(oracleProxySushiswap, addresses):
    is_lp_token = oracleProxySushiswap.isLpToken(addresses.tokens.ethAddress)
    assert is_lp_token == False

def test_get_price_from_router(oracleProxySushiswap, addresses):
    ethPrice = oracleProxySushiswap.getPriceFromRouter(
        addresses.tokens.ethAddress,
        addresses.tokens.usdcAddress
        )
    wethPrice = oracleProxySushiswap.getPriceFromRouter(
        addresses.tokens.wethAddress,
        addresses.tokens.usdcAddress
        )
    # wethPriceAfterFees = oracleProxySushiswap.getPriceFromRouter(
    #     wethAddress, usdcAddress
    # )
    assert ethPrice == wethPrice
    # assert wethPrice > wethPriceAfterFees
    usdcPriceInEth = oracleProxySushiswap.getPriceFromRouter(
        addresses.tokens.usdcAddress,
        addresses.tokens.ethAddress
        )
    usdcPriceInWeth = oracleProxySushiswap.getPriceFromRouter(
        addresses.tokens.usdcAddress,
        addresses.tokens.wethAddress
        )
    assert usdcPriceInEth == usdcPriceInWeth


def test_get_lp_token_total_liquidity_usdc(oracleProxySushiswap, addresses):
    totalLiquidity = oracleProxySushiswap.getLpTokenTotalLiquidityUsdc(
        addresses.tokens.uniswapLpTokenAddress
    )
    assert totalLiquidity > 0


# Synth
'''
def test_synth_calculations(oracle, synth_calculations):
    sEUR = "0xD71eCFF9342A5Ced620049e616c5035F1dB98620"
    synth_calculations.setEurSynth(sEUR, True)
    assert oracle.getPriceUsdcRecommended(sEUR) > 0
'''

# Chainlink

def test_chainlink(chainlink_calculations, management, addresses):
    eurt_namehash = "0xd5aa869323f85cb893514ce48950ba7e84a8d0bf062a7e3058bcc494217da39f"
    with brownie.reverts():
        chainlink_calculations.getPriceUsdc(addresses.tokens.eurt)
    chainlink_calculations.setNamehash(addresses.tokens.eurt, eurt_namehash, {"from": management})
    assert chainlink_calculations.getPriceUsdc(addresses.tokens.eurt) > 0
