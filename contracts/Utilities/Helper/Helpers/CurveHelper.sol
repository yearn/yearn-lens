// SPDX-License-Identifier: MIT

pragma solidity ^0.8.6;

struct LpMetadata {
    address lpAddress;
    address poolAddress;
    address gaugeAddress;
    uint256 gaugeWeight;
    uint256 workingSupply;
    uint256 inflationWeight;
    uint256 poolPrice;
    uint256 baseAssetPrice;
    uint256 crvPrice;
    uint256 baseApr;
}

interface IOracle {
    function getPriceUsdcRecommended(address tokenAddress)
        external
        view
        returns (uint256);
}

interface IAddressesMergeHelper {
    function mergeAddresses(address[][] memory addressesSets)
        external
        view
        returns (address[] memory);
}

interface IStrategiesHelper {
    function assetStrategiesAddresses(address)
        external
        view
        returns (address[] memory);
}

interface IGauge {
    function controller() external view returns (address);

    function working_supply() external view returns (uint256);

    function working_balances(address) external view returns (uint256);

    function totalSupply() external view returns (uint256);

    function inflation_rate() external view returns (uint256);

    function balanceOf(address) external view returns (uint256);

    function user_checkpoint(address) external;
}

interface ICvx {
    function totalSupply() external view returns (uint256);
}

interface ICalculationsCurve {
    function isCurveLpToken(address) external view returns (bool);

    function getBasePrice(address) external view returns (uint256);
}

interface IV2Vault {
    function token() external view returns (address);
}

interface IAddressesGenerator {
    function assetsAddresses() external view returns (address[] memory);
}

interface ICurveAddressesProvider {
    function max_id() external view returns (uint256);

    function get_registry() external view returns (address);

    function get_address(uint256) external view returns (address);
}

interface IGaugeController {
    function n_gauges() external view returns (uint256);

    function gauges(uint256) external view returns (address);

    function token() external view returns (address);

    function gauge_types(address) external view returns (uint256);

    function gauge_relative_weight(address) external view returns (uint256);

    function voting_escrow() external view returns (address);

    function last_user_vote(address, address) external view returns (uint256);
}

interface IMetapoolFactory {
    function get_underlying_coins(address)
        external
        view
        returns (address[8] memory);
}

interface IRegistry {
    function get_pool_from_lp_token(address) external view returns (address);

    function gauge_controller() external view returns (address);

    function get_underlying_coins(address)
        external
        view
        returns (address[8] memory);

    function get_gauges(address) external view returns (address[10] memory);

    function pool_count() external view returns (uint256);

    function pool_list(uint256) external view returns (address);

    function coin_count() external view returns (uint256);

    function get_coin(uint256) external view returns (address);

    function get_lp_token(address) external view returns (address);

    function get_virtual_price_from_lp_token(address)
        external
        view
        returns (uint256);
}

interface IYearnAddressesProvider {
    function addressById(string memory) external view returns (address);
}

uint256 constant COMPOUNDING = 52;
uint256 constant SECONDS_PER_YEAR = 31536000;
uint256 constant SECONDS_PER_DAY = 86400;
uint256 constant MAX_BOOST = 250;
uint256 constant PER_MAX_BOOST = 10000 / MAX_BOOST;

contract CurveHelper {
    // yearn vaults   ✓
    // yearn lps      ✓
    // yearn pools    ✓
    // yearn gauges   ✓
    // all gauges     ✓
    // all lps        ✓
    // all pools      ✓
    // all tokens     x
    // vault > lp     ✓
    // vault > pool   x
    // vault > gauge  x
    // lp > vault     x
    // lp > pool      x
    // lp > gauge     x
    // lp > tokens    ✓
    // pool > vault   x
    // pool > lp      ✓
    // pool > gauge   ✓
    // pool > tokens  x

    address public yearnAddressesProviderAddress;
    address public curveAddressesProviderAddress;
    address public crvAddress;
    address public cvxAddress;

    IYearnAddressesProvider internal yearnAddressesProvider;
    ICurveAddressesProvider internal curveAddressesProvider;

    constructor(
        address _yearnAddressesProviderAddress,
        address _curveAddressesProviderAddress
    ) {
        curveAddressesProviderAddress = _curveAddressesProviderAddress;
        yearnAddressesProviderAddress = _yearnAddressesProviderAddress;
        yearnAddressesProvider = IYearnAddressesProvider(
            _yearnAddressesProviderAddress
        );
        curveAddressesProvider = ICurveAddressesProvider(
            _curveAddressesProviderAddress
        );

        // crvAddress = gaugeController().token();
        crvAddress = address(0xD533a949740bb3306d119CC777fa900bA034cd52);
        cvxAddress = address(0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B);
    }

    function registryAddress() public view returns (address) {
        return curveAddressesProvider.get_registry();
    }

    function metapoolFactoryAddress() public view returns (address) {
        return curveAddressesProvider.get_address(3);
    }

    function registry() internal view returns (IRegistry) {
        return IRegistry(registryAddress());
    }

    function underlyingTokensAddressesFromLpAddress(address poolAddress)
        public
        view
        returns (address[] memory)
    {
        address[] memory underlyingTokensAddresses = new address[](16);
        uint256 currentIdx;

        address[8]
            memory registryUnderlyingTokensAddresses = registryTokensAddressesFromPoolAddress(
                poolAddress
            );

        address[8]
            memory metapoolUnderlyingTokensAddresses = metapoolTokensAddressesFromPoolAddress(
                poolAddress
            );
        for (
            uint256 tokenIdx;
            tokenIdx < registryUnderlyingTokensAddresses.length;
            tokenIdx++
        ) {
            address tokenAddress = registryUnderlyingTokensAddresses[tokenIdx];
            if (tokenAddress != address(0)) {
                underlyingTokensAddresses[currentIdx] = tokenAddress;
                currentIdx++;
            }
        }
        for (
            uint256 tokenIdx;
            tokenIdx < metapoolUnderlyingTokensAddresses.length;
            tokenIdx++
        ) {
            address tokenAddress = metapoolUnderlyingTokensAddresses[tokenIdx];
            if (tokenAddress != address(0)) {
                underlyingTokensAddresses[currentIdx] = tokenAddress;
                currentIdx++;
            }
        }
        bytes memory encodedAddresses = abi.encode(underlyingTokensAddresses);
        assembly {
            mstore(add(encodedAddresses, 0x40), currentIdx)
        }
        address[] memory filteredAddresses = abi.decode(
            encodedAddresses,
            (address[])
        );
        return filteredAddresses;
    }

    function registryTokensAddressesFromPoolAddress(address poolAddress)
        public
        view
        returns (address[8] memory)
    {
        address[8] memory tokensAddresses = registry().get_underlying_coins(
            poolAddress
        );
        return tokensAddresses;
    }

    function metapoolTokensAddressesFromPoolAddress(address poolAddress)
        public
        view
        returns (address[8] memory)
    {
        address[8] memory tokensAddresses = IMetapoolFactory(
            metapoolFactoryAddress()
        ).get_underlying_coins(poolAddress);
        return tokensAddresses;
    }

    function lastVoteTimestamp(address voterAddress, address gaugeAddress)
        public
        view
        returns (uint256)
    {
        return gaugeController().last_user_vote(voterAddress, gaugeAddress);
    }

    function voterCanVoteForGauge(address voterAddress, address gaugeAddress)
        public
        view
        returns (bool)
    {
        uint256 VOTE_DELAY = 10 * SECONDS_PER_DAY;
        uint256 _lastVote = lastVoteTimestamp(voterAddress, gaugeAddress);
        return _lastVote + VOTE_DELAY < block.timestamp;
    }

    function poolAddressFromLpAddress(address lpAddress)
        public
        view
        returns (address)
    {
        address[8]
            memory metapoolTokensAddresses = metapoolTokensAddressesFromPoolAddress(
                lpAddress
            );
        for (uint256 tokenIdx; tokenIdx < 8; tokenIdx++) {
            address tokenAddress = metapoolTokensAddresses[tokenIdx];
            if (tokenAddress != address(0)) {
                return lpAddress;
            }
        }
        return registry().get_pool_from_lp_token(lpAddress);
    }

    function gaugesAddressesFromLpAddress(address lpAddress)
        public
        view
        returns (address[] memory)
    {
        address poolAddress = poolAddressFromLpAddress(lpAddress);
        address[] memory gaugeAddresses = gaugesAddressesFromPoolAddress(
            poolAddress
        );
        return gaugeAddresses;
    }

    function gaugesAddressesFromPoolAddress(address poolAddress)
        public
        view
        returns (address[] memory)
    {
        address[10] memory _gaugesAddresses = registry().get_gauges(
            poolAddress
        );
        address[] memory filteredGaugesAddresses = new address[](10);
        uint256 numberOfGauges;
        for (uint256 gaugeIdx; gaugeIdx < _gaugesAddresses.length; gaugeIdx++) {
            address gaugeAddress = _gaugesAddresses[gaugeIdx];
            if (gaugeAddress == address(0)) {
                break;
            }
            filteredGaugesAddresses[gaugeIdx] = gaugeAddress;
            numberOfGauges++;
        }
        bytes memory encodedAddresses = abi.encode(filteredGaugesAddresses);
        assembly {
            mstore(add(encodedAddresses, 0x40), numberOfGauges)
        }
        filteredGaugesAddresses = abi.decode(encodedAddresses, (address[]));
        return filteredGaugesAddresses;
    }

    function gaugesAddressesByPoolsAddressesSets(
        address[] memory _poolsAddresses
    ) public view returns (address[][] memory) {
        address[][] memory _gaugesAddresses = new address[][](
            _poolsAddresses.length
        );
        for (uint256 poolIdx = 0; poolIdx < _poolsAddresses.length; poolIdx++) {
            address poolAddress = _poolsAddresses[poolIdx];

            address[]
                memory _poolGaugesAddresses = gaugesAddressesFromPoolAddress(
                    poolAddress
                );
            _gaugesAddresses[poolIdx] = _poolGaugesAddresses;
        }
        return _gaugesAddresses;
    }

    function gaugesAddressesByPoolsAddresses(address[] memory _poolsAddresses)
        public
        view
        returns (address[] memory)
    {
        uint256 gaugesLength;
        address[] memory _gaugesAddresses = new address[](
            _poolsAddresses.length * 8
        );
        for (uint256 poolIdx = 0; poolIdx < _poolsAddresses.length; poolIdx++) {
            address poolAddress = _poolsAddresses[poolIdx];

            address[]
                memory _poolGaugesAddresses = gaugesAddressesFromPoolAddress(
                    poolAddress
                );
            for (
                uint256 gaugeIdx;
                gaugeIdx < _poolGaugesAddresses.length;
                gaugeIdx++
            ) {
                address gaugeAddress = _poolGaugesAddresses[gaugeIdx];
                _gaugesAddresses[gaugesLength] = gaugeAddress;
                gaugesLength++;
            }
        }
        bytes memory encodedAddresses = abi.encode(_gaugesAddresses);
        assembly {
            mstore(add(encodedAddresses, 0x40), gaugesLength)
        }
        address[] memory filteredAddresses = abi.decode(
            encodedAddresses,
            (address[])
        );
        return filteredAddresses;
    }

    // TODO: Return unique
    function yearnGaugesAddresses() public view returns (address[] memory) {
        address[] memory _yearnPoolsAddresses = yearnPoolsAddresses();
        return gaugesAddressesByPoolsAddresses(_yearnPoolsAddresses);
    }

    function lpsAddresses() public view returns (address[] memory) {
        address[] memory _poolsAddresses = poolsAddresses();
        uint256 numberOfPools = _poolsAddresses.length;
        address[] memory _lpsAddresses = new address[](numberOfPools);
        for (uint256 poolIdx; poolIdx < numberOfPools; poolIdx++) {
            address poolAddress = _poolsAddresses[poolIdx];
            _lpsAddresses[poolIdx] = registry().get_lp_token(poolAddress);
        }
        return _lpsAddresses;
    }

    function gaugesAddresses() public view returns (address[] memory) {
        uint256 numberOfGauges = gaugeController().n_gauges();
        address[] memory _gaugesAddresses = new address[](numberOfGauges);
        for (uint256 gaugeIdx; gaugeIdx < numberOfGauges; gaugeIdx++) {
            _gaugesAddresses[gaugeIdx] = gaugeController().gauges(gaugeIdx);
        }
        return _gaugesAddresses;
    }

    function gaugesAddressesEthChain() public view returns (address[] memory) {
        address[] memory _gaugesAddresses = gaugesAddresses();
        uint256 numberOfGauges = _gaugesAddresses.length;
        uint256 numberOfEthGauges;
        for (uint256 gaugeIdx; gaugeIdx < numberOfGauges; gaugeIdx++) {
            address gaugeAddress = gaugeController().gauges(gaugeIdx);
            IGauge gauge = IGauge(gaugeAddress);
            try gauge.working_balances(address(0)) {
                _gaugesAddresses[numberOfEthGauges] = gaugeAddress;
                numberOfEthGauges++;
            } catch {}
        }
        bytes memory encodedAddresses = abi.encode(_gaugesAddresses);
        assembly {
            mstore(add(encodedAddresses, 0x40), numberOfEthGauges)
        }
        address[] memory filteredAddresses = abi.decode(
            encodedAddresses,
            (address[])
        );
        return filteredAddresses;
        return filteredAddresses;
    }

    function gaugeControllerAddress() public view returns (address) {
        return registry().gauge_controller();
    }

    function gaugeController() internal view returns (IGaugeController) {
        return IGaugeController(gaugeControllerAddress());
    }

    function gaugesAddressesByTypeId(uint256 typeId)
        public
        view
        returns (address[] memory)
    {
        address[] memory _gaugesAddresses = gaugesAddresses();
        uint256 gaugesLength = _gaugesAddresses.length;
        address[] memory _gaugesAddressesByTypeId = new address[](gaugesLength);
        uint256 gaugesLengthByTypeId;
        for (uint256 gaugeIdx; gaugeIdx < gaugesLength; gaugeIdx++) {
            address gaugeAddress = _gaugesAddresses[gaugeIdx];
            uint256 gaugeTypeId = gaugeController().gauge_types(gaugeAddress);
            if (gaugeTypeId == typeId) {
                _gaugesAddressesByTypeId[gaugesLengthByTypeId] = gaugeAddress;
                gaugesLengthByTypeId++;
            }
        }
        bytes memory encodedAddresses = abi.encode(_gaugesAddressesByTypeId);
        assembly {
            mstore(add(encodedAddresses, 0x40), gaugesLengthByTypeId)
        }
        _gaugesAddressesByTypeId = abi.decode(encodedAddresses, (address[]));
        return _gaugesAddressesByTypeId;
    }

    function coinsAddresses() external view returns (address[] memory) {
        uint256 numberOfCoins = registry().coin_count();
        address[] memory _coinsAddresses = new address[](numberOfCoins);
        for (uint256 coinIdx; coinIdx < numberOfCoins; coinIdx++) {
            _coinsAddresses[coinIdx] = registry().get_coin(coinIdx);
        }
        return _coinsAddresses;
    }

    // TODO: Implement
    function cryptoPoolsAddresses() public view returns (address[] memory) {}

    function poolsAddresses() public view returns (address[] memory) {
        uint256 numberOfPools = registry().pool_count();
        address[] memory _poolsAddresses = new address[](numberOfPools);
        for (uint256 poolIdx; poolIdx < numberOfPools; poolIdx++) {
            _poolsAddresses[poolIdx] = registry().pool_list(poolIdx);
        }
        return _poolsAddresses;
    }

    function poolsAddressesByLpsAddresses(address[] memory _lpsAddresses)
        public
        view
        returns (address[] memory)
    {
        address[] memory _poolsAddresses = new address[](_lpsAddresses.length);
        for (uint256 lpIdx = 0; lpIdx < _lpsAddresses.length; lpIdx++) {
            address lpAddress = _lpsAddresses[lpIdx];
            address poolAddress = poolAddressFromLpAddress(lpAddress);
            _poolsAddresses[lpIdx] = poolAddress;
        }
        return _poolsAddresses;
    }

    function yearnPoolsAddresses() public view returns (address[] memory) {
        address[] memory _yearnLpsAddresses = yearnLpsAddresses();
        return poolsAddressesByLpsAddresses(_yearnLpsAddresses);
    }

    function getAddress(string memory _address) public view returns (address) {
        return yearnAddressesProvider.addressById(_address);
    }

    function curveCalculationsAddress() public view returns (address) {
        return getAddress("CALCULATIONS_CURVE");
    }

    function curveCalculations() internal view returns (ICalculationsCurve) {
        return ICalculationsCurve(curveCalculationsAddress());
    }

    function strategiesHelper() internal view returns (IStrategiesHelper) {
        return IStrategiesHelper(getAddress("HELPER_STRATEGIES"));
    }

    struct Deets {
        uint256 totalCliffs;
        uint256 reductionPerCliff;
        uint256 cvxSupply;
        uint256 cliff;
        uint256 claimableCrv;
        uint256 reduction;
        uint256 cvxMintedPerCrv;
        uint256 cvxCrvRatio;
        uint256 maxSupply;
        uint256 cvxPrintedAsCrv;
        uint256 cvxMultiplier;
    }

    function cvxMultiplier() public view returns (uint256) {
        uint256 totalCliffs = 1000 * 10**6;
        uint256 reductionPerCliff = 1e23;
        uint256 cvxSupply = ICvx(cvxAddress).totalSupply();
        uint256 cliff = (10**6 * cvxSupply) / reductionPerCliff;
        uint256 claimableCrv = 1 * 10**6;
        uint256 reduction = totalCliffs - cliff;
        uint256 cvxMintedPerCrv = (claimableCrv * reduction) / totalCliffs;
        uint256 maxSupply = 1e2 * 1e6 * 1e18;
        uint256 cvxPrintedAsCrv;
        uint256 cvxCrvRatio = (10**6 * cvxPriceUsdc()) / crvPriceUsdc();
        if (cvxSupply <= maxSupply) {
            cvxPrintedAsCrv = (cvxMintedPerCrv * cvxCrvRatio) / 10**10;
        } else {
            cvxPrintedAsCrv = 0;
        }
        uint256 cvxMultiplierBips = cvxPrintedAsCrv + 10**2;
        return cvxMultiplierBips;
    }

    function yearnVaultsAddresses() public view returns (address[] memory) {
        address[] memory vaultsAddresses = IAddressesGenerator(
            getAddress("ADDRESSES_GENERATOR_V2_VAULTS")
        ).assetsAddresses();
        uint256 currentIdx = 0;
        for (
            uint256 vaultIdx = 0;
            vaultIdx < vaultsAddresses.length;
            vaultIdx++
        ) {
            address vaultAddress = vaultsAddresses[vaultIdx];
            bool isCurveLpVault = curveCalculations().isCurveLpToken(
                IV2Vault(vaultAddress).token()
            );
            if (isCurveLpVault) {
                vaultsAddresses[currentIdx] = vaultAddress;
                currentIdx++;
            }
        }
        bytes memory encodedVaultsAddresses = abi.encode(vaultsAddresses);
        assembly {
            mstore(add(encodedVaultsAddresses, 0x40), currentIdx)
        }
        address[] memory filteredVaultsAddresses = abi.decode(
            encodedVaultsAddresses,
            (address[])
        );
        return filteredVaultsAddresses;
    }

    struct LpAddresses {
        address lpAddress;
        address poolAddress;
        address[] gaugeAddress;
    }

    function lpsMetadata() public view returns (LpAddresses[] memory) {
        address[] memory _lpsAddresses = lpsAddresses();
        return lpsMetadata(_lpsAddresses);
    }

    function lpsMetadata(address[] memory _lpsAddresses)
        public
        view
        returns (LpAddresses[] memory)
    {
        address[] memory _poolsAddresses = poolsAddressesByLpsAddresses(
            _lpsAddresses
        );

        address[][]
            memory _gaugesAddressesSet = gaugesAddressesByPoolsAddressesSets(
                _poolsAddresses
            );

        uint256 poolsLength = _poolsAddresses.length;
        LpAddresses[] memory _lpsMetadata = new LpAddresses[](poolsLength);
        for (uint256 poolIdx; poolIdx < poolsLength; poolIdx++) {
            LpAddresses memory metadata = LpAddresses({
                lpAddress: _lpsAddresses[poolIdx],
                poolAddress: _poolsAddresses[poolIdx],
                gaugeAddress: _gaugesAddressesSet[poolIdx]
            });
            _lpsMetadata[poolIdx] = metadata;
        }
        return _lpsMetadata;
    }

    function chainlinkPriceUsdc(address tokenAddress)
        public
        view
        returns (uint256)
    {}

    //   function isMetaPool() public view returns (bool) {

    //   }

    function yearnVaultsAddressesMetadata()
        public
        view
        returns (VaultAddressesMetadata[] memory)
    {
        address[] memory _yearnVaultsAddresses = yearnVaultsAddresses();
        return vaultsAddressesMetadata(_yearnVaultsAddresses);
    }

    struct VaultAddressesMetadata {
        address vaultAddress;
        address lpAddress;
        address poolAddress;
        address[] gaugesAddresses;
        address[] strategiesAddresses;
    }

    function vaultsAddressesMetadata(address[] memory _vaultsAddresses)
        public
        view
        returns (VaultAddressesMetadata[] memory)
    {
        address[] memory _lpsAddresses = lpsAddressesByVaultsAddresses(
            _vaultsAddresses
        );
        address[] memory _poolsAddresses = poolsAddressesByLpsAddresses(
            _lpsAddresses
        );

        address[][]
            memory _gaugesAddressesSets = gaugesAddressesByPoolsAddressesSets(
                _poolsAddresses
            );
        uint256 vaultsLength = _vaultsAddresses.length;

        VaultAddressesMetadata[]
            memory _vaultsMetadata = new VaultAddressesMetadata[](vaultsLength);
        for (uint256 vaultIdx; vaultIdx < vaultsLength; vaultIdx++) {
            address vaultAddress = _vaultsAddresses[vaultIdx];
            address[] memory _strategiesAddresses = strategiesHelper()
                .assetStrategiesAddresses(vaultAddress);
            VaultAddressesMetadata memory metadata = VaultAddressesMetadata({
                vaultAddress: vaultAddress,
                lpAddress: _lpsAddresses[vaultIdx],
                poolAddress: _poolsAddresses[vaultIdx],
                gaugesAddresses: _gaugesAddressesSets[vaultIdx],
                strategiesAddresses: _strategiesAddresses
            });
            _vaultsMetadata[vaultIdx] = metadata;
        }
        return _vaultsMetadata;
    }

    function lpAddressFromVaultAddress(address vaultAddress)
        public
        view
        returns (address)
    {
        IV2Vault vault = IV2Vault(vaultAddress);
        address lpTokenAddress = vault.token();
        return lpTokenAddress;
    }

    function lpsAddressesByVaultsAddresses(address[] memory _vaultsAddresses)
        public
        view
        returns (address[] memory)
    {
        address[] memory _lpsAddresses = new address[](_vaultsAddresses.length);
        for (
            uint256 vaultIdx = 0;
            vaultIdx < _vaultsAddresses.length;
            vaultIdx++
        ) {
            address vaultAddress = _vaultsAddresses[vaultIdx];
            IV2Vault vault = IV2Vault(vaultAddress);
            address lpTokenAddress = vault.token();
            _lpsAddresses[vaultIdx] = lpTokenAddress;
        }
        return _lpsAddresses;
    }

    function yearnLpsAddresses() public view returns (address[] memory) {
        address[] memory _vaultsAddresses = yearnVaultsAddresses();
        return lpsAddressesByVaultsAddresses(_vaultsAddresses);
    }

    function crvPriceUsdc() public view returns (uint256) {
        return IOracle(oracleAddress()).getPriceUsdcRecommended(crvAddress);
    }

    function cvxPriceUsdc() public view returns (uint256) {
        return IOracle(oracleAddress()).getPriceUsdcRecommended(cvxAddress);
    }

    function oracleAddress() public view returns (address) {
        return getAddress("ORACLE");
    }

    function lpMetadata(address lpAddress)
        public
        view
        returns (LpMetadata memory)
    {
        address gaugeAddress = gaugesAddressesFromLpAddress(lpAddress)[0];
        address poolAddress = poolAddressFromLpAddress(lpAddress);
        IGauge gauge = IGauge(gaugeAddress);
        uint256 gaugeWeight = IGaugeController(gaugeControllerAddress())
            .gauge_relative_weight(gaugeAddress);
        uint256 workingSupply = gauge.working_supply();
        uint256 inflationWeight = gauge.inflation_rate();
        uint256 poolPrice = registry().get_virtual_price_from_lp_token(
            lpAddress
        );
        uint256 baseAssetPrice = curveCalculations().getBasePrice(lpAddress);
        uint256 crvPrice = crvPriceUsdc();

        uint256 baseApr = (10**18 *
            inflationWeight *
            gaugeWeight *
            SECONDS_PER_YEAR *
            PER_MAX_BOOST *
            crvPrice) /
            baseAssetPrice /
            poolPrice /
            workingSupply;
        return
            LpMetadata({
                lpAddress: lpAddress,
                poolAddress: poolAddress,
                gaugeAddress: gaugeAddress,
                gaugeWeight: gaugeWeight,
                workingSupply: workingSupply,
                inflationWeight: inflationWeight,
                poolPrice: poolPrice,
                baseAssetPrice: baseAssetPrice,
                crvPrice: crvPrice,
                baseApr: baseApr
            });
    }
}
