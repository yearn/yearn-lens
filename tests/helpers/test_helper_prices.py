import pytest
from ..addresses import *
from conftest import usdcAddress, crvAddress


def test_tokens_prices(pricesHelper):
    """
    Solidity (Returns):
    struct TokenPrice {
        address tokenId;
        uint256 priceUsdc;
    }
    TokenPrice[]

    Brownie:
    List[(tokenId, priceUsdc)]
    """
    token_prices = pricesHelper.tokensPrices(
        [usdcAddress, crvAddress],
    )
    assert token_prices[0][0] == usdcAddress
    assert token_prices[0][1] > 0
    assert token_prices[1][0] == crvAddress
    assert token_prices[1][1] > 0


def test_tokens_prices_normalized_usdc(pricesHelper):
    """
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
    """
    token_prices = pricesHelper.tokensPricesNormalizedUsdc(
        [(usdcAddress, 1), (crvAddress, 1e12)]
    )
    assert token_prices[0][0] == usdcAddress
    assert token_prices[0][1] > 0
    assert token_prices[1][0] == crvAddress
    assert token_prices[1][1] > 0
