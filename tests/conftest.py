import pytest


@pytest.fixture
def gov(accounts):
    yield accounts[0]
