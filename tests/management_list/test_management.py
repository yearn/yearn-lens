import pytest
import brownie

from brownie import ManagementList, ZERO_ADDRESS


@pytest.fixture
def manageable(ManagementList, gov):
    return ManagementList.deploy("Managers", {"from": gov})


def test_initialization(manageable, gov):
    assert manageable.managersCount() == 1
    assert manageable.managerAddressByIdx(1) == gov
    assert manageable.managerIdxByAddress(gov) == 1
    assert manageable.managersCount() == 1
    assert manageable.managersList()[0] == gov


def test_managers_list(manageable, gov, chad, rando):
    manageable.addManager(chad, {"from": gov})
    manageable.addManager(rando, {"from": gov})
    assert manageable.managersCount() == 3
    assert manageable.managersList()[0] == gov
    assert manageable.managersList()[1] == chad
    assert manageable.managersList()[2] == rando
    assert len(manageable.managersList()) == 3


def test_is_manager(manageable, gov, rando):
    assert manageable.isManager(gov)
    assert not manageable.isManager(rando)


def test_add_manager(manageable, gov, chad, rando):
    # Randos cannot add managers
    with brownie.reverts():
        manageable.addManager(rando, {"from": rando})
    assert manageable.managersCount() == 1

    # Managers can add managers
    manageable.addManager(rando, {"from": gov})
    assert len(manageable.managersList()) == 2
    assert manageable.managersCount() == 2

    # New managers can add managers
    manageable.addManager(chad, {"from": rando})
    assert manageable.managersCount() == 3

    # Can't add managers that already exist
    with brownie.reverts():
        manageable.addManager(chad, {"from": rando})
    assert manageable.managersCount() == 3


def test_remove_manager(manageable, gov, chad, rando):
    manageable.addManager(chad, {"from": gov})
    assert manageable.managersCount() == 2

    # Randos cannot remove managers
    with brownie.reverts():
        manageable.removeManager(chad, {"from": rando})

    # Managers cannot remove the owner
    with brownie.reverts():
        manageable.removeManager(gov, {"from": chad})

    # Managers can remove mangers
    manageable.removeManager(chad, {"from": chad})
    assert manageable.managersCount() == 1

    # Non-managers cannot be removed
    with brownie.reverts():
        manageable.removeManager(chad, {"from": gov})


def test_reset_managers(manageable, gov, chad, rando):
    manageable.addManager(chad, {"from": gov})
    manageable.addManager(rando, {"from": gov})
    assert manageable.managersCount() == 3

    # Managers cannot reset managers
    with brownie.reverts():
        manageable.resetManagers({"from": chad})

    # Owners can reset managers
    manageable.resetManagers({"from": gov})
    assert manageable.managersCount() == 1
    assert manageable.managerAddressByIdx(1) == gov
    assert manageable.managerAddressByIdx(2) == ZERO_ADDRESS
    assert manageable.managerAddressByIdx(3) == ZERO_ADDRESS
    assert manageable.managerIdxByAddress(chad) == 0
    assert manageable.managerIdxByAddress(rando) == 0
    assert manageable.managerIdxByAddress(gov) == 1
    assert manageable.isManager(gov)
    assert not manageable.isManager(chad)
    assert not manageable.isManager(rando)
