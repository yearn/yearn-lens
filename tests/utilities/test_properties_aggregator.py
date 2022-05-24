import pytest
from brownie import convert, Contract, chain

@pytest.fixture
def properties_aggregator(PropertiesAggregator, management):
    return PropertiesAggregator.deploy({"from": management})

@pytest.fixture
def vault_address():
    if chain.id == 1:
        return "0xd9788f3931Ede4D5018184E198699dC6d66C1915"
    elif chain.id == 250:
        return "0x637eC617c86D24E421328e6CAEa1d92114892439"
    elif chain.id == 42161:
        return "0x239e14A19DFF93a17339DCC444f74406C17f8E67"
    else:
        return None

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