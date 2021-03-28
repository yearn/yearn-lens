from brownie import RegisteryAdapterV2Vault, accounts


def main():
    v2RegistryAddress = "0xaF0A409307dF49Dac36f55DA2238A1E3a3679365"
    oracleAddress = "0x9b8b9F6146B29CC32208f42b995E70F0Eb2807F3"
    acct = accounts.load("deployment_account")
    RegisteryAdapterV2Vault.deploy(
        v2RegistryAddress,
        oracleAddress,
        {"from": acct, "gas_price": "1 gwei"},
        publish_source=True,
    )

