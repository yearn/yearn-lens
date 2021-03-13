from brownie import Lens, accounts


def main():
    acct = accounts.load("deployment_account")
    Lens.deploy({"from": acct, "gas_price": "1 gwei"}, publish_source=True)
