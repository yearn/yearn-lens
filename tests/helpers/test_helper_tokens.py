import pytest

from brownie import Contract, interface, accounts


def test_set_helpers(BalancesHelper, iv2Registry):
    factoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
    routerAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
    oracleAddress = "0x83d95e0D5f402511dB06817Aff3f9eA88224B030"
    usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    usdcVaultAddress = iv2Registry.latestVault(usdcAddress)
    crvAddress = "0xD533a949740bb3306d119CC777fa900bA034cd52"
    wbtcAddress = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"

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
        ],
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
        ],
    )
    crvMetadata = tokensMetadata[0]
    wbtcMetadata = tokensMetadata[1]
    assert crvMetadata[0] == crvAddress
    assert crvMetadata[1] == "Curve DAO Token"
    assert crvMetadata[2] == "CRV"
    assert crvMetadata[3] == 18
