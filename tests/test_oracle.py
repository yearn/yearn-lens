import pytest

from brownie import Oracle, accounts


USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
ETH = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
YFI = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"


@pytest.fixture
def oracle():
    return accounts[0].deploy(Oracle)


def test_account_balance(oracle):
    eth_usdc = oracle.getPriceFromRouter(ETH, USDC)
    print("ETH/USDC", eth_usdc)
    assert eth_usdc > 0

    yfi_usdc = oracle.getPriceFromRouter(YFI, USDC)
    print("YFI/USDC", yfi_usdc)
    assert yfi_usdc > 0
