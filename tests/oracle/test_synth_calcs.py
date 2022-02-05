import brownie
from ..addresses import *


def test_eur_price(synth_calculations):
    price = synth_calculations.getPriceUsdc(sEUR)
    assert price > 0


def test_gbp_price(synth_calculations):
    price = synth_calculations.getPriceUsdc(sGBP)
    assert price > 0


def test_chf_price(synth_calculations):
    price = synth_calculations.getPriceUsdc(sCHF)
    assert price > 0


def test_aud_price(synth_calculations):
    price = synth_calculations.getPriceUsdc(sAUD)
    assert price > 0


def test_jpy_price(synth_calculations):
    price = synth_calculations.getPriceUsdc(sJPY)
    assert price > 0


def test_krw_price(synth_calculations):
    price = synth_calculations.getPriceUsdc(sKRW)
    assert price > 0


def test_synth_price_reverts_when_not_added(synth_calculations):
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(random_token)


def test_all_prices(synth_calculations):
    # TODO: synthAddress isn't used
    synthsAddresses = synth_calculations.synthsAddresses()
    for synthAddress in synthsAddresses:
        price = synth_calculations.getPriceUsdc(sKRW)
        assert price > 0
