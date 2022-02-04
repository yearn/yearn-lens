// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface Pair {
    function factory() external view returns (address);

    function token0() external view returns (address);

    function token1() external view returns (address);

    function totalSupply() external view returns (uint256);

    function decimals() external view returns (uint8);

    function getReserves()
        external
        view
        returns (
            uint112,
            uint112,
            uint32
        );
}
