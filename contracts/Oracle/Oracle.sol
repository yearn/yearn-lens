// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.2;

import "../Utilities/Manageable.sol";

contract Oracle is Manageable {
    address[] private _calculations;
    address public usdcAddress;

    constructor(address _managementListAddress, address _usdcAddress)
        Manageable(_managementListAddress)
    {
        usdcAddress = _usdcAddress;
    }

    /**
     * The oracle supports an array of calculation contracts. Each calculation contract must implement getPriceUsdc().
     * When setting calculation contracts all calculations must be set at the same time (we intentionally do not support for adding/removing calculations).
     * The order of calculation contracts matters as it determines the order preference in the cascading fallback mechanism.
     */
    function setCalculations(address[] memory calculationAddresses)
        public
        onlyManagers
    {
        _calculations = calculationAddresses;
    }

    function calculations() external view returns (address[] memory) {
        return (_calculations);
    }

    function getPriceUsdcRecommended(address tokenAddress)
        public
        view
        returns (uint256)
    {
        (bool success, bytes memory data) =
            address(this).staticcall(
                abi.encodeWithSignature("getPriceUsdc(address)", tokenAddress)
            );
        if (success) {
            return abi.decode(data, (uint256));
        }
        revert("Oracle: No price found");
    }

    /**
     * Cascading fallback proxy
     *
     * Loop through all contracts in _calculations and attempt to forward the method call to each underlying contract.
     * This allows users to call getPriceUsdc() on the oracle contract and the result of the first non-reverting contract that
     * implements getPriceUsdc() will be returned.
     *
     * This mechanism also exposes all public methods for calculation contracts. This allows a user to
     * call oracle.isIronBankMarket() or oracle.isCurveLpToken() even though these methods live on different contracts.
     */
    fallback() external {
        for (uint256 i = 0; i < _calculations.length; i++) {
            address calculation = _calculations[i];
            assembly {
                let _target := calculation
                calldatacopy(0, 0, calldatasize())
                let success := staticcall(
                    gas(),
                    _target,
                    0,
                    calldatasize(),
                    0,
                    0
                )
                returndatacopy(0, 0, returndatasize())
                if success {
                    return(0, returndatasize())
                }
            }
        }
        revert("Oracle: Fallback proxy failed to return data");
    }
}
