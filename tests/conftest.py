import pytest
from brownie import Oracle
from eth_account import Account
from brownie import web3, Contract, interface


class MiscAddresses:
    curveAddressProvider = "0x0000000022D53366457F9d5E68Ec105046FC4383"
    ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"
    trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
    unitrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
    usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    vestedYfiAddress = "0x34dDFC06ce0c39242Fb380066Ee01e409a4a525e"
    yvBOOSTAddress = "0x9d409a0A012CFbA9B15F6D4B36Ac57A46966Ab9a"
    yveCRVAddress = "0xc5bDdf9843308380375a611c18B50Fb9341f502A"
    zapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"


class ProviderAddresses:
    curveAddressProviderAddress = "0x0000000022D53366457F9d5E68Ec105046FC4383"
    yearnAddressesProviderAddress = "0x9be19Ee7Bc4099D62737a7255f5c227fBcd6dB93"


class RegistryAddresses:
    curveRegistryAddress = "0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c"
    v2RegistryAddress = "0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804"


class FactoryAddresses:
    sushiswapFactoryAddress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
    uniswapFactoryAddress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"


class RouterAddresses:
    sushiswapRouterAddress = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
    uniswapRouterAddress = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"


class VaultAddresses:
    yfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
    v2UsdcVaultV1Address = "0xe2F6b9773BF3A015E2aA70741Bde1498bdB9425b"
    v2UsdcVaultV2Address = "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9"
    v2YfiVaultAddress = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"


class TokenAddresses:
    aLinkAddress = "0xA64BD6C70Cb9051F6A9ba1F163Fdc07E0DfB5F84"
    crvAddress =  "0xD533a949740bb3306d119CC777fa900bA034cd52"
    crvEURSUSDCAddress = "0x3D229E1B4faab62F621eF2F6A610961f7BD7b23B"
    crvEURTUSDAddress = "0x3b6831c0077a1e44ED0a21841C3bC4dC11bCE833"
    cvxCrvAddress = "0x9D0464996170c6B9e75eED71c68B99dDEDf279e8"
    cyDaiAddress = "0x8e595470Ed749b85C6F7669de83EAe304C2ec68F"
    cySusdOldAddress = "0x4e3a36A633f63aee0aB57b5054EC78867CB3C0b8"
    eCrvAddress = "0xA3D87FffcE63B53E0d54fAa1cc983B7eB0b74A9c"
    ethAddress = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    eurs = "0xdB25f211AB05b1c97D595516F45794528a807ad8"
    eursUsdcPool = "0x98a7F18d4E56Cfe84E3D081B40001B3d5bD3eB8B"
    eurt = "0xC581b735A1688071A1746c968e0798D642EDE491"
    ibEurPoolAddress = "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859"
    linkAddress = "0x514910771AF9Ca656af840dff83E8264EcF986CA"
    oBtcAddress = "0x8064d9Ae6cDf087b1bcd5BDf3531bD5d8C537a68"
    random_token = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
    sAUD = "0xF48e200EAF9906362BB1442fca31e0835773b8B4"
    sCHF = "0x0F83287FF768D1c1e17a42F44d644D7F22e8ee1d"
    sEUR = "0xD71eCFF9342A5Ced620049e616c5035F1dB98620"
    sGBP = "0x97fe22E7341a0Cd8Db6F6C021A24Dc8f4DAD855F"
    sJPY = "0xF6b1C627e95BFc3c1b4c9B825a032Ff0fBf3e07d"
    sKRW = "0x269895a3dF4D73b077Fc823dD6dA1B95f72Aaf9B"
    steCrvAddress = "0x06325440D014e39736583c165C2963BA99fAf14E"
    sushiswapLpTokenAddress = "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0"  # USDC/WETH
    threeCrvAddress = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"
    threeCrvPoolAddress = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
    triCryptoAddress = "0xc4AD29ba4B3c580e6D59105FFf484999997675Ff"
    uniswapLpTokenAddress = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"  # USDC/WETH
    usdc = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    usdpAddress = "0x1456688345527bE1f37E9e627DA0837D6f08C925"
    wbtcAddress = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    wethAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
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


class Addresses:
    misc = MiscAddresses()
    providers = ProviderAddresses()
    registries = RegistryAddresses()
    routers = RouterAddresses()
    tokens = TokenAddresses()
    vaults = VaultAddresses()


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
  pass


@pytest.fixture
def addresses():
    return Addresses


@pytest.fixture
def iv2Registry():
    return interface.IV2Registry(Addresses.registries.v2RegistryAddress)


@pytest.fixture
def v2VaultsGenerator(AddressesGeneratorV2Vaults, management):
    generator = AddressesGeneratorV2Vaults.deploy(
        Addresses.registries.v2RegistryAddress,
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
    return Contract.from_explorer(Addresses.providers.yearnAddressesProviderAddress)


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
def pricesHelper(PricesHelper, management,  oracle):
    return PricesHelper.deploy(oracle, {"from": management})


@pytest.fixture
def delegationMapping(DelegatedBalanceMapping, management):
    return DelegatedBalanceMapping.deploy({"from": management})


@pytest.fixture
def v2AddressesGenerator(
    AddressesGeneratorV2Vaults, management
):
    generator = AddressesGeneratorV2Vaults.deploy(
        Addresses.registries.v2RegistryAddress, {"from": management}
    )
    positionSpenderAddresses = [Addresses.misc.trustedMigratorAddress]
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
def strategiesHelper(StrategiesHelper, v2AddressesGenerator, addressMergeHelper, oracle, management):
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
        Addresses.routers.sushiswapRouterAddress,
        Addresses.tokens.usdcAddress,
        {"from": management},
    )
    return calculationsSushiswap

@pytest.fixture
def calculationsFixedforex(CalculationsFixedForex, management):
    return CalculationsFixedForex.deploy(
        Addresses.providers.yearnAddressesProviderAddress,
        {"from": management}
        )

@pytest.fixture
def synth_calculations(CalculationsSynth, management):
    return CalculationsSynth.deploy(
        Addresses.providers.yearnAddressesProviderAddress,
        {"from": management}
        )

@pytest.fixture
def curve_calculations(CalculationsCurve, management):
    calculations_curve = CalculationsCurve.deploy(
        Addresses.providers.yearnAddressesProviderAddress,
        Addresses.providers.curveAddressProviderAddress,
        {"from": management}
    )
    return calculations_curve

@pytest.fixture
def calculationsOverrides(CalculationsOverrides, management):
    return CalculationsOverrides.deploy(
        Addresses.providers.yearnAddressesProviderAddress,
        {"from": management}
        )

@pytest.fixture
def chainlink_calculations(CalculationsChainlink, management):
    chainlink_calculations = CalculationsChainlink.deploy({"from": management})
    return chainlink_calculations

@pytest.fixture
def calculationsIronBank(CalculationsIronBank, management):
    calculations = CalculationsIronBank.deploy(
        Addresses.providers.yearnAddressesProviderAddress,
        {"from": management}
    )
    calculations.addUnitrollers([
        "UNITROLLER_IRON_BANK",
        "UNITROLLER_COMPOUND"
    ], {"from": management})
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
    chainlink_calculations
):
    oracle = Oracle.deploy(Addresses.tokens.usdcAddress, {"from": management})
    oracle.addTokenAliases(
        [
          [Addresses.tokens.steCrvAddress, Addresses.tokens.wethAddress],
          [Addresses.tokens.eCrvAddress, Addresses.tokens.wethAddress],
          [Addresses.tokens.ethAddress, Addresses.tokens.wethAddress],
          [Addresses.tokens.aLinkAddress, Addresses.tokens.linkAddress],
          [Addresses.tokens.usdpAddress, Addresses.tokens.usdcAddress],
          [Addresses.tokens.oBtcAddress, Addresses.tokens.wbtcAddress],
          ],
        {"from": management},
        )
    calculationsYearnVaults = CalculationsYearnVaults.deploy(oracle, {"from": management})
    oracle.setCalculations(
        [
            calculationsOverrides,
            chainlink_calculations,
            curve_calculations,
            calculationsYearnVaults,
            calculationsIronBank,
            synth_calculations,
            calculationsSushiswap
        ],
        {"from": management},
    )
    return oracle


@pytest.fixture
def earnRegistry(GenericRegistry, management):
    registry = GenericRegistry.deploy({"from": management})
    registry.addAssets(
        [
            Addresses.tokens.yDaiV2Address,
            Addresses.tokens.yUsdcV2Address,
            Addresses.tokens.yUsdtV2Address,
            Addresses.tokens.ySusdV2Address,
            Addresses.tokens.yTusdV2Address,
            Addresses.tokens.yWbtcV2Address,
            Addresses.tokens.yDaiV3Address,
            Addresses.tokens.yUsdcV3Address,
            Addresses.tokens.yUsdtV3Address,
            Addresses.tokens.yBusdV3Address,
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
        Addresses.registries.v2RegistryAddress,
        {"from": management},
    )


@pytest.fixture
def v1VaultsAddressesGenerator(AddressesGeneratorV1Vaults, management,):
    # TODO: what address is this?
    registryAddress = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0"
    return AddressesGeneratorV1Vaults.deploy(
        registryAddress,
        {"from": management},
    )


@pytest.fixture
def ironBankAddressesGenerator(AddressesGeneratorIronBank, management):
    generator = AddressesGeneratorIronBank.deploy(
        Addresses.misc.unitrollerAddress,
        {"from": management},
    )
    generator.setAssetDeprecated(
        Addresses.tokens.cySusdOldAddress,
        True,
        {"from": management}
        )
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
    positionSpenderAddresses = [Addresses.misc.trustedMigratorAddress]
    adapter = RegistryAdapterEarn.deploy(earnRegistry, oracle, {"from": management})
    adapter.setPositionSpenderAddresses(positionSpenderAddresses, {"from": management})
    return adapter


@pytest.fixture
def v2VaultsAdapter(
    RegisteryAdapterV2Vault,
    v2AddressesGenerator,
    oracle,
    helperInternal,
    management
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
