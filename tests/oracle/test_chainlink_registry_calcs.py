import brownie
import pytest

from ..addresses import *
from brownie import chain


@pytest.fixture
def calculations_chainlink_registry(CalculationsChainlinkRegistry, management):
    return CalculationsChainlinkRegistry.deploy({"from": management})

def test_adding_feed(calculations_chainlink_registry):
    chain.snapshot()
    with brownie.reverts():
        calculations_chainlink_registry.getPriceUsdc(yfiAddress)

    calculations_chainlink_registry.setTokenFeed(yfiAddress, yfiUsdFeed)

    assert calculations_chainlink_registry.getPriceUsdc(yfiAddress) > 0
    chain.revert()

def test_adding_multiple_feeds(calculations_chainlink_registry, management):
    chain.snapshot()
    with brownie.reverts():
        calculations_chainlink_registry.getPriceUsdc(yfiAddress)

    with brownie.reverts():
        calculations_chainlink_registry.getPriceUsdc(wethAddress)

    calculations_chainlink_registry.setTokenFeeds(
        [(yfiAddress, yfiUsdFeed), (wethAddress, wethUsdFeed)],
        {"from": management}
        )

    assert calculations_chainlink_registry.getPriceUsdc(yfiAddress) > 0
    assert calculations_chainlink_registry.getPriceUsdc(wethAddress) > 0
    chain.revert()
