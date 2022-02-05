import pytest
from .addresses import *
from brownie import Oracle
from eth_account import Account
from brownie import web3, Contract, interface


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture
def iv2Registry():
    return interface.IV2Registry(v2RegistryAddress)


@pytest.fixture
def v2VaultsGenerator(AddressesGeneratorV2Vaults, management):
    generator = AddressesGeneratorV2Vaults.deploy(
        v2RegistryAddress,
        {"from": management},
    )
    return generator


@pytest.fixture
def managementList(ManagementList, management):
    return ManagementList.deploy("Managemenet list", {"from": management})


@pytest.fixture
def gov(accounts):
    yield accounts.at(web3.ens.resolve("ychad.eth"), force=True)


@pytest.fixture
def yearnAddressesProvider():
    return Contract.from_explorer(yearnAddressesProviderAddress)


@pytest.fixture
def registryAdapterCommonInterface():
    return [
        "yearnAddressesProviderAddress()",  # Address of the current oracle
        "extensionsAddresses()",  # Addresses of fallback method extensions
        "setExtensionsAddresses(address[])",  # Update fallback extension contract addresses
        "assetsStatic(address[])",  # Fetch a list of static adapter assets given an array of asset addresses
        "assetsDynamic(address[])",  # Fetch a list of dynamic adapter assets given an array of asset addresses
        "assetsStatic()",  # Fetch a list of all static adapter assets
        "assetsDynamic()",  # Fetch a list of all dynamic adapter assets
        "tokenAllowances(address,address)",  # Fetch token allowances for an asset scoped to an asset and account
        "assetAllowances(address,address)",  # Fetch asset allowances for an asset scoped to a spender and account
        "assetsLength()",  # Fetch the total number of assets in the adapter
        "assetsAddresses()",  # Fetch a list of all asset addresses for the adapter
        "registryAddress()",  # Fetch the address of the registry associated with the adapter
        "assetsPositionsOf(address,address[])",  # Fetch account positions relative to an asset given a list of asset addresses
        "assetsPositionsOf(address)",  # Fetch account positions relative to an asset
        "adapterInfo()",  # Fetch adapter info metadata
        "assetUserMetadata(address,address)",  # Fetch metadata for an asset scoped to a user
        "assetsUserMetadata(address)",  # Fetch metadata for all assets scoped to a user
        "assetUnderlyingTokenAddress(address)",  # Fetch the underlying token address of an asset
        "assetStatic(address)",  # Fetch static information about an asset given an address
        "assetDynamic(address)",  # Fetch dynamic information about an asset given an address
        "assetPositionsOf(address,address)",  # Fetch account positins for an asset given an account address and asset address
        "assetBalance(address)",  # Fetch the balance for an asset given an asset address
        "assetsTokensAddresses()",  # Fetch a list of unique underlying token addresses associated with an adapter
        "adapterPositionOf(address)",  # Fetch asset position metadata scoped to a user
        "updateSlot(bytes32,bytes32)",  # Allow owner to update a storage slot directly
    ]


@pytest.fixture
def introspection(Introspection, management):
    return Introspection.deploy({"from": management})


@pytest.fixture(autouse=True)
def strings(String, management):
    return String.deploy({"from": management})


@pytest.fixture
def pricesHelper(PricesHelper, management, oracle):
    return PricesHelper.deploy(oracle, {"from": management})


@pytest.fixture
def delegationMapping(DelegatedBalanceMapping, management):
    return DelegatedBalanceMapping.deploy({"from": management})


@pytest.fixture
def v2AddressesGenerator(AddressesGeneratorV2Vaults, management):
    generator = AddressesGeneratorV2Vaults.deploy(
        v2RegistryAddress, {"from": management}
    )
    positionSpenderAddresses = [trustedMigratorAddress]
    generator.setPositionSpenderAddresses(
        positionSpenderAddresses, {"from": management}
    )
    return generator


@pytest.fixture
def ironBankTvlAdapter(
    TvlAdapterIronBank,
    ironBankAddressesGenerator,
    delegationMapping,
    oracle,
    management,
):
    return TvlAdapterIronBank.deploy(
        oracle,
        ironBankAddressesGenerator,
        delegationMapping,
        {"from": management},
    )


@pytest.fixture
def v2VaultsTvlAdapter(
    TvlAdapterV2Vaults,
    v2VaultsAddressesGenerator,
    oracle,
    helperInternal,
    management,
):
    return TvlAdapterV2Vaults.deploy(
        oracle,
        helperInternal,
        v2VaultsAddressesGenerator,
        {"from": management},
    )


@pytest.fixture
def allowancesHelper(AllowancesHelper, management):
    return AllowancesHelper.deploy({"from": management})


@pytest.fixture
def addressMergeHelper(AddressMergeHelper, management):
    return AddressMergeHelper.deploy({"from": management})


@pytest.fixture
def helperInternal(Helper, management):
    return Helper.deploy({"from": management})


@pytest.fixture
def strategiesHelper(
    StrategiesHelper, v2AddressesGenerator, addressMergeHelper, oracle, management
):
    return StrategiesHelper.deploy(
        v2AddressesGenerator, addressMergeHelper, oracle, {"from": management}
    )


@pytest.fixture
def helper(
    helperInternal,
    management,
    allowancesHelper,
    pricesHelper,
    addressMergeHelper,
    strategiesHelper,
    uniqueAddressesHelper,
):

    helperInternal.setHelpers(
        [
            allowancesHelper,
            uniqueAddressesHelper,
            pricesHelper,
            addressMergeHelper,
            strategiesHelper,
        ],
        {"from": management},
    )
    return helperInternal


@pytest.fixture
def calculationsSushiswap(CalculationsSushiswap, management):
    calculationsSushiswap = CalculationsSushiswap.deploy(
        sushiswapRouterAddress,
        usdcAddress,
        {"from": management},
    )
    return calculationsSushiswap


@pytest.fixture
def calculationsFixedforex(CalculationsFixedForex, management):
    return CalculationsFixedForex.deploy(
        yearnAddressesProviderAddress, {"from": management}
    )


@pytest.fixture
def synth_calculations(CalculationsSynth, management):
    return CalculationsSynth.deploy(yearnAddressesProviderAddress, {"from": management})


@pytest.fixture
def curve_calculations(CalculationsCurve, management):
    calculations_curve = CalculationsCurve.deploy(
        yearnAddressesProviderAddress, curveAddressProviderAddress, {"from": management}
    )
    return calculations_curve


@pytest.fixture
def calculationsOverrides(CalculationsOverrides, management):
    return CalculationsOverrides.deploy(
        yearnAddressesProviderAddress, {"from": management}
    )


@pytest.fixture
def chainlink_calculations(CalculationsChainlink, management):
    chainlink_calculations = CalculationsChainlink.deploy({"from": management})
    return chainlink_calculations


@pytest.fixture
def calculationsIronBank(CalculationsIronBank, management):
    calculations = CalculationsIronBank.deploy(
        yearnAddressesProviderAddress, {"from": management}
    )
    calculations.addUnitrollers(
        ["UNITROLLER_IRON_BANK", "UNITROLLER_COMPOUND"], {"from": management}
    )
    return calculations


@pytest.fixture
def oracle(
    Oracle,
    management,
    calculationsSushiswap,
    synth_calculations,
    curve_calculations,
    calculationsIronBank,
    CalculationsYearnVaults,
    calculationsOverrides,
    chainlink_calculations,
):
    oracle = Oracle.deploy(usdcAddress, {"from": management})
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
    calculationsYearnVaults = CalculationsYearnVaults.deploy(
        oracle, {"from": management}
    )
    oracle.setCalculations(
        [
            calculationsOverrides,
            chainlink_calculations,
            curve_calculations,
            calculationsYearnVaults,
            calculationsIronBank,
            synth_calculations,
            calculationsSushiswap,
        ],
        {"from": management},
    )
    return oracle


@pytest.fixture
def earnRegistry(GenericRegistry, management):
    registry = GenericRegistry.deploy({"from": management})
    registry.addAssets(
        [
            yDaiV2Address,
            yUsdcV2Address,
            yUsdtV2Address,
            ySusdV2Address,
            yTusdV2Address,
            yWbtcV2Address,
            yDaiV3Address,
            yUsdcV3Address,
            yUsdtV3Address,
            yBusdV3Address,
        ]
    )
    return registry


@pytest.fixture
def v1VaultTvlAdapter(
    TvlAdapterV1Vaults,
    v1VaultsAddressesGenerator,
    delegationMapping,
    oracle,
    management,
):
    return TvlAdapterV1Vaults.deploy(
        oracle,
        v1VaultsAddressesGenerator,
        delegationMapping,
        {"from": management},
    )


@pytest.fixture
def v2VaultsAddressesGenerator(AddressesGeneratorV2Vaults, management):
    return AddressesGeneratorV2Vaults.deploy(
        v2RegistryAddress,
        {"from": management},
    )


@pytest.fixture
def v1VaultsAddressesGenerator(
    AddressesGeneratorV1Vaults,
    management,
):
    # TODO: what address is this?
    registryAddress = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0"
    return AddressesGeneratorV1Vaults.deploy(
        registryAddress,
        {"from": management},
    )


@pytest.fixture
def ironBankAddressesGenerator(AddressesGeneratorIronBank, management):
    generator = AddressesGeneratorIronBank.deploy(
        unitrollerAddress,
        {"from": management},
    )
    generator.setAssetDeprecated(cySusdOldAddress, True, {"from": management})
    return generator


@pytest.fixture
def earnAddressesGenerator(AddressesGeneratorEarn, management):
    # TODO: what address is this?
    registryAddress = "0x62a4e0E7574E5407656A65CC8DbDf70f3C6EB04B"
    return AddressesGeneratorEarn.deploy(
        registryAddress,
        {"from": management},
    )


@pytest.fixture
def earnAdapter(RegistryAdapterEarn, earnRegistry, management, oracle):
    positionSpenderAddresses = [trustedMigratorAddress]
    adapter = RegistryAdapterEarn.deploy(earnRegistry, oracle, {"from": management})
    adapter.setPositionSpenderAddresses(positionSpenderAddresses, {"from": management})
    return adapter


@pytest.fixture
def v2VaultsAdapter(
    RegisteryAdapterV2Vault, v2AddressesGenerator, oracle, helperInternal, management
):
    return RegisteryAdapterV2Vault.deploy(
        oracle,
        helperInternal,
        v2AddressesGenerator,
        {"from": management},
    )


@pytest.fixture
def uniqueAddressesHelper(UniqueAddressesHelper, management):
    return UniqueAddressesHelper.deploy({"from": management})


@pytest.fixture
def management(accounts):
    yield accounts[0]


@pytest.fixture
def chad(accounts):
    yield accounts[1]


@pytest.fixture
def rando():
    yield Account.create().address
