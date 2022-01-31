import brownie

sEUR = "0xD71eCFF9342A5Ced620049e616c5035F1dB98620"
sGBP = "0x97fe22E7341a0Cd8Db6F6C021A24Dc8f4DAD855F"
sCHF = "0x0F83287FF768D1c1e17a42F44d644D7F22e8ee1d"
sAUD = "0xF48e200EAF9906362BB1442fca31e0835773b8B4"
sJPY = "0xF6b1C627e95BFc3c1b4c9B825a032Ff0fBf3e07d"
sKRW = "0x269895a3dF4D73b077Fc823dD6dA1B95f72Aaf9B"
random_token = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"


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
    synthsAddresses = synth_calculations.synthsAddresses()
    for synthAddress in synthsAddresses:
        price = synth_calculations.getPriceUsdc(sKRW)
        assert price > 0
