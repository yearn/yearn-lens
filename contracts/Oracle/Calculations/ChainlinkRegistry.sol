// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "../../Utilities/Ownable.sol";

interface ChainlinkFeed {
    function latestAnswer() external view returns (int256);
}

contract CalculationsChainlinkRegistry is Ownable {
    struct TokenFeedData {
        address token;
        address feed;
    }

    mapping(address => address) public tokenToFeed;

    function setTokenFeed(address tokenAddress, address feed)
        external
        onlyOwner
    {
        tokenToFeed[tokenAddress] = feed;
    }

    function setTokenFeeds(TokenFeedData[] memory tokenFeedData)
        external
        onlyOwner
    {
        for (uint256 idx; idx < tokenFeedData.length; idx++) {
            TokenFeedData memory tokenFeedDatum = tokenFeedData[idx];
            tokenToFeed[tokenFeedDatum.token] = tokenFeedDatum.feed;
        }
    }

    function getPriceUsdc(address tokenAddress) public view returns (uint256) {
        address feed = tokenToFeed[tokenAddress];
        require(feed != address(0));
        return uint256(ChainlinkFeed(feed).latestAnswer()) / 10**2;
    }
}
