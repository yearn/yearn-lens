// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.2;

/**
 * @dev Interface of the ERC20 standard as defined in the EIP.
 */
interface IERC20 {
  function totalSupply() external view returns (uint256);

  function balanceOf(address account) external view returns (uint256);

  function transfer(address recipient, uint256 amount) external returns (bool);

  function allowance(address owner, address spender)
    external
    view
    returns (uint256);

  function approve(address spender, uint256 amount) external returns (bool);

  function transferFrom(
    address sender,
    address recipient,
    uint256 amount
  ) external returns (bool);

  event Transfer(address indexed from, address indexed to, uint256 value);
  event Approval(address indexed owner, address indexed spender, uint256 value);
}

interface IERC20Metadata is IERC20 {
  function name() external view returns (string memory);

  function symbol() external view returns (string memory);

  function decimals() external view returns (uint8);
}

interface IStdReference {
  /// A structure returned whenever someone requests for standard reference data.
  struct ReferenceData {
    uint256 rate; // base/quote exchange rate, multiplied by 1e18.
    uint256 lastUpdatedBase; // UNIX epoch of the last time when base price gets updated.
    uint256 lastUpdatedQuote; // UNIX epoch of the last time when quote price gets updated.
  }

  /// Returns the price data for the given base/quote pair. Revert if not available.
  function getReferenceData(string memory _base, string memory _quote)
    external
    view
    returns (ReferenceData memory);

  /// Similar to getReferenceData, but with multiple base/quote pairs at once.
  function getReferenceDataBulk(string[] memory _bases, string[] memory _quotes)
    external
    view
    returns (ReferenceData[] memory);
}

contract CalculationsBand {
  address public bandOracle;

  constructor(address _bandOracle) {
    bandOracle = _bandOracle;
  }

  function getPriceUsdc(address tokenAddress) public view returns (uint256) {
    IStdReference oracle = IStdReference(bandOracle);
    string memory symbol = IERC20Metadata(tokenAddress).symbol();
    string memory usdcSymbol = "USDC";
    IStdReference.ReferenceData memory referenceData = oracle.getReferenceData(
      symbol,
      usdcSymbol
    );
    return referenceData.rate / 10**12;
  }
}
