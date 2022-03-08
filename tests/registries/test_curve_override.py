import brownie
import pytest

from ..addresses import *


def test_lp_pool_override(curve_registry_override):
    curve_registry_override.setPoolForLp(
        threeCrvPoolAddress, sushiswapLpTokenAddress  # random pool
    )
    override_pool = curve_registry_override.poolByLp(sushiswapLpTokenAddress)
    assert override_pool == threeCrvPoolAddress


def test_lp_pool_curve_registry0(curve_registry_override):
    curve_registry_override.setCurveRegistries([curveRegistryAddress0])
    curve_pool = curve_registry_override.poolByLp(threeCrvAddress)
    assert curve_pool == threeCrvPoolAddress


def test_lp_pool_curve_registry5(curve_registry_override):
    curve_registry_override.setCurveRegistries([curveRegistryAddress5])
    curve_pool = curve_registry_override.poolByLp(triCryptoAddress)
    assert curve_pool == triCryptoPoolAddress


def test_lp_pool_reverts(curve_registry_override):
    with brownie.reverts():
        # curve registry should never be in an LP->Pool mapping
        curve_pool = curve_registry_override.poolByLp(curveRegistryAddress)


def test_pool_list(curve_registry_override):
    curve_registry_override.setCurveRegistries(
            [curveRegistryAddress0, curveRegistryAddress5]
            )
    pool_list = curve_registry_override.curveRegistriesList()
    assert len(pool_list) == 2
