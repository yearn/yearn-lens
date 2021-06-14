import pytest
import brownie

from brownie import Contract, ZERO_ADDRESS, chain

# Oracle deployment options
uniswapRouterAddress = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
uniswapFactoryAddress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
sushiswapRouterAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
sushiswapFactoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
curveAddressProvider = "0x0000000022D53366457F9d5E68Ec105046FC4383"
unitrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

# Test token addresses
uniswapLpTokenAddress = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"  # USDC/WETH
sushiswapLpTokenAddress = "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0"  # USDC/WETH
ethAddress = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
wethAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
threeCrvAddress = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"
threeCrvPoolAddress = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
cyDaiAddress = "0x8e595470Ed749b85C6F7669de83EAe304C2ec68F"

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
    newOracleAddress = "0x83d95e0D5f402511dB06817Aff3f9eA88224B030"
    oldOracleAddress = "0x6951b5Bd815043E3F842c1b026b0Fa888Cc2DD85"
    assert oracleAddress == oldOracleAddress
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


def test_set_calculations(
    Oracle, managementList, CalculationsCurve, gov, management, rando
):
    oracle = Oracle.deploy(managementList, usdcAddress, {"from": management})
    calculationsCurve = CalculationsCurve.deploy(
        curveAddressProvider, oracle, {"from": gov}
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
    assert not oracle.managementList() == ZERO_ADDRESS


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
    markets = oracleProxyIronBank.getIronBankMarkets()
    assert len(markets) > 0


def test_get_iron_bank_market_price_usdc(oracleProxyIronBank):
    price = oracleProxyIronBank.getIronBankMarketPriceUsdc(cyDaiAddress)
    assert price > 0


def test_is_iron_bank_market(oracleProxyIronBank):
    assert oracleProxyIronBank.isIronBankMarket(cyDaiAddress)
    assert not oracleProxyIronBank.isIronBankMarket(yfiAddress)


# Curve
def test_is_curve_lp_token(oracle, CalculationsCurve, gov):
    calculationsCurve = CalculationsCurve.deploy(
        curveAddressProvider, oracle, {"from": gov}
    )
    assert calculationsCurve.isCurveLpToken(threeCrvAddress)


def test_get_get_curve_price_usdc(oracleProxyCurve):
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


# Sushiswap
def test_get_lp_token_price_usdc(oracleProxySushiswap):
    lpTokenPrice = oracleProxySushiswap.getLpTokenPriceUsdc(uniswapLpTokenAddress)
    assert lpTokenPrice > 0


def test_get_lp_token_price_usdc(oracleProxySushiswap):
    lpTokenPrice = oracleProxySushiswap.getLpTokenPriceUsdc(uniswapLpTokenAddress)
    assert lpTokenPrice > 0


def test_is_lp_token(oracleProxySushiswap):
    tokenIsLp = oracleProxySushiswap.isLpToken(uniswapLpTokenAddress)
    assert tokenIsLp


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


def test_get_router_for_lp_token(oracleProxySushiswap):
    derivedRouterAddress = oracleProxySushiswap.getRouterForLpToken(
        uniswapLpTokenAddress
    )
    assert derivedRouterAddress == uniswapRouterAddress
    derivedRouterAddress = oracleProxySushiswap.getRouterForLpToken(
        sushiswapLpTokenAddress
    )
    assert derivedRouterAddress == sushiswapRouterAddress
    with brownie.reverts():
        oracleProxySushiswap.getRouterForLpToken(yfiAddress)


def test_get_lp_token_total_liquidity_usdc(oracleProxySushiswap):
    totalLiquidity = oracleProxySushiswap.getLpTokenTotalLiquidityUsdc(
        uniswapLpTokenAddress
    )
    assert totalLiquidity > 0