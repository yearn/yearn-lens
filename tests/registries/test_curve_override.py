import brownie
import pytest
from brownie import ZERO_ADDRESS

from ..addresses import *


def test_lp_pool_override(curve_registry_override):
    curve_registry_override.setPoolForLp(
        threeCrvPoolAddress, sushiswapLpTokenAddress  # random pool
    )
    override_pool = curve_registry_override.poolByLp(sushiswapLpTokenAddress)
    assert override_pool == threeCrvPoolAddress


def test_lp_pool_curve_registry(curve_registry_override):
    curve_registry_override.setCurveRegistries([curveRegistryAddress])
    curve_pool = curve_registry_override.poolByLp(threeCrvAddress)
    assert curve_pool == threeCrvPoolAddress


def test_lp_pool_curve_cryptoswap_registry(curve_registry_override):
    curve_registry_override.setCurveRegistries([curveCryptoSwapRegistryAddress])
    curve_pool = curve_registry_override.poolByLp(triCryptoAddress)
    assert curve_pool == triCryptoPoolAddress


def test_lp_pool_returns_zero(curve_registry_override):
    # curve registry should never be in an LP->Pool mapping
    curve_pool = curve_registry_override.poolByLp(curveRegistryAddress)
    assert curve_pool == ZERO_ADDRESS


def test_pool_list(curve_registry_override):
    curve_registry_override.setCurveRegistries(
            [curveRegistryAddress, curveCryptoSwapRegistryAddress]
            )
    pool_list = curve_registry_override.curveRegistriesList()
    assert len(pool_list) == 2
