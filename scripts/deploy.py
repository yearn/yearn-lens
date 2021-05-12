from brownie import (
    RegisteryAdapterV2Vault,
    AddressesGeneratorV2Vaults,
    Helper,
    ManagementList,
    AddressMergeHelper,
    Oracle,
    CalculationsCurve,
    CalculationsSushiswap,
    CalculationsIronBank,
    AllowancesHelper,
    RegistryAdapterIronBank,
    TvlAdapterIronBank,
    TvlAdapterV2Vaults,
    AddressesGeneratorIronBank,
    UniqueAddressesHelper,
    BalancesHelper,
    DelegatedBalanceMapping,
    PricesHelper,
    StrategiesHelper,
    accounts,
)


def main():
    trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
    v2RegistryAddress = "0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804"
    usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    steCrvAddress = "0x06325440D014e39736583c165C2963BA99fAf14E"
    eCrvAddress = "0xA3D87FffcE63B53E0d54fAa1cc983B7eB0b74A9c"
    ethAddress = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    wethAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    aLinkAddress = "0xA64BD6C70Cb9051F6A9ba1F163Fdc07E0DfB5F84"
    linkAddress = "0x514910771AF9Ca656af840dff83E8264EcF986CA"
    usdpAddress = "0x1456688345527bE1f37E9e627DA0837D6f08C925"
    oBtcAddress = "0x8064d9Ae6cDf087b1bcd5BDf3531bD5d8C537a68"
    wbtcAddress = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    curveAddressProvider = "0x0000000022D53366457F9d5E68Ec105046FC4383"
    uniswapRouterAddress = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
    uniswapFactoryAddress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
    sushiswapRouterAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
    sushiswapFactoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
    ironBankRegistryAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
    cySusdOldAddress = "0x4e3a36A633f63aee0aB57b5054EC78867CB3C0b8"

    management = accounts[0]
    positionSpenderAddresses = [trustedMigratorAddress]

    ####################################################
    # Management list
    ####################################################
    managementList = ManagementList.deploy("Managemenet list", {"from": management})

    ####################################################
    # Oracle
    ####################################################
    oracle = Oracle.deploy(managementList, usdcAddress, {"from": management})

    oracle.addTokenAliases(
        [
            [steCrvAddress, wethAddress],
            [eCrvAddress, wethAddress],
            [ethAddress, wethAddress],
            [aLinkAddress, linkAddress],
            [usdpAddress, usdcAddress],
            [oBtcAddress, wbtcAddress],
        ],
        {"from": management},
    )

    ####################################################
    # Oracle calculations
    ####################################################
    calculationsSushiswap = CalculationsSushiswap.deploy(
        sushiswapRouterAddress,
        sushiswapFactoryAddress,
        uniswapRouterAddress,
        uniswapFactoryAddress,
        usdcAddress,
        {"from": management},
    )

    calculationsCurve = CalculationsCurve.deploy(
        curveAddressProvider, oracle, {"from": management}
    )
    calculationsIronBank = CalculationsIronBank.deploy(
        ironBankRegistryAddress, oracle, {"from": management}
    )
    oracle.setCalculations(
        [
            calculationsCurve,
            calculationsIronBank,
            calculationsSushiswap,
        ],
        {"from": management},
    )

    ####################################################
    # Helper utility
    ####################################################
    helper = Helper.deploy(managementList, {"from": management})

    ####################################################
    # Addresses generators
    ####################################################
    v2VaultsAddressesGenerator = AddressesGeneratorV2Vaults.deploy(
        v2RegistryAddress, managementList, {"from": management}
    )

    positionSpenderAddresses = [trustedMigratorAddress]
    v2VaultsAddressesGenerator.setPositionSpenderAddresses(
        positionSpenderAddresses, {"from": management}
    )

    ironBankAddressesGenerator = AddressesGeneratorIronBank.deploy(
        ironBankRegistryAddress,
        managementList,
        {"from": management},
    )
    ironBankAddressesGenerator.setAssetDeprecated(
        cySusdOldAddress, True, {"from": management}
    )
    balancesHelper = BalancesHelper.deploy(oracle, {"from": management})

    ####################################################
    # Delegated balance mapping
    ####################################################
    delegatedBalanceMapping = DelegatedBalanceMapping.deploy(
        managementList, {"from": management}
    )

    ####################################################
    # TVL adapters
    ####################################################
    ironBankTvlAdapter = TvlAdapterIronBank.deploy(
        oracle,
        ironBankAddressesGenerator,
        delegatedBalanceMapping,
        {"from": management},
    )
    v2VaultsTvlAdapter = TvlAdapterV2Vaults.deploy(
        oracle,
        helper,
        v2VaultsAddressesGenerator,
        {"from": management},
    )

    ####################################################
    # Registry adapters
    ####################################################
    v2VaultsAdapter = RegisteryAdapterV2Vault.deploy(
        oracle,
        helper,
        v2VaultsAddressesGenerator,
        {"from": management},
    )
    ironBankAdapter = RegistryAdapterIronBank.deploy(
        oracle,
        helper,
        ironBankAddressesGenerator,
        {"from": management},
    )
    ironBankAdapter.setExtensionsAddresses([ironBankTvlAdapter], {"from": management})

    ####################################################
    # Helper utilities
    ####################################################
    allowancesHelper = AllowancesHelper.deploy({"from": management})
    uniqueAddressesHelper = UniqueAddressesHelper.deploy({"from": management})
    addressMergeHelper = AddressMergeHelper.deploy({"from": management})
    pricesHelper = PricesHelper.deploy(oracle, {"from": management})
    strategiesHelper = StrategiesHelper.deploy(
        v2VaultsAdapter, helper, {"from": management}
    )
    helper.setHelpers(
        [
            allowancesHelper,
            uniqueAddressesHelper,
            pricesHelper,
            addressMergeHelper,
            strategiesHelper,
        ],
        {"from": management},
    )

    print("Management list")
    print("---------------")
    print("Management List:         ", managementList)
    print("")

    print("Oracle")
    print("------")
    print("Oracle:                  ", oracle)
    print("")

    print("Calculations")
    print("------------")
    print("Sushiswap Calculations:  ", calculationsSushiswap)
    print("Curve calculations:      ", calculationsCurve)
    print("Iron Bank Calculations:  ", calculationsIronBank)
    print("")

    print("Delegated balance mapping")
    print("-------------------------")
    print("Delegated balances:      ", delegatedBalanceMapping)
    print("")

    print("Helpers")
    print("-------")
    print("Helper:                  ", helper)
    print("Prices Helper:           ", pricesHelper)
    print("Allowances Helper:       ", allowancesHelper)
    print("Unique Addresses Helper: ", uniqueAddressesHelper)
    print("Addresses Merge Helper:  ", addressMergeHelper)
    print("Prices Helper:           ", pricesHelper)
    print("Balances Helper:         ", balancesHelper)
    print("Strategies Helper:       ", strategiesHelper)
    print("")

    print("Addresses generators")
    print("--------------------")
    print("Iron Bank Generator:     ", ironBankAddressesGenerator)
    print("V2 Generator:            ", v2VaultsAddressesGenerator)
    print("")

    print("TVL Adapters")
    print("------------")
    print("Iron Bank TVL Adapter:   ", ironBankTvlAdapter)
    print("V2 Vaults TVL Adapter:   ", v2VaultsTvlAdapter)
    print("")

    print("Registry Adapters")
    print("-----------------")
    print("V2 Vaults Adapter:       ", v2VaultsAdapter)
    print("Iron Bank Adapter:       ", ironBankAdapter)
    print("")
