import pytest
from brownie import Oracle


@pytest.fixture
def gov(accounts):
    yield accounts[0]


@pytest.fixture
def oracle(Oracle, gov):

    uniswapRouterAddress = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
    uniswapFactoryAddress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
    sushiswapRouterAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
    sushiswapFactoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
    curveRegistryAddress = "0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c"
    unitrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"  # Cream
    uniswapLpTokenAddress = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"  # USDC/WETH
    sushiswapLpTokenAddress = "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0"  # USDC/WETH

    usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

    return Oracle.deploy(
        uniswapRouterAddress,
        uniswapFactoryAddress,
        sushiswapRouterAddress,
        sushiswapFactoryAddress,
        curveRegistryAddress,
        unitrollerAddress,
        usdcAddress,
        {"from": gov},
    )

    return gov.deploy(Oracle)
