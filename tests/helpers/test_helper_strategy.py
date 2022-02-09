import pytest

from ..addresses import *


@pytest.fixture
def v2VaultsAdapter(RegisteryAdapterV2Vault, managementList, oracle, management):
    return RegisteryAdapterV2Vault.deploy(
        v2RegistryAddress,
        oracle,
        managementList,
        {"from": management},
    )


@pytest.fixture
def strategyHelper(
    StrategiesHelper, v2AddressesGenerator, addressMergeHelper, oracle, management
):
    return StrategiesHelper.deploy(
        v2AddressesGenerator, addressMergeHelper, oracle, {"from": management}
    )


# Tests count of strategies for a vault given count output
def test_asset_strategies_length(strategyHelper):
    length = strategyHelper.assetStrategiesLength(yfiVaultAddress)
    assert length > 0


# Tests count of strategies for all vaults given count output
def test_assets_strategies_length(strategyHelper):
    length = strategyHelper.assetsStrategiesLength()
    assert length > 0


# Tests count of strategies for a vault given list of addresses
def test_asset_strategies_addresses(strategyHelper):
    strategies = strategyHelper.assetStrategiesAddresses(yfiVaultAddress)
    assert len(strategies) > 0


# Tests count of strategies for all vaults given list of addresses
def test_assets_strategies_addresses(strategyHelper):
    strategies = strategyHelper.assetsStrategiesAddresses()
    assert len(strategies) > 0


# Tests count of strategies for a vault given strategy metadata
def test_asset_strategies(strategyHelper):
    strategies = strategyHelper.assetStrategies(yfiVaultAddress)
    assert len(strategies) > 0


# Tests count of strategies for all vaults given strategy metadata
# TODO: use different vault addresses
def test_assets_strategies(strategyHelper):
    strategies = strategyHelper.assetsStrategies([yfiVaultAddress])
    assert len(strategies) > 0
