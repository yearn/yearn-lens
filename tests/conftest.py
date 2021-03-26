import pytest
from brownie import Oracle
from eth_account import Account
from brownie import web3


@pytest.fixture
def gov(accounts):
    yield accounts.at(web3.ens.resolve("ychad.eth"), force=True)


@pytest.fixture
def managementList(ManagementList, management):
    return ManagementList.deploy("Managemenet list", {"from": management})


@pytest.fixture
def oracle(
    Oracle,
    management,
    managementList,
    CalculationsSushiswap,
    CalculationsCurve,
    CalculationsIronBank,
):

    uniswapRouterAddress = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
    uniswapFactoryAddress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
    sushiswapRouterAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
    sushiswapFactoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
    curveRegistryAddress = "0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c"
    unitrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
    usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

    oracle = Oracle.deploy(managementList, usdcAddress, {"from": management})
    calculationsSushiswap = CalculationsSushiswap.deploy(
        uniswapRouterAddress,
        uniswapFactoryAddress,
        sushiswapRouterAddress,
        sushiswapFactoryAddress,
        usdcAddress,
        {"from": management},
    )
    calculationsCurve = CalculationsCurve.deploy(
        curveRegistryAddress, oracle, {"from": management}
    )
    calculationsIronBank = CalculationsIronBank.deploy(
        unitrollerAddress, oracle, {"from": management}
    )
    oracle.setCalculations(
        [calculationsCurve, calculationsIronBank, calculationsSushiswap]
    )
    return oracle


@pytest.fixture
def management(accounts):
    yield accounts[0]


@pytest.fixture
def chad(accounts):
    yield accounts[1]


@pytest.fixture
def rando(accounts):
    yield Account.create().address
