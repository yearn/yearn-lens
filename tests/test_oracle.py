import pytest
import brownie

from brownie import Oracle, accounts


uniswapRouterAddress = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
uniswapFactoryAddress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
sushiswapRouterAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
sushiswapFactoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
curveRegistryAddress = "0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c"
unitrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

uniswapLpTokenAddress = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"  # USDC/WETH
sushiswapLpTokenAddress = "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0"  # USDC/WETH
ethAddress = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
wethAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"

threeCrvAddress = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"

cyDaiAddress = "0x8e595470Ed749b85C6F7669de83EAe304C2ec68F"


@pytest.fixture
def oracle(gov):
    return Oracle.deploy(
        uniswapRouterAddress,
        uniswapFactoryAddress,
        sushiswapRouterAddress,
        sushiswapFactoryAddress,
        curveRegistryAddress,
        unitrollerAddress,
        usdcAddress,
        {"from": gov},
    )


def test_get_router_for_lp_token(oracle):
    # Uniswap router
    derivedRouterAddress = oracle.getRouterForLpToken(uniswapLpTokenAddress)
    assert derivedRouterAddress == uniswapRouterAddress

    # Sushiswap router
    derivedRouterAddress = oracle.getRouterForLpToken(sushiswapLpTokenAddress)
    assert derivedRouterAddress == sushiswapRouterAddress

    # Invalid router
    with brownie.reverts():
        oracle.getRouterForLpToken(yfiAddress)


def test_get_price_usdc_curve(oracle):
    price = oracle.getPriceUsdc(threeCrvAddress)
    assert price > 0


def test_get_price_usdc_lp_token(oracle):
    price = oracle.getPriceUsdc(uniswapLpTokenAddress)
    assert price > 0


def test_get_price_usdc_iron_bank(oracle):
    price = oracle.getPriceUsdc(cyDaiAddress)
    assert price > 0


def test_get_iron_bank_market_price_usdc(oracle):
    price = oracle.getIronBankMarketPriceUsdc(cyDaiAddress)
    assert price > 0


def test_iron_bank_markets(oracle):
    markets = oracle.getIronBankMarkets()
    assert len(markets) > 0


def test_is_iron_bank_market(oracle):
    assert oracle.isIronBankMarket(cyDaiAddress)
    assert not oracle.isIronBankMarket(yfiAddress)


def test_get_lp_token_price_usdc(oracle):
    lpTokenPrice = oracle.getLpTokenPriceUsdc(uniswapLpTokenAddress)
    assert lpTokenPrice > 0


def test_get_lp_token_price_usdc(oracle):
    lpTokenPrice = oracle.getLpTokenPriceUsdc(uniswapLpTokenAddress)
    assert lpTokenPrice > 0


def test_is_lp_token(oracle):
    tokenIsLp = oracle.isLpToken(uniswapLpTokenAddress)
    assert tokenIsLp


def test_get_price_from_router(oracle):
    ethPrice = oracle.getPriceFromRouter(ethAddress, usdcAddress)
    wethPrice = oracle.getPriceFromRouter(wethAddress, usdcAddress)
    assert ethPrice == wethPrice
    usdcPriceInEth = oracle.getPriceFromRouter(usdcAddress, ethAddress)
    usdcPriceInWeth = oracle.getPriceFromRouter(usdcAddress, wethAddress)
    assert usdcPriceInEth == usdcPriceInWeth


def test_get_lp_token_total_liquidity_usdc(oracle):
    totalLiquidity = oracle.getLpTokenTotalLiquidityUsdc(uniswapLpTokenAddress)
    assert totalLiquidity > 0


def test_account_balance(oracle):
    eth_usdc = oracle.getPriceFromRouter(ethAddress, usdcAddress)
    assert eth_usdc > 0
    yfi_usdc = oracle.getPriceUsdc(yfiAddress)
    assert yfi_usdc > 0

