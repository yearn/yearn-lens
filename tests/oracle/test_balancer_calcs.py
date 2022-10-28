import brownie
from brownie import Contract, interface
from pytest import approx

from ..addresses import *

def test_boosted_aave_pool(balancer_calculations, oracle):
    #need to set the test deployed oracle in the addressProvider for the recursive calls to work
    set_test_oracle(oracle)

    boosted_usd = balancer_calculations.getPriceUsdc(boostedAaveUsd)
    assert boosted_usd > 0

    boosted_usdt = balancer_calculations.getPriceUsdc(phantomUsdt)
    assert boosted_usdt > 0
    
    wrapped_usdt = balancer_calculations.getPriceUsdc(wAUsdt)
    assert wrapped_usdt > 1e6

    boosted_usd1 = oracle.getPriceUsdcRecommended(boostedAaveUsd)
    assert boosted_usd == boosted_usd1

    boosted_usdt1 = oracle.getPriceUsdcRecommended(phantomUsdt)
    assert boosted_usdt == boosted_usdt1
    
    wrapped_usdt1 = oracle.getPriceUsdcRecommended(wAUsdt)
    assert wrapped_usdt == wrapped_usdt1

def test_stable_pool(balancer_calculations, oracle):
    fud = balancer_calculations.getPriceUsdc(fudStable)
    assert fud > 1e6
    assert fud == oracle.getPriceUsdcRecommended(fudStable)
    
def test_normal_pools(balancer_calculations, oracle):
    steth = balancer_calculations.getPriceUsdc(wethwstEth)
    assert steth > 0

    bal = balancer_calculations.getPriceUsdc(balWeth)
    assert bal > 0

    assert steth ==  oracle.getPriceUsdcRecommended(wethwstEth)
    assert bal ==  oracle.getPriceUsdcRecommended(balWeth)

def set_test_oracle(oracle):
    owner = '0xC27AE930D94434bE000000000000000000000000'
    yap = Contract(yearnAddressesProviderAddress)
    yap.setAddress(
        ("ORACLE", oracle.address),
        {"from": owner}
    )
    assert yap.addressById("ORACLE") == oracle.address