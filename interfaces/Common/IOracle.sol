// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

interface IOracle {
    function getPriceUsdcRecommended(address tokenAddress)
        external
        view
        returns (uint256);

    function getNormalizedValueUsdc(address tokenAddress, uint256 amount)
        external
        view
        returns (uint256);

    function usdcAddress() external view returns (address);
}
