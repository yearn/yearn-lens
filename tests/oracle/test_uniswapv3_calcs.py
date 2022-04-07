import brownie

usdc = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
weth = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
wsteth = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"
invalid_token = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc3"


def test_weth_price(uniswapv3_calculations):
    price = uniswapv3_calculations.getPriceUsdc(weth)
    assert price > 0

def test_wsteth_price(uniswapv3_calculations):
    price = uniswapv3_calculations.getPriceUsdc(wsteth)
    assert price > 0

def test_weth_price_with_invalid_pool_from_first_fee(uniswapv3_calculations):
    uniswapv3_calculations.setFees([1, 500])
    price = uniswapv3_calculations.getPriceUsdc(weth)
    assert price > 0


def test_set_fee(uniswapv3_calculations):
    uniswapv3_calculations.setFees([600, 4000])
    assert uniswapv3_calculations.fees(0) == 600
    assert uniswapv3_calculations.fees(1) == 4000


def test_set_period(uniswapv3_calculations):
    uniswapv3_calculations.setPeriod(20)
    assert uniswapv3_calculations.period() == 20


def test_invalid_token_price_reverts(uniswapv3_calculations):
    with brownie.reverts():
        uniswapv3_calculations.getPriceUsdc(invalid_token)


def test_invalid_pools_reverts(uniswapv3_calculations):
    with brownie.reverts():
        uniswapv3_calculations.setFees([1, 2])
        uniswapv3_calculations.getPriceUsdc(wsteth)


def test_set_invalid_fees_reverts(uniswapv3_calculations):
    with brownie.reverts():
        uniswapv3_calculations.setFees([])


def test_set_period_reverts(uniswapv3_calculations):
    with brownie.reverts():
        uniswapv3_calculations.setPeriod(0)
