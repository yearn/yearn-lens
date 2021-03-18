import pytest
from brownie import Oracle


@pytest.fixture
def gov(accounts):
    yield accounts[0]
