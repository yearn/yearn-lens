import pytest

from ..addresses import *


@pytest.fixture
def delegatedBalanceMapping(DelegatedBalanceMapping, management):
    return DelegatedBalanceMapping.deploy({"from": management},)


def test_update_delegation_status_for_asset(delegatedBalanceMapping):
    assert delegatedBalanceMapping.assetBalanceIsDelegated(yCrvAddress) == False
    delegatedBalanceMapping.updateDelegationStatusForAsset(yCrvAddress, True)
    assert delegatedBalanceMapping.assetBalanceIsDelegated(yCrvAddress) == True
    delegatedBalanceMapping.updateDelegationStatusForAsset(yCrvAddress, False)
    assert delegatedBalanceMapping.assetBalanceIsDelegated(yCrvAddress) == False
