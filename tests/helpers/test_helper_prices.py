import pytest

from brownie import accounts

@pytest.fixture
def prices_helper(PricesHelper, management):
    oracle_address = "0x83d95e0D5f402511dB06817Aff3f9eA88224B030"
    return PricesHelper.deploy(oracle_address, management, {"from": accounts[0]})

@pytest.fixture
def token_addresses():
    return {
        "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "crv": "0xD533a949740bb3306d119CC777fa900bA034cd52"
        }


def test_tokens_prices(prices_helper, token_addresses):
    '''
    Solidity (Returns):
    struct TokenPrice {
        address tokenId;
        uint256 priceUsdc;
    }
    TokenPrice[]

    Brownie:
    List[(tokenId, priceUsdc)]
    '''
    token_prices = prices_helper.tokensPrices(
        [token_addresses['usdc'], token_addresses['crv']],
        )
    assert token_prices[0][0] == token_addresses['usdc']
    assert token_prices[0][1] > 0
    assert token_prices[1][0] == token_addresses['crv']
    assert token_prices[1][1] > 0

def test_tokens_prices_normalized_usdc(prices_helper, token_addresses):
    '''
    Solidity (returns):
    struct Tokens {
      address tokenId;
      uint256 amount;
    }

    Brownie:
    List[(tokenId, priceUsdc)]

    refer to Oracle.sol:70
    usdc decimals: 6
    erc20 decimals: 18
    normalization is based on usdc decimals
    use 18-6 = 12 decimals for erc20 testing
    '''
    token_prices = prices_helper.tokensPricesNormalizedUsdc([
          (token_addresses['usdc'], 1),
          (token_addresses['crv'], 1e12)
        ])
    assert token_prices[0][0] == token_addresses['usdc']
    assert token_prices[0][1] > 0
    assert token_prices[1][0] == token_addresses['crv']
    assert token_prices[1][1] > 0
