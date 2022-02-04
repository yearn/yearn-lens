import brownie

ibAud = "0xfafdf0c4c1cb09d430bf88c75d88bb46dae09967"
random_token = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"


def test_ibAud(calculationsFixedforex):
    price = calculationsFixedforex.getPriceUsdc(ibAud)
    assert price > 0


def test_price_reverts(calculationsFixedforex):
    with brownie.reverts():
        calculationsFixedforex.getPriceUsdc(random_token)
