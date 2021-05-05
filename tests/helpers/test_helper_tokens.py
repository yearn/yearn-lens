import pytest
import brownie

from web3 import Web3
from brownie import Contract, interface, accounts


def test_set_helpers(BalancesHelper, PairsHelper, UniqueAddressesHelper, management):
    unique = UniqueAddressesHelper.deploy({"from": accounts[0]})
    factoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
    routerAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
    oracleAddress = "0x83d95e0D5f402511dB06817Aff3f9eA88224B030"
    wethAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    pairsHelper = PairsHelper.deploy(wethAddress, unique, {"from": accounts[0]})

    balancesHelper = BalancesHelper.deploy(
        oracleAddress, pairsHelper, {"from": accounts[0]}
    )
    print(
        balancesHelper.tokensBalances(
            "0x253c5cBDd08838DaD5493D511E17Aa1ac5eAB51B", factoryAddress, 2, 0
        )
    )
