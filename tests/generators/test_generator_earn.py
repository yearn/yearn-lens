import pytest
import brownie

from ..addresses import *
from brownie import ZERO_ADDRESS


@pytest.fixture
def earnGenerator(AddressesGeneratorEarn, oracle, management):
    # TODO: what address is this?
    registryAddress = "0x62a4e0E7574E5407656A65CC8DbDf70f3C6EB04B"
    generator = AddressesGeneratorEarn.deploy(registryAddress, {"from": management})
    return generator


# def test_generator_info(earnGenerator):
#     adapterInfo = earnGenerator.generatorInfo()
#     assert adapterInfo[0] == earnGenerator
#     assert adapterInfo[1] == "EARN"
#     assert adapterInfo[2] == "SAFE"


# def test_registry_address(earnGenerator):
#     assert not earnGenerator.registry() == ZERO_ADDRESS


# def test_assets_length(earnGenerator):
#     assetsLength = earnGenerator.assetsLength()
#     assert assetsLength > 0


def test_set_asset_deprecated(earnGenerator, management):
    originalAssetsLength = earnGenerator.assetsLength()
    originalAssetsAddressesLength = len(earnGenerator.assetsAddresses())
    assert originalAssetsLength > 0
    earnGenerator.setAssetDeprecated(yDaiV2Address, True, {"from": management})
    newAssetsLength = earnGenerator.assetsLength()
    newAssetsAddressesLength = len(earnGenerator.assetsAddresses())
    newAssetsLength = earnGenerator.assetsLength()
    assert earnGenerator.assetDeprecated(yDaiV2Address) == True
    assert newAssetsAddressesLength == originalAssetsAddressesLength - 1
    assert earnGenerator.numberOfDeprecatedAssets() > 0
    assert newAssetsLength == originalAssetsLength - 1


def test_assets_addresses(earnGenerator):
    assetsAddresses = earnGenerator.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_set_position_spender_addresses(earnGenerator, management, rando):
    with brownie.reverts():
        earnGenerator.setPositionSpenderAddresses([ethZapAddress], {"from": rando})
    earnGenerator.setPositionSpenderAddresses([ethZapAddress], {"from": management})
    assert earnGenerator.positionSpenderAddresses(0) == ethZapAddress
    spenderAddresses = earnGenerator.getPositionSpenderAddresses()
    assert len(spenderAddresses) > 0
