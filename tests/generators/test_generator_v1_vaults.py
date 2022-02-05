import brownie
import pytest
from brownie import ZERO_ADDRESS

from ..addresses import *


@pytest.fixture
def v1Generator(AddressesGeneratorV1Vaults, management):
    # TODO: what is this address?
    registryAddress = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0"
    generator = AddressesGeneratorV1Vaults.deploy(
        registryAddress,
        {"from": management},
    )
    return generator


def test_generator_info(v1Generator):
    adapterInfo = v1Generator.generatorInfo()
    assert adapterInfo[0] == v1Generator
    assert adapterInfo[1] == "VAULT_V1"
    assert adapterInfo[2] == "VAULT"


def test_registry_address(v1Generator):
    assert not v1Generator.registry() == ZERO_ADDRESS


def test_assets_length(v1Generator):
    assetsLength = v1Generator.assetsLength()
    assert assetsLength > 0


def test_set_asset_deprecated(v1Generator, management):
    originalAssetsLength = v1Generator.assetsLength()
    originalAssetsAddressesLength = len(v1Generator.assetsAddresses())
    assert originalAssetsLength > 0
    print(v1Generator.assetsAddresses())
    v1Generator.setAssetDeprecated(yCrvAddress, True, {"from": management})
    newAssetsLength = v1Generator.assetsLength()
    newAssetsAddressesLength = len(v1Generator.assetsAddresses())
    print(v1Generator.assetsAddresses())
    newAssetsLength = v1Generator.assetsLength()
    assert v1Generator.assetDeprecated(yCrvAddress) == True
    assert newAssetsAddressesLength == originalAssetsAddressesLength - 1
    assert v1Generator.numberOfDeprecatedAssets() > 0
    assert newAssetsLength == originalAssetsLength - 1


def test_assets_addresses(v1Generator):
    assetsAddresses = v1Generator.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_set_position_spender_addresses(v1Generator, management, rando):
    with brownie.reverts():
        v1Generator.setPositionSpenderAddresses([ethZapAddress], {"from": rando})
    v1Generator.setPositionSpenderAddresses([ethZapAddress], {"from": management})
    assert v1Generator.positionSpenderAddresses(0) == ethZapAddress
    spenderAddresses = v1Generator.getPositionSpenderAddresses()
    assert len(spenderAddresses) > 0
