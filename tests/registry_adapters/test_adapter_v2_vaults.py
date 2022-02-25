import brownie
import pytest
from brownie import ZERO_ADDRESS, Contract, interface

from ..addresses import *


@pytest.fixture
def v2VaultsAdapter(
    RegisteryAdapterV2Vault,
    v2AddressesGenerator,
    oracle,
    helper,
    management,
):
    positionSpenderAddresses = [trustedMigratorAddress]
    adapter = RegisteryAdapterV2Vault.deploy(
        oracle,
        helper,
        v2AddressesGenerator,
        {"from": management},
    )
    v2AddressesGenerator.setPositionSpenderAddresses(
        positionSpenderAddresses, {"from": management}
    )
    return adapter


def test_interface(v2VaultsAdapter, introspection, registryAdapterCommonInterface):
    for method in registryAdapterCommonInterface:
        methodImplemented = introspection.implementsMethod(v2VaultsAdapter, method)
        if not methodImplemented:
            print(f"Missing method implementation: {method}")
        assert methodImplemented == True


def test_assets_tokens_addresses(v2VaultsAdapter):
    tokens = v2VaultsAdapter.assetsTokensAddresses()
    assert len(tokens) > 0


def test_asset_user_metadata(v2VaultsAdapter, management):
    assetUserMetadata = v2VaultsAdapter.assetUserMetadata(
        v2UsdcVaultV2Address, management
    )


def test_assets_user_metadata(v2VaultsAdapter, management):
    assetUserMetadata = v2VaultsAdapter.assetsUserMetadata(management)


def test_adapter_info(v2VaultsAdapter):
    adapterInfo = v2VaultsAdapter.adapterInfo()
    assert adapterInfo[0] == v2VaultsAdapter
    assert adapterInfo[1] == "VAULT_V2"
    assert adapterInfo[2] == "VAULT"


def test_registry_address(v2VaultsAdapter):
    assert not v2VaultsAdapter.registryAddress() == ZERO_ADDRESS


def test_assets_length(v2VaultsAdapter):
    assetsLength = v2VaultsAdapter.assetsLength()
    assert assetsLength > 0


def test_set_asset_deprecated(v2VaultsAdapter, v2AddressesGenerator, management):
    originalAssetsLength = v2VaultsAdapter.assetsLength()
    assert originalAssetsLength > 0
    v2AddressesGenerator.setAssetDeprecated(
        v2YfiVaultAddress, True, {"from": management}
    )
    newAssetsLength = v2VaultsAdapter.assetsLength()
    v2AddressesGenerator.assetDeprecated(v2YfiVaultAddress) == True
    assert newAssetsLength == originalAssetsLength - 1
    v2AddressesGenerator.setAssetDeprecated(
        v2YfiVaultAddress, False, {"from": management}
    )
    newAssetsLength = v2VaultsAdapter.assetsLength()
    assert newAssetsLength == originalAssetsLength
    v2AddressesGenerator.assetDeprecated(v2YfiVaultAddress) == False


def test_assets_addresses(v2VaultsAdapter):
    assetsAddresses = v2VaultsAdapter.assetsAddresses()
    assert len(assetsAddresses) > 0
    assert not assetsAddresses[0] == ZERO_ADDRESS


def test_asset_static(v2VaultsAdapter):
    # test vault data
    assetStatic = v2VaultsAdapter.assetStatic(v2UsdcVaultV2Address)
    assetId = assetStatic[0]
    assetTypeId = assetStatic[1]
    assetTokenId = assetStatic[2]
    name = assetStatic[3]
    version = assetStatic[4]
    symbol = assetStatic[5]
    decimals = assetStatic[6]
    assert assetId == v2UsdcVaultV2Address
    assert assetTypeId == "VAULT_V2"
    assert assetTokenId == usdcAddress
    assert name == "USDC yVault"
    assert version == "0.3.0"
    assert symbol == "yvUSDC"
    assert decimals == 6


def test_asset_dynamic(v2VaultsAdapter, oracle):
    assetDynamic = v2VaultsAdapter.assetDynamic(v2UsdcVaultV1Address)
    assetId = assetDynamic[0]
    typeId = assetDynamic[1]
    tokenId = assetDynamic[2]
    underlyingTokenBalance = assetDynamic[3]
    metadata = assetDynamic[4]

    # Test vault underlying balances
    tokenPriceUsdc = oracle.getPriceUsdcRecommended(tokenId)
    balance = underlyingTokenBalance[0]
    balanceUsdc = underlyingTokenBalance[1]
    tolerance = 5000000  # $5.00
    estimatedBalanceUsdc = tokenPriceUsdc * balance / 10 ** 6
    assert tokenPriceUsdc > 900000
    assert tokenPriceUsdc < 1100000
    assert balance > 0
    assert estimatedBalanceUsdc >= balanceUsdc - tolerance
    assert estimatedBalanceUsdc <= balanceUsdc + tolerance
    # assert balanceUsdc > balance / 10 ** 6 # This assumes the price of USDC >= 1

    # Test vault metadata
    pricePerShare = metadata[0]
    migrationAvailable = metadata[1]
    latestVaultAddress = metadata[2]
    depositLimit = metadata[3]
    emergencyShutdown = metadata[4]
    assert migrationAvailable == True
    assert latestVaultAddress != v2UsdcVaultV1Address
    assert latestVaultAddress != ZERO_ADDRESS
    assert depositLimit > 0
    assert emergencyShutdown == False


def test_assets_static(v2VaultsAdapter):
    assets = v2VaultsAdapter.assetsStatic()
    assert len(assets) > 1
    firstAsset = assets[0]
    assetId = firstAsset[0]
    assetTypeId = firstAsset[1]
    assetTokenId = firstAsset[2]
    assetName = firstAsset[3]
    assetVersion = firstAsset[4]
    assetSymbol = firstAsset[5]
    assetDecimals = firstAsset[6]
    assert assetId == yfiVaultAddress
    assert assetTypeId == "VAULT_V2"
    assert assetTokenId == yfiAddress
    assert assetName == "YFI yVault"
    assert assetVersion == "0.3.2"
    assert assetSymbol == "yvYFI"
    assert assetDecimals == 18
    # print(assets)


def test_assets_dynamic(v2VaultsAdapter):
    assets = v2VaultsAdapter.assetsDynamic([v2YfiVaultAddress, v2UsdcVaultV2Address])
    assert len(assets) > 1
    firstAsset = assets[0]
    assetId = firstAsset[0]
    assetTypeId = firstAsset[1]
    assetTokenId = firstAsset[2]
    assetUnderlyingTokenBalance = firstAsset[3]
    assetMetadata = firstAsset[4]
    assert assetId == yfiVaultAddress
    assert assetTypeId == "VAULT_V2"
    assert assetTokenId == yfiAddress
    assert assetUnderlyingTokenBalance[0] > 0
    assert assetUnderlyingTokenBalance[1] > 0
    secondAsset = assets[1]
    assetId = secondAsset[0]
    assetTypeId = secondAsset[1]
    assetTokenId = secondAsset[2]
    assetUnderlyingTokenBalance = secondAsset[3]
    assetMetadata = secondAsset[4]
    assert assetId == v2UsdcVaultV2Address
    assert assetTypeId == "VAULT_V2"
    assert assetTokenId == usdcAddress
    assert assetUnderlyingTokenBalance[0] > 0
    assert assetUnderlyingTokenBalance[1] > 0
    # print(assets)


def test_asset_positions_of(v2VaultsAdapter, oracle, accounts):
    # Deposit into YFI vault
    yfiAccount = accounts.at(vestedYfiAddress, force=True)
    yfi = Contract.from_explorer(yfiAddress)
    yfi.approve(v2YfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
    yfiVault = interface.IV2Vault(v2YfiVaultAddress)
    # yfiVault.deposit(0.5 * 10 ** 18, {"from": yfiAccount})
    yfiVault.approve(trustedMigratorAddress, 100, {"from": vestedYfiAddress})
    pricePerShare = yfiVault.pricePerShare()
    decimals = yfiVault.decimals()
    userVaultBalanceShares = yfiVault.balanceOf(vestedYfiAddress)
    userVaultBalance = userVaultBalanceShares * pricePerShare / 10 ** decimals
    userVaultBalanceUsdc = oracle.getNormalizedValueUsdc(yfiAddress, userVaultBalance)
    assert userVaultBalanceShares > 0
    positions = v2VaultsAdapter.assetPositionsOf(vestedYfiAddress, v2YfiVaultAddress)
    position = positions[0]

    # Test basic info
    assetId = position[0]
    tokenId = position[1]
    typeId = position[2]
    balance = position[3]
    assert assetId == v2YfiVaultAddress
    assert tokenId == yfiAddress
    assert typeId == "DEPOSIT"
    assert balance == userVaultBalanceShares

    # Test account asset balance
    underlyingTokenBalance = position[4]
    underlyingTokenBalanceAmount = underlyingTokenBalance[0]
    underlyingTokenBalanceAmountUsdc = underlyingTokenBalance[1]
    assert userVaultBalanceUsdc >= underlyingTokenBalanceAmountUsdc - 100
    assert userVaultBalanceUsdc <= underlyingTokenBalanceAmountUsdc + 100
    assert underlyingTokenBalanceAmountUsdc > underlyingTokenBalanceAmount / 10 ** 18

    # Test token allowances
    tokenAllowances = position[5]
    owner = tokenAllowances[0][0]
    spender = tokenAllowances[0][1]
    allowance = tokenAllowances[0][2]
    assert owner == vestedYfiAddress
    assert spender == v2YfiVaultAddress
    assert allowance > 0

    # Position allowances
    positionAllowances = position[6]
    owner = positionAllowances[0][0]
    spender = positionAllowances[0][1]
    allowance = positionAllowances[0][2]
    assert owner == vestedYfiAddress
    assert spender == trustedMigratorAddress
    assert allowance == 100

    # Test assetPositionOf


def test_assets_positions_of(v2VaultsAdapter, oracle):
    # Deposit into YFI vault
    yfi = interface.IERC20(yfiAddress)
    yfi.approve(v2YfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
    yfiVault = interface.IV2Vault(v2YfiVaultAddress)
    # yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
    yfiVault.approve(trustedMigratorAddress, 100, {"from": vestedYfiAddress})
    userVaultBalanceShares = yfiVault.balanceOf(vestedYfiAddress)
    assert userVaultBalanceShares > 0

    # Test positionsOf(address, [...address])
    positions = v2VaultsAdapter.assetsPositionsOf(
        vestedYfiAddress, [v2YfiVaultAddress, v2UsdcVaultV2Address]
    )
    position = positions[0]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == v2YfiVaultAddress


def test_set_position_spender_addresses(v2AddressesGenerator, management, rando):
    with brownie.reverts():
        v2AddressesGenerator.setPositionSpenderAddresses(
            [ethZapAddress], {"from": rando}
        )
    v2AddressesGenerator.setPositionSpenderAddresses(
        [ethZapAddress], {"from": management}
    )
    assert v2AddressesGenerator.positionSpenderAddresses(0) == ethZapAddress
