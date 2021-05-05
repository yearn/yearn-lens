import pytest
import brownie
from brownie import web3


@pytest.fixture
def v2VaultsAdapter(RegisteryAdapterV2Vault, managementList, management, oracle):
    v2RegistryAddress = "0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804"
    return RegisteryAdapterV2Vault.deploy(
        v2RegistryAddress, oracle, managementList, [], {"from": management}
    )


@pytest.fixture
def v1VaultsAdapter(RegisteryAdapterV1Vault, management, oracle):
    v1RegistryAddress = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0"
    return RegisteryAdapterV1Vault.deploy(v1RegistryAddress, {"from": management})


@pytest.fixture
def lens(
    Lens, managementList, management, earnAdapter, v2VaultsAdapter, v1VaultsAdapter
):
    lens = Lens.deploy(managementList, {"from": management})
    lens.addAdapter(v2VaultsAdapter, {"from": management})
    lens.addAdapter(v1VaultsAdapter, {"from": management})
    lens.addAdapter(earnAdapter, {"from": management})
    return lens


def test_add_adapter(
    Lens, management, earnAdapter, managementList, RegistryAdapterEarn
):
    lens = Lens.deploy(managementList, {"from": management})
    assert len(lens.adapters()) == 0
    lens.addAdapter(earnAdapter, {"from": management})
    assert len(lens.adapters()) == 1
    assert lens.adapters()[0] == earnAdapter
    adapterInfo = lens.adaptersInfo()[0]
    adapterInfoId = adapterInfo[0]
    adapterInfoTypeId = adapterInfo[1]
    adapterInfoCategoryId = adapterInfo[2]
    adapterInfoSubcategoryId = adapterInfo[3]
    assert adapterInfoId == earnAdapter
    assert adapterInfoTypeId == "earn"
    assert adapterInfoCategoryId == "deposit"
    assert adapterInfoSubcategoryId == "safe"


def test_add_adapters(Lens, management, managementList, earnAdapter, v1VaultsAdapter):
    lens = Lens.deploy(managementList, {"from": management})
    assert len(lens.adapters()) == 0
    lens.addAdapters([earnAdapter, v1VaultsAdapter], {"from": management})
    assert len(lens.adapters()) == 2

    adapterInfo1 = lens.adaptersInfo()[0]
    adapterInfo1Id = adapterInfo1[0]
    adapterInfo1TypeId = adapterInfo1[1]
    adapterInfo1CategoryId = adapterInfo1[2]
    adapterInfo1SubcategoryId = adapterInfo1[3]
    assert adapterInfo1Id == earnAdapter
    assert adapterInfo1TypeId == "earn"
    assert adapterInfo1CategoryId == "deposit"
    assert adapterInfo1SubcategoryId == "safe"

    adapterInfo2 = lens.adaptersInfo()[1]
    adapterInfo2Id = adapterInfo2[0]
    adapterInfo2TypeId = adapterInfo2[1]
    adapterInfo2CategoryId = adapterInfo2[2]
    adapterInfo2SubcategoryId = adapterInfo2[3]
    assert adapterInfo2Id == v1VaultsAdapter
    assert adapterInfo2TypeId == "v1Vault"
    assert adapterInfo2CategoryId == "deposit"
    assert adapterInfo2SubcategoryId == "vault"


def test_remove_adapter(lens, earnAdapter, management):
    assert len(lens.adapters()) == 3
    lens.removeAdapter(earnAdapter, {"from": management})
    assert len(lens.adapters()) == 2


# def test_assets_from_adapter(lens):


# def test_assets_length(lens):
#     length = lens.assetsLength()
#     print(length)
#     assert length > 0


def test_assets_addresses(lens):
    assert len(lens.assetsAddresses()) > 0


# def test_assets(lens):

# def test_positions_from_adapter(lens):

# def test_positions_of(lens):

