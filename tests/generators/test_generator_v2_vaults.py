import pytest
import brownie

from ..addresses import *
from brownie import ZERO_ADDRESS


def test_generator_info(v2VaultsGenerator):
    adapterInfo = v2VaultsGenerator.generatorInfo()
    assert adapterInfo[0] == v2VaultsGenerator
    assert adapterInfo[1] == "VAULT_V2"
    assert adapterInfo[2] == "VAULT"


def test_registry_address(v2VaultsGenerator):
    assert not v2VaultsGenerator.registry() == ZERO_ADDRESS


def test_assets_length(v2VaultsGenerator):
    assetsLength = v2VaultsGenerator.assetsLength()
    assert assetsLength > 0


def test_set_asset_deprecated(v2VaultsGenerator, management):
    originalAssetsLength = v2VaultsGenerator.assetsLength()
    assert originalAssetsLength > 0
    v2VaultsGenerator.setAssetDeprecated(v2YfiVaultAddress, True, {"from": management})
    newAssetsLength = v2VaultsGenerator.assetsLength()
    v2VaultsGenerator.assetDeprecated(v2YfiVaultAddress) == True
    assert v2VaultsGenerator.numberOfDeprecatedAssets() > 0
    assert newAssetsLength == originalAssetsLength - 1
    v2VaultsGenerator.setAssetDeprecated(v2YfiVaultAddress, False, {"from": management})
    newAssetsLength = v2VaultsGenerator.assetsLength()
    assert newAssetsLength == originalAssetsLength
    v2VaultsGenerator.assetDeprecated(v2YfiVaultAddress) == False


def test_assets_addresses(v2VaultsGenerator):
    assetsAddresses = v2VaultsGenerator.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_set_position_spender_addresses(v2VaultsGenerator, management, rando):
    with brownie.reverts():
        v2VaultsGenerator.setPositionSpenderAddresses([ethZapAddress], {"from": rando})
    v2VaultsGenerator.setPositionSpenderAddresses([ethZapAddress], {"from": management})
    assert v2VaultsGenerator.positionSpenderAddresses(0) == ethZapAddress
    spenderAddresses = v2VaultsGenerator.getPositionSpenderAddresses()
    assert len(spenderAddresses) > 0
