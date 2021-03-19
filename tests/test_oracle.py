import pytest
import brownie

from brownie import Oracle, accounts, Contract, ZERO_ADDRESS

# Oracle deployment options
uniswapRouterAddress = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
uniswapFactoryAddress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
sushiswapRouterAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
sushiswapFactoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
curveRegistryAddress = "0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c"
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


@pytest.fixture
def managementList(ManagementList, gov):
    return ManagementList.deploy("Managemenet list", {"from": gov})


@pytest.fixture
def oracle(
    gov,
    Oracle,
    managementList,
    CalculationsSushiswap,
    CalculationsCurve,
    CalculationsIronBank,
):
    oracle = Oracle.deploy(managementList, usdcAddress, {"from": gov})
    calculationsSushiswap = CalculationsSushiswap.deploy(
        uniswapRouterAddress,
        uniswapFactoryAddress,
        sushiswapRouterAddress,
        sushiswapFactoryAddress,
        {"from": gov},
    )
    calculationsCurve = CalculationsCurve.deploy(curveRegistryAddress, {"from": gov})
    calculationsIronBank = CalculationsIronBank.deploy(unitrollerAddress, {"from": gov})
    oracle.setCalculations(
        [calculationsCurve, calculationsIronBank, calculationsSushiswap]
    )
    return oracle


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
def test_set_calculations(Oracle, ManagementList, CalculationsCurve, gov, rando):
    managementList = ManagementList.deploy("Managemenet list", {"from": gov})
    oracle = Oracle.deploy(managementList, usdcAddress, {"from": gov})
    calculationsCurve = CalculationsCurve.deploy(curveRegistryAddress, {"from": gov})

    # Randos cannot set calculations
    with brownie.reverts():
        oracle.setCalculations(
            [calculationsCurve], {"from": rando},
        )

    # Managers can set calculations
    oracle.setCalculations(
        [calculationsCurve], {"from": gov},
    )


def test_get_price_usdc_sushiswap(oracle):
    price = oracle.getPriceUsdcEtherscan(yfiAddress)
    assert price > 0


def test_get_price_usdc_curve(oracle):
    price = oracle.getPriceUsdcEtherscan(threeCrvAddress)
    assert price > 0


def test_get_price_usdc_lp_token(oracle):
    price = oracle.getPriceUsdcEtherscan(uniswapLpTokenAddress)
    assert price > 0


def test_get_price_usdc_iron_bank(oracle):
    price = oracle.getPriceUsdcEtherscan(cyDaiAddress)
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
def test_is_curve_lp_token(oracleProxyCurve, CalculationsCurve, gov):
    calculationsCurve = CalculationsCurve.deploy(curveRegistryAddress, {"from": gov})
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
    token = oracleProxyCurve.getFirstUnderlyingCoinFromPool(threeCrvPoolAddress)
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
    assert ethPrice == wethPrice
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
