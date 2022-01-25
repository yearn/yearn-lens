import pytest

yCrvAddress = "0x5dbcF33D8c2E976c6b560249878e6F1491Bca25c"
ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"

@pytest.fixture
def delegatedBalanceMapping(DelegatedBalanceMapping, management):
    return DelegatedBalanceMapping.deploy({"from": management},)


def test_update_delegation_status_for_asset(delegatedBalanceMapping):
    assert delegatedBalanceMapping.assetBalanceIsDelegated(yCrvAddress) == False
    delegatedBalanceMapping.updateDelegationStatusForAsset(yCrvAddress, True)
    assert delegatedBalanceMapping.assetBalanceIsDelegated(yCrvAddress) == True
    delegatedBalanceMapping.updateDelegationStatusForAsset(yCrvAddress, False)
    assert delegatedBalanceMapping.assetBalanceIsDelegated(yCrvAddress) == False
