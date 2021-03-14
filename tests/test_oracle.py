import pytest

from brownie import Oracle, accounts


uniswapRouterAddress = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
uniswapFactoryAddress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
sushiswapRouterAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
sushiswapFactoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
curveRegistryAddress = "0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c"
uniswapLpTokenAddress = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"  # USDC/WETH
sushiswapLpTokenAddress = "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0"  # USDC/WETH

usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
ethAddress = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"


@pytest.fixture
def oracle(gov):
    return Oracle.deploy(
        uniswapRouterAddress,
        uniswapFactoryAddress,
        sushiswapRouterAddress,
        sushiswapFactoryAddress,
        curveRegistryAddress,
        usdcAddress,
        {"from": gov},
    )


def test_get_lp_token_price_usdc(oracle):
    lpTokenPrice = oracle.getLpTokenPriceUsdc(uniswapLpTokenAddress)
    assert lpTokenPrice > 0


def test_is_lp_token(oracle):
    tokenIsLp = oracle.isLpToken(uniswapLpTokenAddress)
    assert tokenIsLp


def test_get_lp_token_total_liquidity_usdc(oracle):
    totalLiquidity = oracle.getLpTokenTotalLiquidityUsdc(uniswapLpTokenAddress)
    assert totalLiquidity > 0
    print("USDC/ETH Uniswap liquidity", totalLiquidity)


def test_get_router_for_lp_token(oracle):
    derivedUniswapRouterAddress = oracle.getRouterForLpToken(uniswapLpTokenAddress)
    assert derivedUniswapRouterAddress == uniswapRouterAddress
    print("Uniswap Router", derivedUniswapRouterAddress)

    derivedSushiswapRouterAddress = oracle.getRouterForLpToken(sushiswapLpTokenAddress)
    assert derivedSushiswapRouterAddress == sushiswapRouterAddress
    print("Sushiswap Router", derivedSushiswapRouterAddress)


def test_account_balance(oracle):
    eth_usdc = oracle.getPriceFromRouter(ethAddress, usdcAddress)
    print("ETH/USDC", eth_usdc)
    assert eth_usdc > 0

    yfi_usdc = oracle.getPriceUsdc(yfiAddress)
    print("YFI/USDC", yfi_usdc)
    assert yfi_usdc > 0

