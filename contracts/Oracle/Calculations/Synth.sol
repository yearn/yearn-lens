// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.2;

import "../../Utilities/Ownable.sol";

interface AggregatorV3Interface {
  function latestRoundData()
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );
}

contract CalculationsSynth is Ownable {

    mapping (address => bool) public eurSynths;
    mapping (address => bool) public gbpSynths;
    mapping (address => bool) public chfSynths;
    mapping (address => bool) public audSynths;
    mapping (address => bool) public jpySynths;
    mapping (address => bool) public krwSynths;

    AggregatorV3Interface public eurChainlinkFeed;
    AggregatorV3Interface public gbpChainlinkFeed;
    AggregatorV3Interface public chfChainlinkFeed;
    AggregatorV3Interface public audChainlinkFeed;
    AggregatorV3Interface public jpyChainlinkFeed;
    AggregatorV3Interface public krwChainlinkFeed;

    constructor(
        address _eurChainlinkFeed,
        address _gbpChainlinkFeed,
        address _chfChainlinkFeed,
        address _audChainlinkFeed,
        address _jpyChainlinkFeed,
        address _krwChainlinkFeed
    ) {
        eurChainlinkFeed = AggregatorV3Interface(_eurChainlinkFeed);
        gbpChainlinkFeed = AggregatorV3Interface(_gbpChainlinkFeed);
        chfChainlinkFeed = AggregatorV3Interface(_chfChainlinkFeed);
        audChainlinkFeed = AggregatorV3Interface(_audChainlinkFeed);
        jpyChainlinkFeed = AggregatorV3Interface(_jpyChainlinkFeed);
        krwChainlinkFeed = AggregatorV3Interface(_krwChainlinkFeed);
    }

    function setEurFeed(address _eurChainlinkFeed) public onlyOwner {
        eurChainlinkFeed = AggregatorV3Interface(_eurChainlinkFeed);
    }

    function setGbpFeed(address _gbpChainlinkFeed) public onlyOwner {
        gbpChainlinkFeed = AggregatorV3Interface(_gbpChainlinkFeed);
    }

    function setChfFeed(address _chfChainlinkFeed) public onlyOwner {
        chfChainlinkFeed = AggregatorV3Interface(_chfChainlinkFeed);
    }

    function setAudFeed(address _audChainlinkFeed) public onlyOwner {
        audChainlinkFeed = AggregatorV3Interface(_audChainlinkFeed);
    }

    function setJpyFeed(address _jpyChainlinkFeed) public onlyOwner {
        jpyChainlinkFeed = AggregatorV3Interface(_jpyChainlinkFeed);
    }

    function setKrwFeed(address _krwChainlinkFeed) public onlyOwner {
        krwChainlinkFeed = AggregatorV3Interface(_krwChainlinkFeed);
    }

    function setSynths(
        address[] memory _eurSynths,
        address[] memory _gbpSynths,
        address[] memory _chfSynths,
        address[] memory _audSynths,
        address[] memory _jpySynths,
        address[] memory _krwSynths
    ) public onlyOwner {
        for (uint i = 0; i < _eurSynths.length; i++) {
            eurSynths[_eurSynths[i]] = true;
        }
        for (uint i = 0; i < _gbpSynths.length; i++) {
            gbpSynths[_gbpSynths[i]] = true;
        }
        for (uint i = 0; i < _chfSynths.length; i++) {
            chfSynths[_chfSynths[i]] = true;
        }
        for (uint i = 0; i < _audSynths.length; i++) {
            audSynths[_audSynths[i]] = true;
        }
        for (uint i = 0; i < _jpySynths.length; i++) {
            jpySynths[_jpySynths[i]] = true;
        }
        for (uint i = 0; i < _krwSynths.length; i++) {
            krwSynths[_krwSynths[i]] = true;
        }
    }

    function setEurSynth(address synthAddress, bool isSynth) public onlyOwner {
        eurSynths[synthAddress] = isSynth;
    }

    function setGbpSynth(address synthAddress, bool isSynth) public onlyOwner {
        gbpSynths[synthAddress] = isSynth;
    }

    function setChfSynth(address synthAddress, bool isSynth) public onlyOwner {
        chfSynths[synthAddress] = isSynth;
    }

    function setAudSynth(address synthAddress, bool isSynth) public onlyOwner {
        audSynths[synthAddress] = isSynth;
    }

    function setJpySynth(address synthAddress, bool isSynth) public onlyOwner {
        jpySynths[synthAddress] = isSynth;
    }

    function setKrwSynth(address synthAddress, bool isSynth) public onlyOwner {
        krwSynths[synthAddress] = isSynth;
    }

    function getEurPrice() public view returns (int256) {
        (,int price,,,) = eurChainlinkFeed.latestRoundData();
        return price;
    }

    function getGbpPrice() public view returns (int256) {
        (,int price,,,) = gbpChainlinkFeed.latestRoundData();
        return price;
    }

    function getChfPrice() public view returns (int256) {
        (,int price,,,) = chfChainlinkFeed.latestRoundData();
        return price;
    }

    function getAudPrice() public view returns (int256) {
        (,int price,,,) = audChainlinkFeed.latestRoundData();
        return price;
    }

    function getJpyPrice() public view returns (int256) {
        (,int price,,,) = jpyChainlinkFeed.latestRoundData();
        return price;
    }

    function getKrwPrice() public view returns (int256) {
        (,int price,,,) = krwChainlinkFeed.latestRoundData();
        return price;
    }

    function getPriceUsdc(address tokenAddress) public view returns (int256) {
        int256 price;

        if (eurSynths[tokenAddress]) {
            price = getEurPrice();
        } else if (gbpSynths[tokenAddress]) {
            price = getGbpPrice();
        } else if (chfSynths[tokenAddress]) {
            price = getChfPrice();
        } else if (audSynths[tokenAddress]) {
            price = getAudPrice();
        } else if (jpySynths[tokenAddress]) {
            price = getJpyPrice();
        } else if (krwSynths[tokenAddress]) {
            price = getKrwPrice();
        } else {
            revert("token not a synth");
        }

        return price / 10 ** 2;
    }
}
