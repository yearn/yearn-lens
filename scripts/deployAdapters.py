from brownie import (
    RegisteryAdapterV1Vault,
    RegisteryAdapterV2Vault,
    RegistryAdapterEarn,
    ManagementList,
    RegistryAdapterIronBank,
    GenericRegistry,
    accounts,
)


def main():
    # managementListAddress = "0xf64e58Ee8C7BadC741A7ea98FB65488084385674"
    oracleAddress = "0xd3ca98d986be88b72ff95fc2ec976a5e6339150d"
    trustedMigratorAddress = "0x1824df8D751704FA10FA371d62A37f9B8772ab90"

    management = accounts[0]
    positionSpenderAddresses = [trustedMigratorAddress]

    # Deploy management list
    managementListAddress = ManagementList.deploy(
        "Managemenet list", {"from": management}
    )

    # Deploy v1 adapter
    v1RegistryAddress = "0x3eE41C098f9666ed2eA246f4D2558010e59d63A0"
    v1Adapter = RegisteryAdapterV1Vault.deploy(
        v1RegistryAddress, oracleAddress, managementListAddress, {"from": management},
    )
    v1Adapter.setPositionSpenderAddresses(
        positionSpenderAddresses, {"from": management}
    )

    # Deploy v2 adapter
    v2RegistryAddress = "0xaF0A409307dF49Dac36f55DA2238A1E3a3679365"
    v2Adapter = RegisteryAdapterV2Vault.deploy(
        v2RegistryAddress, oracleAddress, managementListAddress, {"from": management}
    )

    # Deploy earn registry
    earnRegistry = GenericRegistry.deploy({"from": management})
    yDaiV2Address = "0x16de59092dAE5CcF4A1E6439D611fd0653f0Bd01"
    yUsdcV2Address = "0xd6aD7a6750A7593E092a9B218d66C0A814a3436e"
    yUsdtV2Address = "0x83f798e925BcD4017Eb265844FDDAbb448f1707D"
    ySusdV2Address = "0xF61718057901F84C4eEC4339EF8f0D86D2B45600"
    yTusdV2Address = "0x73a052500105205d34daf004eab301916da8190f"
    yWbtcV2Address = "0x04Aa51bbcB46541455cCF1B8bef2ebc5d3787EC9"
    yDaiV3Address = "0xC2cB1040220768554cf699b0d863A3cd4324ce32"
    yUsdcV3Address = "0x26EA744E5B887E5205727f55dFBE8685e3b21951"
    yUsdtV3Address = "0xE6354ed5bC4b393a5Aad09f21c46E101e692d447"
    yBusdV3Address = "0x04bC0Ab673d88aE9dbC9DA2380cB6B79C4BCa9aE"
    earnRegistry.addAssets(
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

    # Deploy earn adapter
    earnAdapter = RegistryAdapterEarn.deploy(
        earnRegistry, oracleAddress, managementListAddress, {"from": management},
    )
    earnAdapter.setPositionSpenderAddresses(
        positionSpenderAddresses, {"from": management}
    )

    # Deploy Iron Bank adapter
    comptrollerAddress = "0xAB1c342C7bf5Ec5F02ADEA1c2270670bCa144CbB"
    ironBankAdapter = RegistryAdapterIronBank.deploy(
        comptrollerAddress, oracleAddress, managementListAddress, {"from": management}
    )

    # print("Management List: ", managementListAddress)
    # print("Earn Registry:   ", earnRegistry)
    print("Earn Adapter:    ", earnAdapter)
    print("V1 Adapter:      ", v1Adapter)
    print("V2 Adapter:      ", v2Adapter)
    print("IB Adapter:      ", ironBankAdapter)
