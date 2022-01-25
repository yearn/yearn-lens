import pytest

yfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"


@pytest.fixture
def v2VaultsAdapter(RegisteryAdapterV2Vault, oracle, management):
    v2RegistryAddress = "0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804"
    return RegisteryAdapterV2Vault.deploy(
        v2RegistryAddress, oracle, {"from": management},
    )


@pytest.fixture
def strategyHelper(StrategiesHelper, v2VaultsAdapter, management, addressMergeHelper):
    return StrategiesHelper.deploy(
        v2VaultsAdapter, addressMergeHelper, {"from": management}
    )


def test_asset_strategies_length(strategyHelper, management):
    length = strategyHelper.assetStrategiesLength(yfiVaultAddress)
    assert length > 0


def test_assets_strategies_length(strategyHelper, management):
    length = strategyHelper.assetsStrategiesLength()
    assert length > 0


def test_asset_strategies_addresses(strategyHelper, management, v2VaultsAdapter):
    strategies = strategyHelper.assetStrategiesAddresses(yfiVaultAddress)
    assert len(strategies) > 0


def test_assets_strategies_addresses(strategyHelper, management):
    strategies = strategyHelper.assetsStrategiesAddresses()
    assert len(strategies) > 0


def test_asset_strategies(strategyHelper, management):
    strategies = strategyHelper.assetStrategies(yfiVaultAddress)
    assert len(strategies) > 0


def test_assets_strategies(strategyHelper, management):
    strategies = strategyHelper.assetsStrategies()
    assert len(strategies) > 0
