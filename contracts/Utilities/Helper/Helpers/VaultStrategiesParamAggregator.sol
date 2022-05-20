// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;
import "../../AddressesProviderConsumer.sol";

interface StrategyHelper {
    function assetStrategiesLength(address assetAddress)
        external
        view
        returns (uint256);
}

interface IVault {
    struct VaultStrategyParams {
        uint256 performanceFee; // Strategist's fee (basis points)
        uint256 activation; // Activation block.timestamp
        uint256 debtRatio; // Maximum borrow amount (in BPS of total assets)
        uint256 minDebtPerHarvest; // Lower limit on the increase of debt since last harvest
        uint256 maxDebtPerHarvest; // Upper limit on the increase of debt since last harvest
        uint256 lastReport; // block.timestamp of the last time a report occured
        uint256 totalDebt; // Total outstanding debt that Strategy has
        uint256 totalGain; // Total returns that Strategy has realized for Vault
        uint256 totalLoss; // Total losses that Strategy has realized for Vault
    }

    function strategies(address)
        external
        view
        returns (VaultStrategyParams memory);

    function withdrawalQueue(uint256 arg0) external view returns (address);
}

interface IStrategy {
    function name() external view returns (string memory);
}

contract VaultStrategiesParamAggregator is AddressesProviderConsumer {
    struct StrategyInfo {
        address strategyAddress;
        string name;
        IVault.VaultStrategyParams params;
    }

    constructor(address _addressesProviderAddress)
        AddressesProviderConsumer(_addressesProviderAddress)
    {}

    function strategyHelper() public view returns (StrategyHelper) {
        return StrategyHelper(addressById("HELPER"));
    }

    function assetVaultStrategiesInfo(address assetAddress)
        external
        view
        returns (StrategyInfo[] memory)
    {
        IVault vault = IVault(assetAddress);
        uint256 numberOfStrategies = strategyHelper().assetStrategiesLength(
            assetAddress
        );
        StrategyInfo[] memory result = new StrategyInfo[](numberOfStrategies);

        for (
            uint256 strategyIdx = 0;
            strategyIdx < numberOfStrategies;
            strategyIdx++
        ) {
            address strategyAddress = vault.withdrawalQueue(strategyIdx);
            IVault.VaultStrategyParams memory params = vault.strategies(
                strategyAddress
            );
            string memory name = IStrategy(strategyAddress).name();
            StrategyInfo memory info = StrategyInfo(
                strategyAddress,
                name,
                params
            );
            result[strategyIdx] = info;
        }

        return result;
    }
}
