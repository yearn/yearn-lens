import brownie

cyDai = "0x8e595470Ed749b85C6F7669de83EAe304C2ec68F"
cUsdt = "0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9"
random_token = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"


def test_iron_bank_and_compound(calculationsIronBank, management):
    price = calculationsIronBank.getPriceUsdc(cyDai)
    assert price > 0
    price = calculationsIronBank.getPriceUsdc(cUsdt)
    assert price > 0


def test_price_reverts(calculationsIronBank):
    with brownie.reverts():
        calculationsIronBank.getPriceUsdc(random_token)
