import pytest
import brownie
from brownie import interface, ZERO_ADDRESS
from operator import itemgetter

yfiVaultAddress = "0xBA2E7Fed597fd0E3e70f5130BcDbbFE06bB94fe1"
yfiAddress = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
usdcAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
usdcVaultAddress = "0x597ad1e0c13bfe8025993d9e79c69e1c0233522e"
v1UsdcVaultV1Address = "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9"
ethZapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"
vestedYfiAddress = "0x42A28ADDC15E627d19e780c89043b4B1d3629D34"
trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
zapAddress = "0x5A0bade607eaca65A0FE6d1437E0e3EC2144d540"


@pytest.fixture
def v1VaultsAdapter(
    RegisteryAdapterV1Vault,
    helper,
    v1VaultsAddressesGenerator,
    v1VaultTvlAdapter,
    managementList,
    oracle,
    management,
):
    v1RegistryAddress = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0"
    trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"
    positionSpenderAddresses = [trustedMigratorAddress]
    adapter = RegisteryAdapterV1Vault.deploy(
        oracle,
        helper,
        v1VaultsAddressesGenerator,
        v1VaultTvlAdapter,
        {"from": management},
    )
    return adapter


# def test_interface(
#     v1VaultsAdapter, introspection, management, registryAdapterCommonInterface
# ):
#     adapterImplementsCommonInterface = introspection.implementsInterface(
#         v1VaultsAdapter, registryAdapterCommonInterface
#     )
#     assert adapterImplementsCommonInterface


# def test_adapter_info(v1VaultsAdapter):
#     adapterInfo = v1VaultsAdapter.adapterInfo()
#     assert adapterInfo[0] == v1VaultsAdapter
#     assert adapterInfo[1] == "VAULT_V1"
#     assert adapterInfo[2] == "VAULT"


# def test_registry_address(v1VaultsAdapter):
#     assert not v1VaultsAdapter.registry() == ZERO_ADDRESS


# def test_assets_length(v1VaultsAdapter):
#     assetsLength = v1VaultsAdapter.assetsLength()
#     assert assetsLength > 0


# def test_assets_addresses(v1VaultsAdapter):
#     assetsAddresses = v1VaultsAdapter.assetsAddresses()
#     assert len(assetsAddresses) > 0
#     assert not assetsAddresses[0] == ZERO_ADDRESS


# def test_asset_static(v1VaultsAdapter):
#     # test vault data
#     assetStatic = v1VaultsAdapter.assetStatic(usdcVaultAddress)
#     assetId = assetStatic[0]
#     assetTypeId = assetStatic[1]
#     name = assetStatic[2]
#     version = assetStatic[3]
#     assert assetId == usdcVaultAddress
#     assert name == "yearn USD//C"
#     assert version == "1.0.0"

#     # # Test token
#     token = assetStatic[4]
#     tokenId = token[0]
#     tokenName = token[1]
#     tokenSymbol = token[2]
#     tokenDecimals = token[3]

#     assert tokenId == usdcAddress
#     assert tokenName == "USD Coin"
#     assert tokenSymbol == "USDC"
#     assert tokenDecimals == 6


# def test_asset_dynamic(v1VaultsAdapter, oracle):
#     assetDynamic = v1VaultsAdapter.assetDynamic(usdcVaultAddress)
#     assetId = assetDynamic[0]
#     typeId = assetDynamic[1]
#     tokenId = assetDynamic[2]
#     underlyingTokenBalance = assetDynamic[3]
#     metadata = assetDynamic[4]

#     # Test vault underlying balances
#     tokenPriceUsdc = oracle.getPriceUsdcRecommended(tokenId)
#     balance = underlyingTokenBalance[0]
#     balanceUsdc = underlyingTokenBalance[1]
#     tolerance = 5000000  # $5.00
#     estimatedBalanceUsdc = tokenPriceUsdc * balance / 10 ** 6
#     assert tokenPriceUsdc > 900000
#     assert tokenPriceUsdc < 1100000
#     assert balance > 0
#     assert estimatedBalanceUsdc >= balanceUsdc - tolerance
#     assert estimatedBalanceUsdc <= balanceUsdc + tolerance


# assert balanceUsdc > balance / 10 ** 6 # This assumes the price of USDC >= 1

# Test vault metadata
# symbol = metadata[0]
# pricePerShare = metadata[1]
# migrationAvailable = metadata[2]
# latestVaultAddress = metadata[3]
# depositLimit = metadata[4]
# emergencyShutdown = metadata[5]
# assert migrationAvailable == True
# assert latestVaultAddress != v2UsdcVaultV1Address
# assert latestVaultAddress != ZERO_ADDRESS
# assert depositLimit > 0
# assert emergencyShutdown == False


# def test_asset_metadata(v1VaultsAdapter):
#     # Test vault metadata
#     asset = v1VaultsAdapter.asset(usdcVaultAddress)
#     metadata = asset[7]
#     symbol = metadata[0]
#     pricePerShare = metadata[1]
#     migrationAvailable = metadata[2]
#     latestVaultAddress = metadata[3]
#     depositLimit = metadata[4]
#     emergencyShutdown = metadata[5]
#     assert migrationAvailable == True
#     assert latestVaultAddress != usdcVaultAddress
#     assert latestVaultAddress != ZERO_ADDRESS
#     assert depositLimit > 0
#     assert emergencyShutdown == False


# def test_assets_static(v1VaultsAdapter):
#     assets = v1VaultsAdapter.assetsStatic()
#     assert len(assets) > 1
#     usdcVault = assets[2]
#     assetId = usdcVault[0]
#     assetTypeId = usdcVault[1]
#     assetName = usdcVault[2]
#     assetVersion = usdcVault[3]
#     assert assetId == usdcVaultAddress
#     assert assetName == "yearn USD//C"
#     assert assetTypeId == "VAULT_V1"
#     assert assetVersion == "1.0.0"


# test_assets_dynamic


def test_asset_positions_of(v1VaultsAdapter, management, accounts):
    # Deposit into YFI vault
    yfiAccount = accounts.at(vestedYfiAddress, force=True)
    yfi = interface.IERC20(yfiAddress)
    yfi.approve(yfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
    yfiVault = interface.V1Vault(yfiVaultAddress)
    yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
    yfiVault.approve(trustedMigratorAddress, 100, {"from": vestedYfiAddress})
    pricePerShare = yfiVault.getPricePerFullShare()
    decimals = yfiVault.decimals()
    userVaultBalance = (
        yfiVault.balanceOf(vestedYfiAddress) * pricePerShare / 10 ** decimals
    )
    assert userVaultBalance > 0

    # Test position
    positions = v1VaultsAdapter.assetPositionsOf(vestedYfiAddress, yfiVaultAddress)
    position = positions[0]
    assetId = position[0]
    categoryId = position[1]
    balance = position[2]
    balanceUsdc = position[3]
    assert assetId == yfiVaultAddress
    assert categoryId == "deposit"
    assert userVaultBalance >= balance - 100
    assert userVaultBalance <= balance + 100
    assert balanceUsdc > balance / 10 ** 18

    # Test token position
    tokenPosition = position[4]
    tokenAddress = tokenPosition[0]
    tokenBalance = tokenPosition[1]
    tokenBalanceUsdc = tokenPosition[2]
    assert tokenAddress == yfiAddress
    assert tokenBalance > 0
    assert tokenBalanceUsdc > tokenBalance / 10 ** 18

    # Test token allowances
    tokenAllowances = tokenPosition[3]
    owner = tokenAllowances[0][0]
    spender = tokenAllowances[0][1]
    allowance = tokenAllowances[0][2]
    assert owner == vestedYfiAddress
    assert spender == yfiVaultAddress
    assert allowance > 0

    # Position allowances
    positionAllowances = position[5]
    owner = positionAllowances[0][0]
    spender = positionAllowances[0][1]
    allowance = positionAllowances[0][2]
    assert owner == vestedYfiAddress
    assert spender == trustedMigratorAddress
    assert allowance == 100


def test_positions_of(v1VaultsAdapter, accounts):
    # Deposit into YFI vault
    yfiAccount = accounts.at(vestedYfiAddress, force=True)
    yfi = interface.IERC20(yfiAddress)
    yfi.approve(yfiVaultAddress, 2 ** 256 - 1, {"from": vestedYfiAddress})
    yfiVault = interface.V1Vault(yfiVaultAddress)
    yfiVault.deposit(1 * 10 ** 18, {"from": yfiAccount})
    pricePerShare = yfiVault.getPricePerFullShare()
    decimals = yfiVault.decimals()
    userVaultBalance = (
        yfiVault.balanceOf(vestedYfiAddress) * pricePerShare / 10 ** decimals
    )
    assert userVaultBalance > 0

    # Test positionsOf(address)
    positions = v1VaultsAdapter.positionsOf(vestedYfiAddress)
    position = positions[0]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == yfiVaultAddress

    # Test positionsOf(address, [...address])
    positions = v1VaultsAdapter.positionsOf(
        vestedYfiAddress, [yfiVaultAddress, v1UsdcVaultV1Address]
    )
    position = positions[0]
    assetId = position[0]
    assert len(positions) > 0
    assert assetId == yfiVaultAddress


def test_set_position_spender_addresses(
    v1VaultsAdapter, v1AddressesGenerator, management, rando
):
    with brownie.reverts():
        v1AddressesGenerator.setPositionSpenderAddresses(
            [ethZapAddress], {"from": rando}
        )
    v1AddressesGenerator.setPositionSpenderAddresses(
        [ethZapAddress], {"from": management}
    )
    assert v1AddressesGenerator.positionSpenderAddresses(0) == ethZapAddress
