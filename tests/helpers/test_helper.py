import pytest
from brownie import Contract, interface

from ..addresses import *


@pytest.fixture
def allowancesHelper(AllowancesHelper, management):
    return AllowancesHelper.deploy({"from": management})


@pytest.fixture
def helper(Helper, allowancesHelper, management):
    helper = Helper.deploy({"from": management})
    helper.setHelpers([allowancesHelper])
    return helper


def test_set_helpers(allowancesHelper, Helper, management):
    helper = Helper.deploy({"from": management})
    assert len(helper.helpers()) == 0
    helper.setHelpers([allowancesHelper])
    assert len(helper.helpers()) > 0
    assert helper.helpers()[0] == allowancesHelper


def test_allowances(helper, rando, AllowancesHelper):

    yfi = interface.IERC20(yfiAddress)
    yfi.approve(ethZapAddress, 500, {"from": rando})

    threeCrv = interface.IERC20(threeCrvAddress)
    threeCrv.approve(ethZapAddress, 600, {"from": rando})

    wethAddress = interface.IERC20(threeCrvAddress)
    wethAddress.approve(masterChefAddress, 200, {"from": rando})

    helperProxy = Contract.from_abi("", helper, AllowancesHelper.abi)

    allowances = helperProxy.allowances(
        rando,
        [yfiAddress, wethAddress, threeCrvAddress],
        [ethZapAddress, masterChefAddress],
    )

    allowance1 = allowances[0]
    allowanceOwner1 = allowance1[0]
    allowanceSpender1 = allowance1[1]
    allowanceAmount1 = allowance1[2]
    allowanceToken1 = allowance1[3]
    assert allowanceToken1 == yfiAddress
    assert allowanceOwner1 == rando
    assert allowanceSpender1 == ethZapAddress
    assert allowanceAmount1 == 500

    allowance2 = allowances[1]
    allowanceOwner2 = allowance2[0]
    allowanceSpender2 = allowance2[1]
    allowanceAmount2 = allowance2[2]
    allowanceToken2 = allowance2[3]
    assert allowanceToken2 == threeCrvAddress
    assert allowanceOwner2 == rando
    assert allowanceSpender2 == ethZapAddress
    assert allowanceAmount2 == 600

    allowance3 = allowances[2]
    allowanceOwner3 = allowance3[0]
    allowanceSpender3 = allowance3[1]
    allowanceAmount3 = allowance3[2]
    allowanceToken3 = allowance3[3]
    assert allowanceToken3 == wethAddress
    assert allowanceOwner3 == rando
    assert allowanceSpender3 == masterChefAddress
    assert allowanceAmount3 == 200
