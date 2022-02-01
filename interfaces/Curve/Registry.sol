// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

interface CurveRegistry {
  function get_pool_from_lp_token(address arg0) external view returns (address);

  function get_underlying_coins(address arg0)
    external
    view
    returns (address[8] memory);

  function get_virtual_price_from_lp_token(address arg0)
    external
    view
    returns (uint256);
}
