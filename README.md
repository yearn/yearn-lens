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
yarn install --frozen-lockfile
pip install -r requirements-dev.txt
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

## Deployment Addresses

| Contract | Ethereum | Fantom | Arbitrum |
| -------- | -------- | ------ | -------- |
| AddressesProvider        | [Link](https://etherscan.io/address/0xe11dC9f2Ab122dC5978EACA41483Da0D7D7e6128) | [Link](https://ftmscan.com/address/0xac5A9E4135A3A26497F3890bFb602b06Ee592B61) | [Link](https://arbiscan.io/address/0xcAd10033C86B0C1ED6bfcCAa2FF6779938558E9f) |
| Oracle                   | [Link](https://etherscan.io/address/0x83d95e0D5f402511dB06817Aff3f9eA88224B030) | [Link](https://ftmscan.com/address/0x57AA88A0810dfe3f9b71a9b179Dd8bF5F956C46A) | [Link](https://arbiscan.io/address/0x043518ab266485dc085a1db095b8d9c2fc78e9b9) |
| CalculationsChainlink    | [Link](https://etherscan.io/address/0xc8D60D8273E69E63eAFc4EA342f96AD593A4ba10) | n/a | n/a |
| CalculationsChainlinkRegistry | n/a | n/a | [Link](https://arbiscan.io/address/0x9d032763693d4ef989b630de2eca8750bde88219) |
| CalculationsBand         | n/a | [Link](https://ftmscan.com/address/0xebaa0b431618bcd9ea67d39c232625c20880d9ba) | n/a |
| CalculationsFixedForex   | [Link](https://etherscan.io/address/0x9956ca141c344e177829671ec0f1a9d4ab3cb1fd) | n/a | n/a |
| CalculationsSynth        | [Link](https://etherscan.io/address/0x5a04749532195d5d16268da74775defcc843151a) | n/a | n/a |
| CalculationsCurve        | [Link](https://etherscan.io/address/0xf1c3047c6310806de1d25535bc50748815066a7b) | [Link](https://ftmscan.com/address/0x0b53e9df372e72d8fdcdbedfbb56059957a37128) | [Link](https://arbiscan.io/address/0x3268c3bda100ef0ff3c2d044f23eab62c80d78d2) |
| CalculationsYearnVaults  | [Link](https://etherscan.io/address/0x38477f2159638956d33e18951d98238a53b9aa3c) | n/a | n/a |
| CalculationsIronBank     | [Link](https://etherscan.io/address/0x5ee8d20afc721abefbb00bc7c049f0de832bee3e) | n/a | n/a |
| CalculationsUniswapV3    | [Link](https://etherscan.io/address/0x3df0f396cf5e472fa59c126fa765a176e1ceb0f6) | n/a | n/a |
| CalculationsSushiswap    | [Link](https://etherscan.io/address/0xab8be4f563f77fae19af22f4465340675e1d2154) | [Link](https://ftmscan.com/address/0x44536de2220987d098d1d29d3aafc7f7348e9ee4) | [Link](https://arbiscan.io/address/0x5ea7e501c9a23f4a76dc7d33a11d995b13a1dd25) |
| CalculationsSpookyswap   | n/a | [Link](https://ftmscan.com/address/0x560144c25e53149ac410e5d33bdb131e49a850e5#code) | n/a |
| CalculationsZeroPrice    | [Link](https://etherscan.io/address/0xa8b5ff097a10a264c30ec302023730fe51b7d8d7) | n/a | n/a |
| RegistryAdapterIronBank  | [Link](https://etherscan.io/address/0x5D03ad44F4Fce73407C73A1779295011691D2e1F) | [Link](https://ftmscan.com/address/0x1164587b49ff7ace303962cc7a7e0841c1b34986) | [Link](https://arbiscan.io/address/0x7aad416eb4e16a27b85e7076dd56742a44e9d25b) |
| RegistryAdapterV2Vaults  | [Link](https://etherscan.io/address/0x240315db938d44bb124ae619f5Fd0269A02d1271) | [Link](https://ftmscan.com/address/0xf628fb7436ffc382e2af8e63dd7ccbaa142e3cd1) | [Link](https://arbiscan.io/address/0x57aa88a0810dfe3f9b71a9b179dd8bf5f956c46a) |
| Helper                   | [Link](https://etherscan.io/address/0x5AACD0D03096039aC4381CD814637e9FB7C34a6f) | [Link](https://ftmscan.com/address/0xe55dd55b3355c261a048b3f310706c7478657d74) | [Link](https://arbiscan.io/address/0xe55dd55b3355c261a048b3f310706c7478657d74) |
| BalancesHelper           | [Link](https://etherscan.io/address/0x855ffe28019106d089bc018df18838f8d241c402) | [Link](https://ftmscan.com/address/0x6b8de08d2520c955554e837ae72022cd46ba7f0e) | [Link](https://arbiscan.io/address/0x94734ba0f9f8c2464d963a402743fd79b402efd7) |
| StrategiesHelper         | [Link](https://etherscan.io/address/0xae813841436fe29b95a14ac701afb1502c4cb789) | [Link](https://ftmscan.com/address/0x97d0be2a72fc4db90ed9dbc2ea7f03b4968f6938) | [Link](https://arbiscan.io/address/0x66a1a27f4b22dcaa24e427dcffbf0cddd9d35e0f) |
| PricesHelper             | [Link](https://etherscan.io/address/0x090ea08061b61c4d99b423cee8835017bd9d8b3e) | n/a | n/a |
| AllowancesHelper         | [Link](https://etherscan.io/address/0x4218e20db87023049fc582aaa4bd47a3611a20ab) | [Link](https://ftmscan.com/address/0x14785e5e3650f0603ee17401c9890de380713914) | [Link](https://arbiscan.io/address/0xf5875d60241c8f6448649206a6f485b812acf44d) |
| AddressMergeHelper       | [Link](https://etherscan.io/address/0x957e3ae7983155a9f9e08da555b8084448be26e4) | [Link](https://ftmscan.com/address/0x001d0a58b336f60ee050cb11ee455fd7eb984518) | n/a |
| ParnterTracker           | [Link](https://etherscan.io/address/0x8ee392a4787397126C163Cb9844d7c447da419D8) | n/a | n/a |
| CurveRegistryOverrides   | [Link](https://etherscan.io/address/0xc455D134AfCC5353317A4e5afb553Fd5Ab6C2eE3) | n/a | [Link](https://arbiscan.io/address/0x3d197c5b6ea199e04ed4c9002e8435bb371efeed) |
| AddressGeneratorV2Vaults | [Link]() | [Link](https://ftmscan.com/address/0x8ca27a3ab8917a033f278D20135d2467faA099bA) | n/a |
| AddressGeneratorIronBank | [Link]() | [Link](https://ftmscan.com/address/0x5ABdfDfa0cF2d83c4755E0a2a782eF57FEd5c23B) | [Link](https://arbiscan.io/address/0x941f727f267913e76e3f03a25d3bc7c07e891763) |
