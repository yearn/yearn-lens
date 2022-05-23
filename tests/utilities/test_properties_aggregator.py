import pytest
from brownie import convert, Contract

@pytest.fixture
def properties_aggregator(PropertiesAggregator, management):
    return PropertiesAggregator.deploy({"from": management})

@pytest.fixture
def vault_address():
    return "0xd9788f3931Ede4D5018184E198699dC6d66C1915"

@pytest.fixture
def vault(vault_address):
    return Contract(vault_address)

def test_get_property(properties_aggregator, vault, vault_address):
    expected_total_assets = vault.totalAssets()
    result = properties_aggregator.getProperty(vault_address, "totalAssets")
    decoded = convert.to_uint(result)
    assert decoded == expected_total_assets

def test_get_properties(properties_aggregator, vault, vault_address):
    expected_total_assets = vault.totalAssets()
    expected_pps = vault.pricePerShare()

    result = properties_aggregator.getProperties(vault_address, ["totalAssets", "pricePerShare"])
    decoded_total_assets = convert.to_uint(result[0])
    decoded_pps = convert.to_uint(result[1])

    assert decoded_total_assets == expected_total_assets
    assert decoded_pps == expected_pps