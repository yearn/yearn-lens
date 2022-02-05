import brownie

from ..addresses import *


def test_ibAud(calculationsFixedforex):
    price = calculationsFixedforex.getPriceUsdc(ibAud)
    assert price > 0


def test_price_reverts(calculationsFixedforex):
    with brownie.reverts():
        calculationsFixedforex.getPriceUsdc(random_token)
