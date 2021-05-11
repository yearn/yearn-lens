import pytest
from brownie import Oracle
from eth_account import Account
from brownie import web3

uniswapRouterAddress = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
uniswapFactoryAddress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
sushiswapRouterAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
sushiswapFactoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
curveRegistryAddress = "0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c"
unitrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"


@pytest.fixture
def gov(accounts):
    yield accounts.at(web3.ens.resolve("ychad.eth"), force=True)


@pytest.fixture
def managementList(ManagementList, management):
    return ManagementList.deploy("Managemenet list", {"from": management})


@pytest.fixture
def registryAdapterCommonInterface():
    return [
        "oracleAddress()",  # Address of the current oracle
        "helperAddress()",  # Address of the helper utility
        "addressesGeneratorAddress()",  # Address of the addresses generator utility
        "extensionsAddresses()",  # Addresses of fallback method extensions
        "setExtensionsAddresses(address[])",
        "assetsStatic(address[])",
        "assetsDynamic(address[])",
        "assetsStatic()",
        "assetsDynamic()",
        "tokenAllowances(address,address)",
        "assetAllowances(address,address)",
        "assetsLength()",
        "assetsAddresses()",
        "registry()",
        "updateSlot(bytes32,bytes32)",
        "assetsPositionsOf(address,address[])",
        "assetsPositionsOf(address)",
        "adapterInfo()",
        "assetUserMetadata(address,address)",
        "assetsUserMetadata(address)",
        "underlyingTokenAddress(address)",
        "assetStatic(address)",
        "assetDynamic(address)",
        "assetPositionsOf(address,address)",
        "assetBalance(address)",
        "assetsTokensAddresses()",
        "adapterPositionOf(address)",
    ]


@pytest.fixture
def introspection(Introspection, management):
    return Introspection.deploy({"from": management})


@pytest.fixture
def pricesHelper(PricesHelper, management, managementList, oracle):
    return PricesHelper.deploy(oracle, {"from": management})


@pytest.fixture
def delegationMapping(DelegatedBalanceMapping, management, managementList):
    return DelegatedBalanceMapping.deploy(managementList, {"from": management})


@pytest.fixture
def v2AddressesGenerator(
    AddressesGeneratorV2Vaults, management, managementList, oracle
):
    v2RegistryAddress = "0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804"
    generator = AddressesGeneratorV2Vaults.deploy(
        v2RegistryAddress, managementList, {"from": management}
    )
    trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
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
    managementList,
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
    managementList,
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
def helperInternal(Helper, managementList, management):
    return Helper.deploy(managementList, {"from": management})


@pytest.fixture
def strategiesHelper(StrategiesHelper, v2VaultsAdapter, helperInternal, management):
    return StrategiesHelper.deploy(
        v2VaultsAdapter, helperInternal, {"from": management}
    )


@pytest.fixture
def helper(
    helperInternal,
    management,
    managementList,
    oracle,
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
        sushiswapFactoryAddress,
        uniswapRouterAddress,
        uniswapFactoryAddress,
        usdcAddress,
        {"from": management},
    )
    return calculationsSushiswap


@pytest.fixture
def oracle(
    Oracle,
    management,
    managementList,
    calculationsSushiswap,
    CalculationsCurve,
    CalculationsIronBank,
    CalculationsYearnVaults,
):

    uniswapRouterAddress = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
    uniswapFactoryAddress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
    sushiswapRouterAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
    sushiswapFactoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
    curveAddressProvider = "0x0000000022D53366457F9d5E68Ec105046FC4383"
    unitrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
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

    # return Oracle.at("0x83d95e0d5f402511db06817aff3f9ea88224b030")

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

    calculationsCurve = CalculationsCurve.deploy(
        curveAddressProvider, oracle, {"from": management}
    )
    calculationsIronBank = CalculationsIronBank.deploy(
        unitrollerAddress, oracle, {"from": management}
    )
    oracle.setCalculations(
        [
            calculationsCurve,
            calculationsIronBank,
            calculationsSushiswap,
        ],
        {"from": management},
    )
    return oracle


@pytest.fixture
def earnRegistry(GenericRegistry, management):
    registry = GenericRegistry.deploy({"from": management})

    # Earn v2
    yDaiV2Address = "0x16de59092dAE5CcF4A1E6439D611fd0653f0Bd01"
    yUsdcV2Address = "0xd6aD7a6750A7593E092a9B218d66C0A814a3436e"
    yUsdtV2Address = "0x83f798e925BcD4017Eb265844FDDAbb448f1707D"
    ySusdV2Address = "0xF61718057901F84C4eEC4339EF8f0D86D2B45600"
    yTusdV2Address = "0x73a052500105205d34daf004eab301916da8190f"
    yWbtcV2Address = "0x04Aa51bbcB46541455cCF1B8bef2ebc5d3787EC9"

    # Earn v3
    yDaiV3Address = "0xC2cB1040220768554cf699b0d863A3cd4324ce32"
    yUsdcV3Address = "0x26EA744E5B887E5205727f55dFBE8685e3b21951"
    yUsdtV3Address = "0xE6354ed5bC4b393a5Aad09f21c46E101e692d447"
    yBusdV3Address = "0x04bC0Ab673d88aE9dbC9DA2380cB6B79C4BCa9aE"

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
    managementList,
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
def v2VaultsAddressesGenerator(
    AddressesGeneratorV2Vaults,
    managementList,
    management,
):
    registryAddress = "0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804"
    return AddressesGeneratorV2Vaults.deploy(
        registryAddress,
        managementList,
        {"from": management},
    )


@pytest.fixture
def v1VaultsAddressesGenerator(
    AddressesGeneratorV1Vaults,
    managementList,
    management,
):
    registryAddress = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0"
    return AddressesGeneratorV1Vaults.deploy(
        registryAddress,
        managementList,
        {"from": management},
    )


@pytest.fixture
def ironBankAddressesGenerator(
    AddressesGeneratorIronBank,
    managementList,
    management,
):
    registryAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
    generator = AddressesGeneratorIronBank.deploy(
        registryAddress,
        managementList,
        {"from": management},
    )
    cySusdOldAddress = "0x4e3a36A633f63aee0aB57b5054EC78867CB3C0b8"
    generator.setAssetDeprecated(cySusdOldAddress, True, {"from": management})
    return generator


@pytest.fixture
def earnAddressesGenerator(
    AddressesGeneratorEarn,
    managementList,
    management,
):
    registryAddress = "0x62a4e0E7574E5407656A65CC8DbDf70f3C6EB04B"
    return AddressesGeneratorEarn.deploy(
        registryAddress,
        managementList,
        {"from": management},
    )


@pytest.fixture
def earnAdapter(RegistryAdapterEarn, earnRegistry, management, managementList, oracle):
    trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
    positionSpenderAddresses = [trustedMigratorAddress]
    adapter = RegistryAdapterEarn.deploy(
        earnRegistry,
        oracle,
        managementList,
        {"from": management},
    )
    adapter.setPositionSpenderAddresses(positionSpenderAddresses, {"from": management})
    return adapter


@pytest.fixture
def v2VaultsAdapter(
    RegisteryAdapterV2Vault,
    v2AddressesGenerator,
    oracle,
    helperInternal,
    management,
    v2VaultsTvlAdapter,
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
def rando(accounts):
    yield Account.create().address
