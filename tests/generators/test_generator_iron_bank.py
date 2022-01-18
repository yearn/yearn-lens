import pytest
import brownie
from brownie import interface, ZERO_ADDRESS
from operator import itemgetter

cySusdAddress = "0x4e3a36A633f63aee0aB57b5054EC78867CB3C0b8"
ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"


@pytest.fixture
def ironBankGenerator(
    AddressesGeneratorIronBank, managementList, oracle, helper, management
):
    registryAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
    generator = AddressesGeneratorIronBank.deploy(
        registryAddress, managementList, {"from": management},
    )
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
    ironBankGenerator.setAssetDeprecated(cySusdAddress, True, {"from": management})
    newAssetsLength = ironBankGenerator.assetsLength()
    newAssetsAddressesLength = len(ironBankGenerator.assetsAddresses())
    print(ironBankGenerator.assetsAddresses())
    newAssetsLength = ironBankGenerator.assetsLength()
    assert ironBankGenerator.assetDeprecated(cySusdAddress) == True
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
