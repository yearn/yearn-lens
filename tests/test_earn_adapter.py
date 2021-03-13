import pytest


USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
ETH = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
YFI = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"


@pytest.fixture
def oracle(Oracle, gov):
    return gov.deploy(Oracle)


def test_earn_adapter(oracle, GenericRegistry, RegistryAdapterEarn, gov):
    earnRegistry = GenericRegistry.deploy({"from": gov})

    # Earn v1
    yDaiV1Address = "0x16de59092dAE5CcF4A1E6439D611fd0653f0Bd01"
    yUsdV1Address = "0xd6aD7a6750A7593E092a9B218d66C0A814a3436e"
    yUsdtV1Address = "0x83f798e925BcD4017Eb265844FDDAbb448f1707D"
    yTusdV1Address = "0x73a052500105205d34daf004eab301916da8190f"
    ySusdV1Address = "0xF61718057901F84C4eEC4339EF8f0D86D2B45600"

    # Earn v2
    yDaiV2Address = "0xC2cB1040220768554cf699b0d863A3cd4324ce32"
    yUsdcV2Address = "0x26EA744E5B887E5205727f55dFBE8685e3b21951"
    yUsdtV2Address = "0xE6354ed5bC4b393a5Aad09f21c46E101e692d447"
    yBusdV2Address = "0x04bC0Ab673d88aE9dbC9DA2380cB6B79C4BCa9aE"
    yWbtcV2Address = "0x04Aa51bbcB46541455cCF1B8bef2ebc5d3787EC9"

    earnRegistry.addAssets(
        [
            yDaiV1Address,
            yUsdV1Address,
            yTusdV1Address,
            yUsdtV1Address,
            ySusdV1Address,
            yDaiV2Address,
            yUsdcV2Address,
            yUsdtV2Address,
            yBusdV2Address,
            yWbtcV2Address,
        ]
    )

    # earnRegistry.addAsset(yUsdcV2Address)
    # earnRegistry.addAsset(yBusdV2Address)

    earnAdapter = RegistryAdapterEarn.deploy(earnRegistry, oracle, {"from": gov})
    # print("Asset addresses", earnAdapter.getAssetsAddresses())
    # print("Earn assets", earnAdapter.getAssets())
    # print("yDaiV1", earnAdapter.getAssetTvl(yDaiV1Address))
    # print("yUsdV1", earnAdapter.getAssetTvl(yUsdV1Address))
    # print("yTusdV1", earnAdapter.getAssetTvl(yTusdV1Address))
    # print("yUsdtV1", earnAdapter.getAssetTvl(yUsdtV1Address))
    # print("ySusdV1", earnAdapter.getAssetTvl(ySusdV1Address))
    # print("yDaiV2", earnAdapter.getAssetTvl(yDaiV2Address))
    # print("yUsdcV2", earnAdapter.getAssetTvl(yUsdcV2Address))
    # print("yUsdtV2", earnAdapter.getAssetTvl(yUsdtV2Address))
    # print("yBusdV2", earnAdapter.getAssetTvl(yBusdV2Address))
    # print("yWbtcV2", earnAdapter.getAssetTvl(yWbtcV2Address))

    # print("Oracle", oracle.getPriceUsdc("0x57Ab1ec28D129707052df4dF418D58a2D46d5f51"))
    print("Earn TVL", earnAdapter.getTvl())

