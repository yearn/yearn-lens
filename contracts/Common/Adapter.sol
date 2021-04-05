// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.2;

import "../../interfaces/Common/IOracle.sol";
import "../../interfaces/Common/IERC20.sol";
import "../Utilities/Manageable.sol";

contract Adapter is Manageable {
    IOracle public oracle;
    address public registryAddress;
    address[] public positionSpenderAddresses;

    struct AdapterInfo {
        address id;
        string typeId;
        string categoryId;
    }

    struct Position {
        address assetId;
        string categoryId;
        uint256 balance;
        uint256 balanceUsdc;
        TokenPosition tokenPosition;
        Allowance[] allowances;
    }

    struct Token {
        address id;
        string name;
        string symbol;
        uint8 decimals;
        uint256 priceUsdc;
    }

    struct TokenPosition {
        address tokenId;
        uint256 balance;
        uint256 balanceUsdc;
        Allowance[] allowances;
    }

    struct Allowance {
        address owner;
        address spender;
        uint256 amount;
    }

    function tokenPositionAllowances(
        address accountAddress,
        address tokenAddress,
        address assetAddress
    ) public view returns (Allowance[] memory) {
        IERC20 _token = IERC20(tokenAddress);
        Allowance[] memory allowances = new Allowance[](1);
        uint256 allowanceAmount =
            _token.allowance(accountAddress, assetAddress);
        Allowance memory allowance =
            Allowance({
                owner: accountAddress,
                spender: assetAddress,
                amount: allowanceAmount
            });
        allowances[0] = allowance;
        return allowances;
    }

    function positionAllowances(address accountAddress, address assetAddress)
        public
        view
        returns (Allowance[] memory)
    {
        IERC20 asset = IERC20(assetAddress);
        uint256 numberOfSpenders = positionSpenderAddresses.length;
        Allowance[] memory allowances = new Allowance[](numberOfSpenders);
        for (
            uint256 spenderIdx = 0;
            spenderIdx < numberOfSpenders;
            spenderIdx++
        ) {
            address spenderAddress = positionSpenderAddresses[spenderIdx];
            uint256 allowanceAmount =
                asset.allowance(accountAddress, spenderAddress);
            Allowance memory allowance =
                Allowance({
                    owner: accountAddress,
                    spender: spenderAddress,
                    amount: allowanceAmount
                });
            allowances[spenderIdx] = allowance;
        }
        return allowances;
    }

    function token(address tokenAddress) internal view returns (Token memory) {
        IERC20 _token = IERC20(tokenAddress);
        return
            Token({
                id: tokenAddress,
                name: _token.name(),
                symbol: _token.symbol(),
                decimals: _token.decimals(),
                priceUsdc: oracle.getPriceUsdcRecommended(tokenAddress)
            });
    }

    function setPositionSpenderAddresses(address[] memory addresses)
        public
        onlyManagers
    {
        positionSpenderAddresses = addresses;
    }

    constructor(
        address _registryAddress,
        address _oracleAddress,
        address _managementListAddress
    ) Manageable(_managementListAddress) {
        require(
            _managementListAddress != address(0),
            "Missing management list address"
        );
        require(_registryAddress != address(0), "Missing registry address");
        require(_oracleAddress != address(0), "Missing oracle address");
        registryAddress = _registryAddress;
        oracle = IOracle(_oracleAddress);
    }
}
