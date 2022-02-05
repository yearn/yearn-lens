import brownie


def test_eur_price(synth_calculations, addresses):
    price = synth_calculations.getPriceUsdc(addresses.tokens.sEUR)
    assert price > 0


def test_gbp_price(synth_calculations, addresses):
    price = synth_calculations.getPriceUsdc(addresses.tokens.sGBP)
    assert price > 0


def test_chf_price(synth_calculations, addresses):
    price = synth_calculations.getPriceUsdc(addresses.tokens.sCHF)
    assert price > 0


def test_aud_price(synth_calculations, addresses):
    price = synth_calculations.getPriceUsdc(addresses.tokens.sAUD)
    assert price > 0


def test_jpy_price(synth_calculations, addresses):
    price = synth_calculations.getPriceUsdc(addresses.tokens.sJPY)
    assert price > 0


def test_krw_price(synth_calculations, addresses):
    price = synth_calculations.getPriceUsdc(addresses.tokens.sKRW)
    assert price > 0

def test_synth_price_reverts_when_not_added(synth_calculations, addresses):
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(addresses.tokens.random_token)


def test_all_prices(synth_calculations, addresses):
    # TODO: synthAddress isn't used
    synthsAddresses = synth_calculations.synthsAddresses()
    for synthAddress in synthsAddresses:
        price = synth_calculations.getPriceUsdc(addresses.tokens.sKRW)
        assert price > 0
