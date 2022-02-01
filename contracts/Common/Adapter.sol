// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.2;

import "../../interfaces/Common/IOracle.sol";
import "../../interfaces/Common/IERC20.sol";
import "../Utilities/Ownable.sol";

contract Adapter is Ownable {
  IOracle public oracle;
  address public registryAddress;
  address[] public positionSpenderAddresses;
  mapping(address => bool) public assetDeprecated;
  uint256 public numberOfDeprecatedAssets;

  struct AdapterInfo {
    address id;
    string typeId;
    string categoryId;
  }

  struct TokenAmount {
    uint256 amount;
    uint256 amountUsdc;
  }

  /**
   * High level information about an asset
   */
  struct AssetStatic {
    address id; // Asset address
    string typeId; // Asset typeId (for example "v2Vault" or "ironBankMarket")
    string name; // Asset Name
    string version; // Asset version
    Token token;
  }

  struct Position {
    address assetId;
    address tokenId;
    string typeId;
    uint256 balance;
    TokenAmount accountTokenBalance;
    TokenAmount underlyingTokenBalance;
    Allowance[] tokenAllowances;
    Allowance[] assetAllowances;
  }

  struct Token {
    address id; // token address
    string name; // token name
    string symbol; // token symbol
    uint8 decimals; // token decimals
  }

  struct Allowance {
    address owner;
    address spender;
    uint256 amount;
  }

  function tokenAllowances(
    address accountAddress,
    address tokenAddress,
    address assetAddress
  ) public view returns (Allowance[] memory) {
    IERC20 _token = IERC20(tokenAddress);
    Allowance[] memory allowances = new Allowance[](1);
    uint256 allowanceAmount = _token.allowance(accountAddress, assetAddress);
    Allowance memory allowance = Allowance({
      owner: accountAddress,
      spender: assetAddress,
      amount: allowanceAmount
    });
    allowances[0] = allowance;
    return allowances;
  }

  function assetAllowances(address accountAddress, address assetAddress)
    public
    view
    returns (Allowance[] memory)
  {
    IERC20 _asset = IERC20(assetAddress);
    uint256 numberOfSpenders = positionSpenderAddresses.length;
    Allowance[] memory allowances = new Allowance[](numberOfSpenders);
    for (uint256 spenderIdx = 0; spenderIdx < numberOfSpenders; spenderIdx++) {
      address spenderAddress = positionSpenderAddresses[spenderIdx];
      uint256 allowanceAmount = _asset.allowance(
        accountAddress,
        spenderAddress
      );
      Allowance memory allowance = Allowance({
        owner: accountAddress,
        spender: spenderAddress,
        amount: allowanceAmount
      });
      allowances[spenderIdx] = allowance;
    }
    return allowances;
  }

  function tokenMetadata(address tokenAddress)
    internal
    view
    returns (Token memory)
  {
    IERC20 _token = IERC20(tokenAddress);
    return
      Token({
        id: tokenAddress,
        name: _token.name(),
        symbol: _token.symbol(),
        decimals: _token.decimals()
      });
  }

  function setAssetDeprecated(address assetAddress, bool newDeprecationStatus)
    public
    onlyOwner
  {
    bool currentDeprecationStatus = assetDeprecated[assetAddress];
    if (currentDeprecationStatus == newDeprecationStatus) {
      revert("Adapter: Unable to change asset deprecation status");
    }
    if (newDeprecationStatus == true) {
      numberOfDeprecatedAssets++;
    } else {
      numberOfDeprecatedAssets--;
    }
    assetDeprecated[assetAddress] = newDeprecationStatus;
  }

  function setPositionSpenderAddresses(address[] memory addresses)
    public
    onlyOwner
  {
    positionSpenderAddresses = addresses;
  }

  constructor(address _registryAddress, address _oracleAddress) {
    require(_registryAddress != address(0), "Missing registry address");
    require(_oracleAddress != address(0), "Missing oracle address");
    registryAddress = _registryAddress;
    oracle = IOracle(_oracleAddress);
  }
}
