import pytest

from .addresses import *

@pytest.fixture
def curve_registry_override(CurveRegistryOverrides, management):
    return CurveRegistryOverrides.deploy(
            curveAddressProvider,
            curveRegistryAddress,
            {'from': management}
            )

def test_lp_pool_override(curve_registry_override):
    curve_registry_override.setPoolForLp(
            threeCrvPoolAddress, # random pool
            sushiswapLpTokenAddress
            )
    override_pool = curve_registry_override.poolByLp(sushiswapLpTokenAddress)
    assert override_pool == threeCrvPoolAddress

def test_lp_pool_curve(curve_registry_override):
    curve_pool = curve_registry_override.poolByLp(triCryptoAddress)
    assert curve_pool == threeCrvPoolAddress

def test_curve_registries_list(curve_registry_override):
    print(curve_registry_override.curveRegistriesList())
