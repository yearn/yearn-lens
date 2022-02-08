import pytest
from brownie import Contract, accounts, interface

from ..addresses import *


def test_set_helpers(BalancesHelper, iv2Registry):
    usdcVaultAddress = iv2Registry.latestVault(usdcAddress)
    balancesHelper = BalancesHelper.deploy(oracleAddress, {"from": accounts[0]})

    # Test tokensBalances
    balances = balancesHelper.tokensBalances(
        usdcVaultAddress,
        [
            usdcAddress,
        ],
    )
    usdcVaultBalance = balances[0]
    tokenId = usdcVaultBalance[0]
    priceUsdc = usdcVaultBalance[1]
    balance = usdcVaultBalance[2]
    balanceUsdc = usdcVaultBalance[3]
    assert tokenId == usdcAddress
    assert priceUsdc > 900000
    assert balance > 0
    assert balanceUsdc > 0

    # Test tokensPrices
    tokensPrices = balancesHelper.tokensPrices(
        [
            crvAddress,
            wbtcAddress,
        ]
    )
    crvPrice = tokensPrices[0]
    wbtcPrice = tokensPrices[1]
    assert crvPrice[0] == crvAddress
    assert crvPrice[1] > 0
    assert wbtcPrice[0] == wbtcAddress
    assert wbtcPrice[1] > 0

    # Test tokensMetadata
    tokensMetadata = balancesHelper.tokensMetadata(
        [
            crvAddress,
            wbtcAddress,
        ]
    )
    crvMetadata = tokensMetadata[0]
    assert crvMetadata[0] == crvAddress
    assert crvMetadata[1] == "Curve DAO Token"
    assert crvMetadata[2] == "CRV"
    assert crvMetadata[3] == 18
