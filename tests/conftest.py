import pytest
from brownie import Oracle
from eth_account import Account


@pytest.fixture
def gov(accounts):
    yield accounts[0]


@pytest.fixture
def chad(accounts):
    yield accounts[1]


@pytest.fixture
def rando(accounts):
    yield Account.create().address
