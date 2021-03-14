import pytest
from brownie import Oracle


@pytest.fixture
def gov(accounts):
    yield accounts[0]


@pytest.fixture
def oracle(Oracle, gov):
    return gov.deploy(Oracle)
