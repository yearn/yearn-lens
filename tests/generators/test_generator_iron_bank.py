import pytest
import brownie

from ..addresses import *
from brownie import ZERO_ADDRESS


@pytest.fixture
def ironBankGenerator(AddressesGeneratorIronBank, management):
    # TODO: what is this address?
    registryAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
    generator = AddressesGeneratorIronBank.deploy(registryAddress, {"from": management})
    return generator


def test_generator_info(ironBankGenerator):
    adapterInfo = ironBankGenerator.generatorInfo()
    assert adapterInfo[0] == ironBankGenerator
    assert adapterInfo[1] == "IRON_BANK_MARKET"
    assert adapterInfo[2] == "LENDING"


def test_registry_address(ironBankGenerator):
    assert not ironBankGenerator.registry() == ZERO_ADDRESS


def test_assets_length(ironBankGenerator):
    assetsLength = ironBankGenerator.assetsLength()
    assert assetsLength > 0


def test_set_asset_deprecated(ironBankGenerator, management):
    originalAssetsLength = ironBankGenerator.assetsLength()
    originalAssetsAddressesLength = len(ironBankGenerator.assetsAddresses())
    assert originalAssetsLength > 0
    print(ironBankGenerator.assetsAddresses())
    ironBankGenerator.setAssetDeprecated(cySusdOldAddress, True, {"from": management})
    newAssetsLength = ironBankGenerator.assetsLength()
    newAssetsAddressesLength = len(ironBankGenerator.assetsAddresses())
    print(ironBankGenerator.assetsAddresses())
    newAssetsLength = ironBankGenerator.assetsLength()
    assert ironBankGenerator.assetDeprecated(cySusdOldAddress) == True
    assert newAssetsAddressesLength == originalAssetsAddressesLength - 1
    assert ironBankGenerator.numberOfDeprecatedAssets() > 0
    assert newAssetsLength == originalAssetsLength - 1


def test_assets_addresses(ironBankGenerator):
    assetsAddresses = ironBankGenerator.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_set_position_spender_addresses(ironBankGenerator, management, rando):
    with brownie.reverts():
        ironBankGenerator.setPositionSpenderAddresses([ethZapAddress], {"from": rando})
    ironBankGenerator.setPositionSpenderAddresses([ethZapAddress], {"from": management})
    assert ironBankGenerator.positionSpenderAddresses(0) == ethZapAddress
    spenderAddresses = ironBankGenerator.getPositionSpenderAddresses()
    assert len(spenderAddresses) > 0
