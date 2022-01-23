// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

import "../../Manageable.sol";

interface IOracle {
    function getPriceUsdcRecommended(address tokenAddress)
        external
        view
        returns (uint256);

    function getNormalizedValueUsdc(address tokensAddress, uint256 amount)
        external
        view
        returns (uint256);
}

contract PricesHelper is Manageable {
    address public oracleAddress;

    struct TokenPrice {
        address tokenId;
        uint256 priceUsdc;
    }

    struct Tokens {
      address tokenId;
      uint256 amount;
    }

    constructor(address _oracleAddress, address _managementListAddress) Manageable(_managementListAddress) {
        require(_oracleAddress != address(0), "Missing oracle address");
        oracleAddress = _oracleAddress;
    }

    function tokensPrices(address[] memory tokensAddresses)
        external
        view
        returns (TokenPrice[] memory)
    {
        TokenPrice[] memory _tokensPrices =
            new TokenPrice[](tokensAddresses.length);
        for (
            uint256 tokenIdx = 0;
            tokenIdx < tokensAddresses.length;
            tokenIdx++
        ) {
            address tokenAddress = tokensAddresses[tokenIdx];
            _tokensPrices[tokenIdx] = TokenPrice({
                tokenId: tokenAddress,
                priceUsdc: IOracle(oracleAddress).getPriceUsdcRecommended(tokenAddress)
            });
        }
        return _tokensPrices;
    }

    function tokensPricesNormalizedUsdc(Tokens[] memory tokens)
        external
        view
        returns (TokenPrice[] memory)
    {
        TokenPrice[] memory _tokenPricesNormalized =
            new TokenPrice[](tokens.length);
        for (
            uint256 tokenIdx = 0;
            tokenIdx < tokens.length;
            tokenIdx++
        ) {
            address tokenAddress = tokens[tokenIdx].tokenId;
            uint256 amount = tokens[tokenIdx].amount;
            _tokenPricesNormalized[tokenIdx] = TokenPrice({
                tokenId: tokenAddress,
                priceUsdc: IOracle(oracleAddress).getNormalizedValueUsdc(tokenAddress, amount)
            });
        }
        return _tokenPricesNormalized;
    }

    function updateOracleAddress(address _oracleAddress) external onlyManagers {
        oracleAddress = _oracleAddress;
    }

}
