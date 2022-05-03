import brownie
from brownie import Contract, interface
from pytest import approx

from ..addresses import *


def test_iron_bank_and_compound(calculationsIronBank):
    price = calculationsIronBank.getPriceUsdc(cyDai)
    assert price > 0
    price = calculationsIronBank.getPriceUsdc(cUsdt)
    assert price > 0


def test_price_reverts(calculationsIronBank):
    with brownie.reverts():
        calculationsIronBank.getPriceUsdc(random_token)


def test_compound_usdc_token(calculationsIronBank, oracle):
    cUsdcToken = interface.CyToken(cUsdc)
    cUsdcTokenDecimals = cUsdcToken.decimals()
    assert cUsdcTokenDecimals == 8
    cUsdcExchangeRate = cUsdcToken.exchangeRateStored()
    assert cUsdcExchangeRate > 0
    usdcToken = interface.IERC20(cUsdcToken.underlying())
    usdcTokenDecimals = usdcToken.decimals()
    assert usdcTokenDecimals == 6
    usdcPrice = oracle.getPriceUsdcRecommended(usdcToken.address)
    assert usdcPrice > 0

    price = calculationsIronBank.getPriceUsdc(cUsdcToken.address)
    predictedPrice = (
        usdcPrice * cUsdcExchangeRate * 10**cUsdcTokenDecimals
    ) / 10 ** (usdcTokenDecimals + 18)
    assert approx(price, rel=1e-2) == predictedPrice


def test_compound_dai_token(calculationsIronBank, oracle):
    cDaiToken = interface.CyToken(cDai)
    cDaiTokenDecimals = cDaiToken.decimals()
    assert cDaiTokenDecimals == 8
    cDaiExchangeRate = cDaiToken.exchangeRateStored()
    assert cDaiExchangeRate > 0
    daiToken = interface.IERC20(cDaiToken.underlying())
    daiTokenDecimals = daiToken.decimals()
    assert daiTokenDecimals == 18
    daiPrice = oracle.getPriceUsdcRecommended(daiToken.address)
    assert daiPrice > 0

    price = calculationsIronBank.getPriceUsdc(cDaiToken.address)
    predictedPrice = (daiPrice * cDaiExchangeRate * 10**cDaiTokenDecimals) / 10 ** (
        daiTokenDecimals + 18
    )
    assert approx(price, rel=1e-2) == predictedPrice


def test_yearn_usdc_token(calculationsIronBank, oracle):
    cyUsdcToken = interface.CyToken(cyUsdcAddress)
    cyUsdcTokenDecimals = cyUsdcToken.decimals()
    assert cyUsdcTokenDecimals == 8
    cyUsdcExchangeRate = cyUsdcToken.exchangeRateStored()
    assert cyUsdcExchangeRate > 0
    usdcToken = interface.IERC20(cyUsdcToken.underlying())
    usdcTokenDecimals = usdcToken.decimals()
    assert usdcTokenDecimals == 6
    usdcPrice = oracle.getPriceUsdcRecommended(usdcToken.address)
    assert usdcPrice > 0

    price = calculationsIronBank.getPriceUsdc(cyUsdcToken.address)
    predictedPrice = (
        usdcPrice * cyUsdcExchangeRate * 10**cyUsdcTokenDecimals
    ) / 10 ** (usdcTokenDecimals + 18)
    assert approx(price, rel=1e-2) == predictedPrice
