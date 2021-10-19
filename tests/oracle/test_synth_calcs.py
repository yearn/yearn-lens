import pytest
import brownie

from brownie import ZERO_ADDRESS, chain

sEUR = "0xD71eCFF9342A5Ced620049e616c5035F1dB98620"
sGBP = "0x97fe22E7341a0Cd8Db6F6C021A24Dc8f4DAD855F"
sCHF = "0x0F83287FF768D1c1e17a42F44d644D7F22e8ee1d"
sAUD = "0xF48e200EAF9906362BB1442fca31e0835773b8B4"
sJPY = "0xF6b1C627e95BFc3c1b4c9B825a032Ff0fBf3e07d"
sKRW = "0x269895a3dF4D73b077Fc823dD6dA1B95f72Aaf9B"

eur_usd_feed = "0xb49f677943BC038e9857d61E7d053CaA2C1734C1"
gbp_usd_feed = "0x5c0Ab2d9b5a7ed9f470386e82BB36A3613cDd4b5"
chf_usd_feed = "0x449d117117838fFA61263B61dA6301AA2a88B13A"
aud_usd_feed = "0x77F9710E7d0A19669A13c055F62cd80d313dF022"
jpy_usd_feed = "0xBcE206caE7f0ec07b545EddE332A47C2F75bbeb3"
krw_usd_feed = "0x01435677FB11763550905594A16B645847C1d0F3"
new_test_feed = "0x1237d4FdF54c74fb1753aDeDe4c297d0eD1E61a5"


def test_setting_eur_feed(synth_calculations):
    assert synth_calculations.eurChainlinkFeed() == eur_usd_feed
    synth_calculations.setEurFeed(new_test_feed)
    assert synth_calculations.eurChainlinkFeed() == new_test_feed


def test_setting_gbp_feed(synth_calculations):
    assert synth_calculations.gbpChainlinkFeed() == gbp_usd_feed
    synth_calculations.setGbpFeed(new_test_feed)
    assert synth_calculations.gbpChainlinkFeed() == new_test_feed


def test_setting_chf_feed(synth_calculations):
    assert synth_calculations.chfChainlinkFeed() == chf_usd_feed
    synth_calculations.setChfFeed(new_test_feed)
    assert synth_calculations.chfChainlinkFeed() == new_test_feed


def test_setting_aud_feed(synth_calculations):
    assert synth_calculations.audChainlinkFeed() == aud_usd_feed
    synth_calculations.setAudFeed(new_test_feed)
    assert synth_calculations.audChainlinkFeed() == new_test_feed


def test_setting_jpy_feed(synth_calculations):
    assert synth_calculations.jpyChainlinkFeed() == jpy_usd_feed
    synth_calculations.setJpyFeed(new_test_feed)
    assert synth_calculations.jpyChainlinkFeed() == new_test_feed


def test_setting_krw_feed(synth_calculations):
    assert synth_calculations.krwChainlinkFeed() == krw_usd_feed
    synth_calculations.setKrwFeed(new_test_feed)
    assert synth_calculations.krwChainlinkFeed() == new_test_feed


def test_eur_price(synth_calculations):
    price = synth_calculations.getEurPrice()
    assert price > 0


def test_gbp_price(synth_calculations):
    price = synth_calculations.getGbpPrice()
    assert price > 0


def test_chf_price(synth_calculations):
    price = synth_calculations.getChfPrice()
    assert price > 0


def test_aud_price(synth_calculations):
    price = synth_calculations.getAudPrice()
    assert price > 0


def test_jpy_price(synth_calculations):
    price = synth_calculations.getJpyPrice()
    assert price > 0


def test_krw_price(synth_calculations):
    price = synth_calculations.getKrwPrice()
    assert price > 0


def test_synth_price_reverts_when_not_added(synth_calculations):
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sEUR)


def test_synth_price_after_added_then_removed(synth_calculations):
    synth_calculations.setEurSynth(sEUR, True)
    assert synth_calculations.getPriceUsdc(sEUR) > 0

    synth_calculations.setEurSynth(sEUR, False)
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sEUR)


def test_setting_all_synths(synth_calculations):
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sEUR)
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sGBP)
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sCHF)
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sAUD)
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sJPY)
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sKRW)

    synth_calculations.setSynths([sEUR], [sGBP], [sCHF], [], [], [])

    assert synth_calculations.getPriceUsdc(sEUR) > 0
    assert synth_calculations.getPriceUsdc(sGBP) > 0
    assert synth_calculations.getPriceUsdc(sCHF) > 0
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sAUD)
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sJPY)
    with brownie.reverts("token not a synth"):
        synth_calculations.getPriceUsdc(sKRW)

    synth_calculations.setSynths([], [], [], [sAUD], [sJPY], [sKRW])

    assert synth_calculations.getPriceUsdc(sEUR) > 0
    assert synth_calculations.getPriceUsdc(sGBP) > 0
    assert synth_calculations.getPriceUsdc(sCHF) > 0
    assert synth_calculations.getPriceUsdc(sAUD) > 0
    assert synth_calculations.getPriceUsdc(sJPY) > 0
    assert synth_calculations.getPriceUsdc(sKRW) > 0
