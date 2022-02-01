// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;
import "../../Utilities/AddressesProviderConsumer.sol";

interface IUnitroller {
  function getAllMarkets() external view returns (address[] memory);
}

interface ICyToken {
  function underlying() external view returns (address);

  function exchangeRateStored() external view returns (uint256);

  function decimals() external view returns (uint8);
}

interface IERC20 {
  function decimals() external view returns (uint8);
}

interface IOracle {
  function getPriceUsdcRecommended(address tokenAddress)
    external
    view
    returns (uint256);
}

contract CalculationsIronBank is AddressesProviderConsumer {
  string[] public unitrollerIds;

  constructor(address _addressesProviderAddress)
    AddressesProviderConsumer(_addressesProviderAddress)
  {}

  function getIronBankMarkets(address unitrollerAddress)
    public
    view
    returns (address[] memory)
  {
    return IUnitroller(unitrollerAddress).getAllMarkets();
  }

  function addUnitroller(string memory unitrollerId) public onlyOwner {
    unitrollerIds.push(unitrollerId);
  }

  function addUnitrollers(string[] memory _unitrollerIds) external onlyOwner {
    for (
      uint256 unitrollerIdx;
      unitrollerIdx < _unitrollerIds.length;
      unitrollerIdx++
    ) {
      string memory unitrollerId = _unitrollerIds[unitrollerIdx];
      unitrollerIds.push(unitrollerId);
    }
  }

  function isIronBankMarket(address unitrollerAddress, address tokenAddress)
    public
    view
    returns (bool)
  {
    address[] memory ironBankMarkets = getIronBankMarkets(unitrollerAddress);
    uint256 numIronBankMarkets = ironBankMarkets.length;
    for (uint256 marketIdx = 0; marketIdx < numIronBankMarkets; marketIdx++) {
      address marketAddress = ironBankMarkets[marketIdx];
      if (tokenAddress == marketAddress) {
        return true;
      }
    }
    return false;
  }

  function getIronBankMarketPriceUsdc(address tokenAddress)
    public
    view
    returns (uint256)
  {
    ICyToken cyToken = ICyToken(tokenAddress);
    uint256 exchangeRateStored = cyToken.exchangeRateStored();
    address underlyingTokenAddress = cyToken.underlying();
    uint256 decimals = cyToken.decimals();
    IERC20 underlyingToken = IERC20(underlyingTokenAddress);
    uint8 underlyingTokenDecimals = underlyingToken.decimals();

    IOracle oracle = IOracle(addressById("ORACLE"));
    uint256 underlyingTokenPrice = oracle.getPriceUsdcRecommended(
      underlyingTokenAddress
    );

    uint256 price = (underlyingTokenPrice * exchangeRateStored) /
      10**(underlyingTokenDecimals + decimals);
    return price;
  }

  function getPriceUsdc(address tokenAddress) public view returns (uint256) {
    for (
      uint256 unitrollerIdx = 0;
      unitrollerIdx < unitrollerIds.length;
      unitrollerIdx++
    ) {
      address unitrollerAddress = addressById(unitrollerIds[unitrollerIdx]);
      if (isIronBankMarket(unitrollerAddress, tokenAddress)) {
        return getIronBankMarketPriceUsdc(tokenAddress);
      }
    }
    revert();
  }
}
