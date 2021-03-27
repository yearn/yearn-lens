// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

interface IOracle {
    function getPriceUsdcRecommended(address tokenAddress)
        external
        view
        returns (uint256);

    function usdcAddress() external view returns (address);
}
