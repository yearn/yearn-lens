import pytest
import brownie

from web3 import Web3
from brownie import Contract, interface


@pytest.fixture
def allowancesHelper(AllowancesHelper, management):
    return AllowancesHelper.deploy({"from": management})


@pytest.fixture
def helper(Helper, managementList, allowancesHelper, management):
    helper = Helper.deploy(managementList, {"from": management})
    helper.setHelpers([allowancesHelper])
    return helper


def test_set_helpers(allowancesHelper, Helper, management, managementList):
    helper = Helper.deploy(managementList, {"from": management})
    assert len(helper.helpers()) == 0
    helper.setHelpers([allowancesHelper])
    assert len(helper.helpers()) > 0
    assert helper.helpers()[0] == allowancesHelper


def test_allowances(helper, rando, AllowancesHelper):
    yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
    threeCrvAddress = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"
    ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"
    wethAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    masterChefAddress = "0xbD17B1ce622d73bD438b9E658acA5996dc394b0d"

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

