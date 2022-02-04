import pytest
from brownie import interface, ZERO_ADDRESS, Contract


usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
cyWethAddress = "0x41c84c0e2EE0b740Cf0d31F63f3B6F627DC6b393"
wethAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
cyUsdcAddress = "0x76eb2fe28b36b3ee97f3adae0c69606eedb2a37c"

sushiAddress = "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2"
cySushiAddress = "0x226F3738238932BA0dB2319a8117D9555446102f"
whaleAddress = "0x53c286E0AbE87c9e6d4d95ebE62ceaFa4aFCE849"
comptrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
userAddress = "0x4C026d5D6A7fe1B2e2B28B916Ef2016f6058F7B4"  # sssuttonsss.eth

yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
cyYfiAddress = "0xFa3472f7319477c9bFEcdD66E4B948569E7621b9"


@pytest.fixture
def ironBankAdapter(
    RegistryAdapterIronBank,
    ironBankTvlAdapter,
    yearnAddressesProvider,
    gov,
):
    ironBankAdapter = RegistryAdapterIronBank.deploy(
        yearnAddressesProvider, {"from": gov}
    )
    ironBankAdapter.setExtensionsAddresses([ironBankTvlAdapter], {"from": gov})
    return ironBankAdapter


def test_interface(
    ironBankAdapter, introspection, management, registryAdapterCommonInterface
):
    for method in registryAdapterCommonInterface:
        methodImplemented = introspection.implementsMethod(ironBankAdapter, method)
        if not methodImplemented:
            print(f"Missing method implementation: {method}")
        assert methodImplemented == True


def test_assets_tokens_addresses(ironBankAdapter):
    tokens = ironBankAdapter.assetsTokensAddresses()
    assert len(tokens) > 0


def test_asset_user_metadata(ironBankAdapter, management, accounts, oracle):
    sushi = Contract(sushiAddress)
    cySushi = Contract(cySushiAddress)
    whale = accounts.at(whaleAddress, force=True)
    MAX_UINT256 = 2 ** 256 - 1
    sushi.approve(cySushi, MAX_UINT256, {"from": whale})
    sushi_bal = sushi.balanceOf(whale)
    cySushi.mint(sushi_bal, {"from": whale})
    assert sushi.balanceOf(whale) == 0
    assert cySushi.balanceOf(whale) > 0

    comptroller = Contract(comptrollerAddress)
    _, collateralFactor, _ = comptroller.markets(cySushiAddress)

    comptroller.enterMarkets([cySushi], {"from": whale})

    tokenAddress = cySushi.underlying()
    tokenPriceUsdc = ironBankAdapter.assetUnderlyingTokenPriceUsdc(cySushi)
    exchangeRate = cySushi.exchangeRateStored()
    supplyBalanceShares = cySushi.balanceOf(whale)
    supplyBalanceUnderlying = (supplyBalanceShares * exchangeRate) / 10 ** 18
    supplyBalanceUsdc = oracle.getNormalizedValueUsdc(
        tokenAddress, supplyBalanceUnderlying, tokenPriceUsdc
    )

    borrowBalanceShares = cySushi.borrowBalanceStored(whale)
    borrowBalanceUsdc = oracle.getNormalizedValueUsdc(
        tokenAddress, borrowBalanceShares, tokenPriceUsdc
    )

    _, collateralBalanceShare, _, _ = cySushi.getAccountSnapshot(whale)
    collateralBalanceUnderlying = collateralBalanceShare * exchangeRate / 10 ** 18

    collateralBalanceUsdc = oracle.getNormalizedValueUsdc(
        tokenAddress, collateralBalanceUnderlying, tokenPriceUsdc
    )

    borrowLimitUsdc = collateralBalanceUsdc * collateralFactor / 10 ** 18

    asset_user_metadata = ironBankAdapter.assetUserMetadata(whale, cySushi)
    assert asset_user_metadata[0] == cySushi
    assert asset_user_metadata[1] == True
    assert asset_user_metadata[2] == supplyBalanceUsdc
    assert asset_user_metadata[3] == borrowBalanceUsdc
    assert asset_user_metadata[4] == collateralBalanceUsdc
    assert asset_user_metadata[5] == borrowLimitUsdc


def test_assets_user_metadata(ironBankAdapter, management, accounts, oracle):
    # sushi and cySuchi
    sushi = Contract(sushiAddress)
    cySushi = Contract(cySushiAddress)
    whale = accounts.at(whaleAddress, force=True)
    MAX_UINT256 = 2 ** 256 - 1
    sushi.approve(cySushi, MAX_UINT256, {"from": whale})
    sushi_bal = sushi.balanceOf(whale)
    cySushi.mint(sushi_bal, {"from": whale})
    assert sushi.balanceOf(whale) == 0
    assert cySushi.balanceOf(whale) > 0

    # yfi and cyYfi
    yfi = Contract(yfiAddress)
    cyYfi = Contract(cyYfiAddress)
    whale = accounts.at(whaleAddress, force=True)
    MAX_UINT256 = 2 ** 256 - 1
    yfi.approve(cyYfi, MAX_UINT256, {"from": whale})
    yfi_bal = yfi.balanceOf(whale)
    cyYfi.mint(yfi_bal, {"from": whale})
    assert yfi.balanceOf(whale) == 0
    assert cyYfi.balanceOf(whale) > 0

    comptroller = Contract(comptrollerAddress)
    _, sushiCollateralFactor, _ = comptroller.markets(cySushiAddress)
    _, yfiCollateralFactor, _ = comptroller.markets(cyYfiAddress)

    comptroller.enterMarkets([cySushi, cyYfi], {"from": whale})

    # sushi
    sushiTokenAddress = cySushi.underlying()
    sushiPriceUsdc = ironBankAdapter.assetUnderlyingTokenPriceUsdc(cySushi)
    sushiExchangeRate = cySushi.exchangeRateStored()
    sushiSupplyBalShares = cySushi.balanceOf(whale)
    sushiSupplyBalUnderlying = (sushiSupplyBalShares * sushiExchangeRate) / 10 ** 18
    sushiSupplyBalUsdc = oracle.getNormalizedValueUsdc(
        sushiTokenAddress, sushiSupplyBalUnderlying, sushiPriceUsdc
    )

    sushiBorrowBalShares = cySushi.borrowBalanceStored(whale)
    sushiBorrowBalUsdc = oracle.getNormalizedValueUsdc(
        sushiTokenAddress, sushiBorrowBalShares, sushiPriceUsdc
    )

    _, sushiCollateralBalShare, _, _ = cySushi.getAccountSnapshot(whale)
    sushiCollateralBalUnderlying = (
        sushiCollateralBalShare * sushiExchangeRate / 10 ** 18
    )

    sushiCollateralBalUsdc = oracle.getNormalizedValueUsdc(
        sushiTokenAddress, sushiCollateralBalUnderlying, sushiPriceUsdc
    )

    sushiBorrowLimitUsdc = sushiCollateralBalUsdc * sushiCollateralFactor / 10 ** 18

    # yfi
    yfiTokenAddress = ironBankAdapter.assetUnderlyingTokenAddress(cyYfi)
    yfiPriceUsdc = ironBankAdapter.assetUnderlyingTokenPriceUsdc(cyYfi)
    yfiExchangeRate = cyYfi.exchangeRateStored()
    yfiSupplyBalShares = cyYfi.balanceOf(whale)
    yfiSupplyBalUnderlying = (yfiSupplyBalShares * yfiExchangeRate) / 10 ** 18
    yfiSupplyBalUsdc = oracle.getNormalizedValueUsdc(
        yfiTokenAddress, yfiSupplyBalUnderlying, yfiPriceUsdc
    )

    yfiBorrowBalShares = cyYfi.borrowBalanceStored(whale)
    yfiBorrowBalUsdc = oracle.getNormalizedValueUsdc(
        yfiTokenAddress, yfiBorrowBalShares, yfiPriceUsdc
    )

    _, yfiCollateralBalShare, _, _ = cyYfi.getAccountSnapshot(whale)
    yfiCollateralBalUnderlying = yfiCollateralBalShare * yfiExchangeRate / 10 ** 18

    yfiCollateralBalUsdc = oracle.getNormalizedValueUsdc(
        yfiTokenAddress, yfiCollateralBalUnderlying, yfiPriceUsdc
    )

    yfiBorrowLimitUsdc = yfiCollateralBalUsdc * yfiCollateralFactor / 10 ** 18

    asset_user_metadata = ironBankAdapter.assetsUserMetadata(whale, [cySushi, cyYfi])
    assert asset_user_metadata[0][0] == cySushi
    assert asset_user_metadata[0][1] == True
    assert asset_user_metadata[0][2] == sushiSupplyBalUsdc
    assert asset_user_metadata[0][3] == sushiBorrowBalUsdc
    assert asset_user_metadata[0][4] == sushiCollateralBalUsdc
    assert asset_user_metadata[0][5] == sushiBorrowLimitUsdc

    assert asset_user_metadata[1][0] == cyYfi
    assert asset_user_metadata[1][1] == True
    assert asset_user_metadata[1][2] == yfiSupplyBalUsdc
    assert asset_user_metadata[1][3] == yfiBorrowBalUsdc
    assert asset_user_metadata[1][4] == yfiCollateralBalUsdc
    assert asset_user_metadata[1][5] == yfiBorrowLimitUsdc


def test_adapter_info(ironBankAdapter):
    adapterInfo = ironBankAdapter.adapterInfo()
    assert adapterInfo[0] == ironBankAdapter
    assert adapterInfo[1] == "IRON_BANK_MARKET"
    assert adapterInfo[2] == "LENDING"


def test_registry_address(ironBankAdapter):
    assert not ironBankAdapter.registryAddress() == ZERO_ADDRESS


def test_assets_length(ironBankAdapter):
    assetsLength = ironBankAdapter.assetsLength()
    assert assetsLength > 0


def test_assets_addresses(ironBankAdapter):
    assetsAddresses = ironBankAdapter.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_asset_static(ironBankAdapter):
    cyUsdcToken = Contract(cyUsdcAddress)
    usdcTokenAddress = ironBankAdapter.assetUnderlyingTokenAddress(cyUsdcAddress)
    _, typeId, _ = ironBankAdapter.adapterInfo()
    usdcTokenName = cyUsdcToken.name()
    usdcTokenSymbol = cyUsdcToken.symbol()
    usdcTokenDecimal = cyUsdcToken.decimals()

    assetStatic = ironBankAdapter.assetStatic(cyUsdcAddress)
    assetId = assetStatic[0]
    assetTypeId = assetStatic[1]
    assetTokenId = assetStatic[2]
    assetName = assetStatic[3]
    assetVersion = assetStatic[4]
    assetSymbol = assetStatic[5]
    assetDecimals = assetStatic[6]

    assert assetId == cyUsdcAddress
    assert assetTypeId == typeId
    assert assetTokenId == usdcTokenAddress
    assert assetName == usdcTokenName
    assert assetVersion == "2.0.0"
    assert assetSymbol == usdcTokenSymbol
    assert assetDecimals == usdcTokenDecimal


def test_asset_dynamic(ironBankAdapter, oracle):
    cyUsdcToken = Contract(cyUsdcAddress)
    usdcTokenAddress = ironBankAdapter.assetUnderlyingTokenAddress(cyUsdcAddress)
    liquidity = cyUsdcToken.getCash()
    usdcTokenPrice = ironBankAdapter.assetUnderlyingTokenPriceUsdc(cyUsdcAddress)
    assert liquidity > 0
    assert usdcTokenPrice > 0

    liquidityUsdc = oracle.getNormalizedValueUsdc(
        usdcTokenAddress, liquidity, usdcTokenPrice
    )
    assert liquidityUsdc > 0

    cyUsdcAddressBalance = ironBankAdapter.assetBalance(cyUsdcAddress)
    assert cyUsdcAddressBalance > 0

    underlyingTokenBalanceUsdc = oracle.getNormalizedValueUsdc(
        usdcTokenAddress, cyUsdcAddressBalance, usdcTokenPrice
    )
    underlyingTokenBalance = (cyUsdcAddressBalance, underlyingTokenBalanceUsdc)
    totalBorrowedUsdc = oracle.getNormalizedValueUsdc(
        usdcTokenAddress, cyUsdcToken.totalBorrows(), usdcTokenPrice
    )
    assert totalBorrowedUsdc > 0

    comptroller = Contract(comptrollerAddress)
    isListed, collateralFactorMantissa, version = comptroller.markets(cyUsdcAddress)
    assert version >= 1

    collateralCap = cyUsdcToken.collateralCap()
    assert collateralCap > 0

    totalCollateralTokens = cyUsdcToken.totalCollateralTokens()
    assert totalCollateralTokens > 0

    blocksPerYear = 2102400
    lendApyBips = cyUsdcToken.supplyRatePerBlock() * blocksPerYear / 10 ** 14
    borrowApyBips = cyUsdcToken.borrowRatePerBlock() * blocksPerYear / 10 ** 14
    assert lendApyBips > 0
    assert borrowApyBips > 0
    collateralFactor = collateralFactorMantissa
    assert collateralFactor > 0

    isActive = isListed
    assert isActive == True

    reserveFactor = cyUsdcToken.reserveFactorMantissa()
    exchangeRate = cyUsdcToken.exchangeRateStored()
    totalSuppliedUsdc = underlyingTokenBalanceUsdc

    assert reserveFactor > 0
    assert exchangeRate > 0
    _, typeId, _ = ironBankAdapter.adapterInfo()
    assetDynamic = ironBankAdapter.assetDynamic(cyUsdcAddress)
    assetId = assetDynamic[0]
    assetTypeId = assetDynamic[1]
    assetTokenId = assetDynamic[2]
    assetUnderlyingTokenBalance = assetDynamic[3]
    assetMetadata = assetDynamic[4]

    assert assetId == cyUsdcAddress
    assert assetTypeId == typeId
    assert assetTokenId == usdcAddress
    assert assetUnderlyingTokenBalance == underlyingTokenBalance

    assert assetMetadata[0] == totalSuppliedUsdc
    assert assetMetadata[1] == totalBorrowedUsdc
    assert assetMetadata[2] == lendApyBips
    assert assetMetadata[3] == borrowApyBips
    assert assetMetadata[4] == liquidity
    assert assetMetadata[5] == liquidityUsdc
    assert assetMetadata[6] == totalCollateralTokens
    assert assetMetadata[7] == collateralFactor
    assert assetMetadata[8] == collateralCap
    assert assetMetadata[9] == isActive
    assert assetMetadata[10] == reserveFactor
    assert assetMetadata[11] == exchangeRate


def test_assets_static(ironBankAdapter):
    cyUsdcToken = Contract(cyUsdcAddress)
    usdcTokenAddress = ironBankAdapter.assetUnderlyingTokenAddress(cyUsdcAddress)

    cySushiToken = Contract(cySushiAddress)
    sushiTokenAddress = ironBankAdapter.assetUnderlyingTokenAddress(cySushiAddress)

    _, typeId, _ = ironBankAdapter.adapterInfo()
    usdcTokenName = cyUsdcToken.name()
    usdcTokenSymbol = cyUsdcToken.symbol()
    usdcTokenDecimal = cyUsdcToken.decimals()

    sushiTokenName = cySushiToken.name()
    sushiTokenSymbol = cySushiToken.symbol()
    sushiTokenDecimal = cySushiToken.decimals()

    assets = ironBankAdapter.assetsStatic([cyUsdcToken, cySushiToken])
    usdcAsset = assets[0]
    sushiAsset = assets[1]

    usdcAssetId = usdcAsset[0]
    usdcAssetTypeId = usdcAsset[1]
    usdcAssetTokenId = usdcAsset[2]
    usdcAssetName = usdcAsset[3]
    usdcAssetVersion = usdcAsset[4]
    usdcAssetSymbol = usdcAsset[5]
    usdcAssetDecimals = usdcAsset[6]

    assert usdcAssetId == cyUsdcAddress
    assert usdcAssetTypeId == typeId
    assert usdcAssetTokenId == usdcTokenAddress
    assert usdcAssetName == usdcTokenName
    assert usdcAssetVersion == "2.0.0"
    assert usdcAssetSymbol == usdcTokenSymbol
    assert usdcAssetDecimals == usdcTokenDecimal

    sushiAssetId = sushiAsset[0]
    sushiAssetTypeId = sushiAsset[1]
    sushiAssetTokenId = sushiAsset[2]
    sushiAssetName = sushiAsset[3]
    sushiAssetVersion = sushiAsset[4]
    sushiAssetSymbol = sushiAsset[5]
    sushiAssetDecimals = sushiAsset[6]

    assert sushiAssetId == cySushiAddress
    assert sushiAssetTypeId == typeId
    assert sushiAssetTokenId == sushiTokenAddress
    assert sushiAssetName == sushiTokenName
    assert sushiAssetVersion == "2.0.0"
    assert sushiAssetSymbol == sushiTokenSymbol
    assert sushiAssetDecimals == sushiTokenDecimal


def test_assets_dynamic(ironBankAdapter):
    assets = ironBankAdapter.assetsDynamic()
    assert len(assets) > 1
    firstAsset = assets[0]
    assetId = firstAsset[0]
    assetTypeId = firstAsset[1]
    assetTokenId = firstAsset[2]
    assetUnderlyingTokenBalance = firstAsset[3]
    assetMetadata = firstAsset[4]
    assert assetId == cyWethAddress
    assert assetTypeId == "IRON_BANK_MARKET"
    assert assetTokenId == wethAddress
    assert assetUnderlyingTokenBalance[0] > 0
    assert assetUnderlyingTokenBalance[1] > 0


def test_asset_positions_of(ironBankAdapter, accounts, oracle):

    weth = Contract(wethAddress)
    cyWeth = Contract(cyWethAddress)
    user = accounts.at(userAddress, force=True)
    MAX_UINT256 = 2 ** 256 - 1
    weth.approve(cyWeth, MAX_UINT256, {"from": user})
    weth_bal = weth.balanceOf(userAddress)
    cyWeth.mint(weth_bal, {"from": user})

    comptroller = Contract(comptrollerAddress)

    comptroller.enterMarkets([cyWeth], {"from": user})

    cyWeth = Contract(cyWethAddress)
    cyWethTokenAddress = ironBankAdapter.assetUnderlyingTokenAddress(cyWethAddress)
    cyWethTokenPrice = ironBankAdapter.assetUnderlyingTokenPriceUsdc(cyWethAddress)
    decimal = cyWeth.decimals()

    userSupplyBalanceShares = cyWeth.balanceOf(userAddress)
    userBorrowBalanceShares = cyWeth.borrowBalanceStored(userAddress)
    assert userSupplyBalanceShares > 0
    assert userBorrowBalanceShares > 0

    exchangeRate = cyWeth.exchangeRateStored()

    userSupplyBalanceUnderlying = userSupplyBalanceShares * exchangeRate / 10 ** 18

    positions = ironBankAdapter.assetPositionsOf(userAddress, cyWethAddress)
    assert userSupplyBalanceUnderlying > 0
    # print(positions)
    supplyPosition = positions[0]

    # basic info test
    assetId = supplyPosition[0]
    tokenId = supplyPosition[1]
    typeId = supplyPosition[2]
    balance = supplyPosition[3]
    # print(assetId, tokenId, typeId, balance)
    assert assetId == cyWethAddress
    assert tokenId == cyWethTokenAddress
    assert typeId == "LEND"
    assert balance == userSupplyBalanceShares

    # Test token allowances
    tokenAllowances = supplyPosition[5]
    owner = tokenAllowances[0][0]
    spender = tokenAllowances[0][1]
    allowance = tokenAllowances[0][2]
    assert owner == userAddress
    assert spender == cyWethAddress
    assert allowance > 0

    # Test account borrow balance
    userBorrowedCyTokenBalance = userBorrowBalanceShares * 10 ** 18 / exchangeRate

    borrowPosition = positions[1]

    # basic info test
    assetId = borrowPosition[0]
    tokenId = borrowPosition[1]
    typeId = borrowPosition[2]
    balance = borrowPosition[3]
    # print(assetId, tokenId, typeId, balance)
    assert assetId == cyWethAddress
    assert tokenId == cyWethTokenAddress
    assert typeId == "BORROW"
    assert balance == userBorrowedCyTokenBalance

    # Test token allowances
    tokenAllowances = borrowPosition[5]
    owner = tokenAllowances[0][0]
    spender = tokenAllowances[0][1]
    allowance = tokenAllowances[0][2]
    assert owner == userAddress
    assert spender == cyWethAddress
    assert allowance > 0


def test_assets_positions_of(ironBankAdapter, oracle, accounts):
    cyWeth = Contract(cyWethAddress)

    userSupplyBalanceShares = cyWeth.balanceOf(userAddress)
    userBorrowBalanceShares = cyWeth.borrowBalanceStored(userAddress)

    assert userSupplyBalanceShares > 0
    assert userBorrowBalanceShares > 0

    # Test positionsOf(address)
    positions = ironBankAdapter.assetsPositionsOf(userAddress, [cyWethAddress])
    position = positions[0]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == cyWethAddress

    # Test positionsOf(address, [...address])
    positions = ironBankAdapter.assetsPositionsOf(
        userAddress, [cyWethAddress, cyUsdcAddress]
    )

    position = positions[0]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == cyWethAddress

    position = positions[3]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == cyUsdcAddress
