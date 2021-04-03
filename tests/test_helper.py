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
    yfi = interface.IERC20(yfiAddress)
    yfi.approve(ethZapAddress, 500, {"from": rando})
    helperProxy = Contract.from_abi("", helper, AllowancesHelper.abi)

    allowances = helperProxy.allowances(
        rando, [yfiAddress, threeCrvAddress], [ethZapAddress]
    )
    allowanceStruct = allowances[0]
    allowanceOwner = allowanceStruct[0]
    allowanceSpender = allowanceStruct[1]
    allowanceAmount = allowanceStruct[2]
    allowanceToken = allowanceStruct[3]
    assert allowanceToken == yfiAddress
    assert allowanceOwner == rando
    assert allowanceSpender == ethZapAddress
    assert allowanceAmount == 500
