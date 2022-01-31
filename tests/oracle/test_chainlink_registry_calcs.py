import brownie
import pytest
from brownie import ZERO_ADDRESS, chain

YFI = "0x82e3A8F066a6989666b031d916c43672085b1582"
YFI_USD_FEED = "0x745Ab5b69E01E2BE1104Ca84937Bb71f96f5fB21"

WETH = "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
WETH_USD_FEED = "0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612"

@pytest.fixture
def calculations_chainlink_registry(CalculationsChainlinkRegistry, management):
    return CalculationsChainlinkRegistry.deploy({"from": management})

def test_adding_feed(calculations_chainlink_registry):
    chain.snapshot()
    with brownie.reverts():
        calculations_chainlink_registry.getPriceUsdc(YFI)

    calculations_chainlink_registry.setTokenFeed(YFI, YFI_USD_FEED)

    assert calculations_chainlink_registry.getPriceUsdc(YFI) > 0
    chain.revert()

def test_adding_multiple_feeds(calculations_chainlink_registry, management):
    chain.snapshot()
    with brownie.reverts():
        calculations_chainlink_registry.getPriceUsdc(YFI)

    with brownie.reverts():
        calculations_chainlink_registry.getPriceUsdc(WETH)

    calculations_chainlink_registry.setTokenFeeds([(YFI, YFI_USD_FEED), (WETH, WETH_USD_FEED)], {"from": management})

    assert calculations_chainlink_registry.getPriceUsdc(YFI) > 0
    assert calculations_chainlink_registry.getPriceUsdc(WETH) > 0
    chain.revert()