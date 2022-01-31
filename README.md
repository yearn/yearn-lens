# Yearn Lens

## What you'll find here

- CI/CD pipelines used by Github Actions to provide linting checks and test runs. ([`workflows/`](`.github/workflows/`))

- A suite of Solidity Smart Contracts responsible for the Yearn Lens infrastructure. ([`contracts/`](`contracts/`))

- Interfaces for Yearn + external DeFi protocols on ethereum mainnet. ([`interfaces/`](`interfaces/`))

- Test suite that runs on a Brownie+Ganache mainnet fork. ([`tests/`](tests))

- Deployment script. ([`tests/`](tests))

This mix is configured for use with [Ganache](https://github.com/trufflesuite/ganache-cli) on a [forked mainnet](https://eth-brownie.readthedocs.io/en/stable/network-management.html#using-a-forked-development-network).

# Basic Use

## Installing dependencies

```bash
yarn install
pip3 install -r requirements-dev.txt
```

## Running linting

#### Solidity linting

```bash
yarn lint:check
yarn lint
```

#### Python tests linting

```bash
yarn lint:tests-check
yarn lint:tests
```

## Tests

See the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html) for more detailed information on testing your project.

### Running all tests

```bash
brownie test
```

### Running a single test file

```bash
brownie test tests/registry_adapters/test_adapter_vaults_v1.py
```

### Running a single test interactively

```bash
brownie test tests/registry_adapters/test_adapter_vaults_v1.py --interactive
```

## Known issues

### No access to archive state errors

If you are using Ganache to fork a network, then you may have issues with the blockchain archive state every 30 minutes. This is due to your node provider (i.e. Infura) only allowing free users access to 30 minutes of archive state. To solve this, upgrade to a paid plan, or simply restart your ganache instance and redploy your contracts.

Alternatively, Infura can be replaced with Alchemy API, which does not timeout after 30 minutes. This would require changes in your `~/.brownie/network-config.yaml` file, affecting global Brownie configuration. Works only with ganache < 7.0.0.
Following configuration is provided only for educational purposes, more information can be found in [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/config.html#networks). You will need to set `ALCHEMY_SECRET_KEY` environment variable, which can be found on [Alchemy dashboard](https://dashboard.alchemyapi.io/).

```yaml
development:
  - cmd: ganache-cli
    cmd_settings:
      accounts: 10
      evm_version: istanbul
      fork: mainnet-alchemy
      gas_limit: 12000000
      mnemonic: brownie
      port: 8545
    host: http://127.0.0.1
    id: mainnet-fork
    name: Ganache-CLI (Mainnet Fork)
    timeout: 120

live:
  - name: Ethereum
    networks:
      - chainid: 1
        explorer: https://api.etherscan.io/api
        host: https://eth-mainnet.alchemyapi.io/v2/$ALCHEMY_SECRET_KEY
        id: mainnet-alchemy
        name: Mainnet (Alchemy)
```
