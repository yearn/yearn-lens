import brownie

from ..addresses import *


def test_iron_bank_and_compound(calculationsIronBank):
    price = calculationsIronBank.getPriceUsdc(cyDai)
    assert price > 0
    price = calculationsIronBank.getPriceUsdc(cUsdt)
    assert price > 0


def test_price_reverts(calculationsIronBank):
    with brownie.reverts():
        calculationsIronBank.getPriceUsdc(random_token)
