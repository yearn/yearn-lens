// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

interface AToken {
    function underlyingAssetAddress() external view returns (address);
}
