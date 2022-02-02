import brownie
import pytest
from brownie import ZERO_ADDRESS, chain

YFI = "0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e"
YFI_USD_FEED = "0xa027702dbb89fbd58938e4324ac03b58d812b0e1"

WETH = "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
WETH_USD_FEED = "0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419"

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
