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
    curve_pool = curve_registry_override.poolByLp(threeCrvAddress)
    assert curve_pool == threeCrvPoolAddress


def test_lp_pool_curve_registry3(curve_registry_override):
    curve_pool = curve_registry_override.poolByLp(triCryptoAddress)
    assert curve_pool == triCryptoPoolAddress


def test_lp_pool_reverts(curve_registry_override):
    with brownie.reverts():
        # curve registry should never be in an LP->Pool mapping
        curve_pool = curve_registry_override.poolByLp(curveRegistryAddress)
