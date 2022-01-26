import pytest

yfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"

def test_asset_strategies_length(strategiesHelper):
    length = strategiesHelper.assetStrategiesLength(yfiVaultAddress)
    assert length > 0


def test_assets_strategies_length(strategiesHelper):
    length = strategiesHelper.assetsStrategiesLength()
    assert length > 0


def test_asset_strategies_addresses(strategiesHelper):
    strategies = strategiesHelper.assetStrategiesAddresses(yfiVaultAddress)
    assert len(strategies) > 0


def test_assets_strategies_addresses(strategiesHelper):
    strategies = strategiesHelper.assetsStrategiesAddresses()
    assert len(strategies) > 0


def test_asset_strategies(strategiesHelper):
    strategies = strategiesHelper.assetStrategies(yfiVaultAddress)
    assert len(strategies) > 0
