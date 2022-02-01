// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity 0.8.11;
import "../../Utilities/AddressesProviderConsumer.sol";

interface IAddressResolver {
  function getAddress(bytes32) external view returns (address);
}

interface ISynth {
  function target() external view returns (address);
}

interface ISynthetix {
  function availableSynthCount() external view returns (uint256);

  function availableSynths(uint256) external view returns (address);
}

interface ISynthTarget {
  function currencyKey() external view returns (bytes32);
}

interface IExchangeRates {
  function ratesForCurrencies(bytes32[] calldata)
    external
    view
    returns (uint256[] memory);
}

contract CalculationsSynth is AddressesProviderConsumer {
  constructor(address _addressesProviderAddress)
    AddressesProviderConsumer(_addressesProviderAddress)
  {}

  function getAddressByName(string memory nameString)
    public
    view
    returns (address)
  {
    bytes32 name = bytes32(bytes(nameString));
    address resolvedAddress = IAddressResolver(
      addressById("SYNTHETIX_ADDRESS_RESOLVER")
    ).getAddress(name);
    address targetAddress = targetAddressByProxyAddress(resolvedAddress);
    if (targetAddress != address(0)) {
      return targetAddress;
    }
    return resolvedAddress;
  }

  function synthetixProxyTarget() public view returns (ISynthetix) {
    return ISynthetix(getAddressByName("ProxyERC20"));
  }

  function exchangeRates() public view returns (IExchangeRates) {
    return IExchangeRates(getAddressByName("ExchangeRates"));
  }

  function synthsAddresses()
    external
    view
    returns (address[] memory _synthsAddresses)
  {
    ISynthetix synthetix = synthetixProxyTarget();
    uint256 availableSynthCount = synthetix.availableSynthCount();
    _synthsAddresses = new address[](availableSynthCount);
    for (uint256 synthIdx; synthIdx < availableSynthCount; synthIdx++) {
      _synthsAddresses[synthIdx] = synthetix.availableSynths(synthIdx);
    }
  }

  function targetAddressByProxyAddress(address contractAddress)
    public
    view
    returns (address)
  {
    try ISynth(contractAddress).target() returns (address targetAddress) {
      return targetAddress;
    } catch {
      return address(0);
    }
  }

  function isSynth(address tokenAddress) external view returns (bool) {
    address targetAddress = targetAddressByProxyAddress(tokenAddress);
    if (targetAddress == address(0)) {
      return false;
    }
    ISynthetix synthetix = synthetixProxyTarget();
    uint256 availableSynthCount = synthetix.availableSynthCount();
    for (uint256 synthIdx; synthIdx < availableSynthCount; synthIdx++) {
      address synthAddress = synthetix.availableSynths(synthIdx);
      if (targetAddress == synthAddress) {
        return true;
      }
    }
    return false;
  }

  function currencyKeyByTokenAddress(address tokenAddress)
    public
    view
    returns (bytes32)
  {
    address targetAddress = targetAddressByProxyAddress(tokenAddress);
    if (targetAddress == address(0)) {
      revert("token not a synth");
    }
    return ISynthTarget(targetAddress).currencyKey();
  }

  function getPriceUsdc(address tokenAddress) external view returns (uint256) {
    bytes32 currencyKey = currencyKeyByTokenAddress(tokenAddress);
    bytes32[] memory currenciesKeys = new bytes32[](1);
    currenciesKeys[0] = currencyKey;
    uint256[] memory rates = exchangeRates().ratesForCurrencies(currenciesKeys);
    return rates[0] / 10**12;
  }
}
