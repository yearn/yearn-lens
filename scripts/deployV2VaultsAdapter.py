from brownie import RegisteryAdapterV2Vault, accounts


def main():
    v2RegistryAddress = "0xaF0A409307dF49Dac36f55DA2238A1E3a3679365"
    oracleAddress = "0xae813841436fe29b95a14ac701afb1502c4cb789"
    managementListAddress = "0xf64e58Ee8C7BadC741A7ea98FB65488084385674"
    acct = accounts.load("deployment_account")
    RegisteryAdapterV2Vault.deploy(
        v2RegistryAddress,
        oracleAddress,
        managementListAddress,
        {"from": acct, "gas_price": "1 gwei"},
        publish_source=True,
    )
