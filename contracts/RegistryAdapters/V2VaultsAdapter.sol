// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

// Common imports
import "../../interfaces/Common/IERC20.sol";
import "../../interfaces/Common/IOracle.sol";
import "../Utilities/Manageable.sol";

// Adapter-specific imports
import "../../interfaces/Yearn/V2Vault.sol";
import "../../interfaces/Yearn/IV2Registry.sol";

contract RegisteryAdapterV2Vault is Manageable {
    /**
     * Common code shared by all adapters
     */
    IOracle public oracle;
    address public registryAddress;
    address[] public positionSpenderAddresses;

    struct AdapterInfo {
        address id;
        string typeId;
        string categoryId;
        string subcategoryId;
    }

    struct Position {
        address assetId;
        uint256 balance;
        uint256 balanceUsdc;
        TokenPosition tokenPosition;
        Allowance[] allowances;
    }

    struct Token {
        address id;
        string name;
        string symbol;
        uint8 decimals;
        uint256 priceUsdc;
    }

    struct TokenPosition {
        address tokenId;
        uint256 balance;
        uint256 balanceUsdc;
        Allowance[] allowances;
    }

    struct Allowance {
        address owner;
        address spender;
        uint256 amount;
    }

    constructor(
        address _registryAddress,
        address _oracleAddress,
        address _managementListAddress,
        address[] memory _positionSpenderAddresses
    ) Manageable(_managementListAddress) {
        require(_registryAddress != address(0), "Missing registry address");
        require(_oracleAddress != address(0), "Missing oracle address");
        require(
            _managementListAddress != address(0),
            "Missing management list address"
        );
        registryAddress = _registryAddress;
        oracle = IOracle(_oracleAddress);
        setPositionSpenderAddresses(_positionSpenderAddresses);
    }

    function setPositionSpenderAddresses(address[] memory addresses)
        public
        onlyManagers
    {
        positionSpenderAddresses = addresses;
    }

    function assets() external view returns (Asset[] memory) {
        address[] memory assetAddresses = assetsAddresses();
        uint256 numberOfAssets = assetAddresses.length;
        Asset[] memory _assets = new Asset[](numberOfAssets);
        for (uint256 i = 0; i < numberOfAssets; i++) {
            address assetAddress = assetAddresses[i];
            Asset memory _asset = asset(assetAddress);
            _assets[i] = _asset;
        }
        return _assets;
    }

    function token(address tokenAddress) internal view returns (Token memory) {
        IERC20 underlyingToken = IERC20(tokenAddress);
        Token memory _token =
            Token({
                id: tokenAddress,
                name: underlyingToken.name(),
                symbol: underlyingToken.symbol(),
                decimals: underlyingToken.decimals(),
                priceUsdc: oracle.getPriceUsdcRecommended(tokenAddress)
            });
        return _token;
    }

    function assetsTvl() external view returns (uint256) {
        uint256 tvl;
        address[] memory assetAddresses = assetsAddresses();
        uint256 numberOfAssets = assetAddresses.length;
        for (uint256 i = 0; i < numberOfAssets; i++) {
            address assetAddress = assetAddresses[i];
            uint256 _assetTvl = assetTvl(assetAddress);
            tvl += _assetTvl;
        }
        return tvl;
    }

    /**
     * V2 Vaults Adapter
     */
    function adapterInfo() public view returns (AdapterInfo memory) {
        return
            AdapterInfo({
                id: address(this),
                typeId: "v2Vault",
                categoryId: "deposit",
                subcategoryId: "vault"
            });
    }

    struct Asset {
        address id;
        string typeId;
        string name;
        string version;
        uint256 balance;
        uint256 balanceUsdc;
        Token token;
        AssetMetadata metadata;
    }

    struct AssetMetadata {
        string symbol;
        uint256 pricePerShare;
        bool migrationAvailable;
        address latestVaultAddress;
        uint256 depositLimit;
        bool emergencyShutdown;
    }

    function assetsLength() public view returns (uint256) {
        IV2Registry registry = IV2Registry(registryAddress);
        uint256 numTokens = registry.numTokens();
        uint256 numVaults;
        for (uint256 i = 0; i < numTokens; i++) {
            address currentToken = registry.tokens(i);
            uint256 numVaultsForToken = registry.numVaults(currentToken);
            numVaults += numVaultsForToken;
        }
        return numVaults;
    }

    function assetsAddresses() public view returns (address[] memory) {
        uint256 numVaults = assetsLength();
        address[] memory vaultAddresses = new address[](numVaults);
        IV2Registry registry = IV2Registry(registryAddress);
        uint256 numTokens = registry.numTokens();
        uint256 currentVaultIdx;
        for (uint256 tokenIdx = 0; tokenIdx < numTokens; tokenIdx++) {
            address currentTokenAddress = registry.tokens(tokenIdx);
            uint256 numVaultsForToken = registry.numVaults(currentTokenAddress);
            for (
                uint256 vaultTokenIdx = 0;
                vaultTokenIdx < numVaultsForToken;
                vaultTokenIdx++
            ) {
                address currentVaultAddress =
                    registry.vaults(currentTokenAddress, vaultTokenIdx);
                vaultAddresses[currentVaultIdx] = currentVaultAddress;
                currentVaultIdx++;
            }
        }
        return vaultAddresses;
    }

    function assetTvl(address vaultAddress) public view returns (uint256) {
        V2Vault vault = V2Vault(vaultAddress);
        uint256 amount = vault.totalAssets();
        address underlyingTokenAddress = vault.token();
        uint256 tvl =
            oracle.getNormalizedValueUsdc(underlyingTokenAddress, amount);
        return tvl;
    }

    function asset(address vaultAddress) public view returns (Asset memory) {
        V2Vault vault = V2Vault(vaultAddress);
        IV2Registry registry = IV2Registry(registryAddress);
        uint256 totalSupply = vault.totalSupply();
        uint256 pricePerShare = 0;
        bool vaultHasShares = totalSupply != 0;
        if (vaultHasShares) {
            pricePerShare = vault.pricePerShare();
        }
        address vaultTokenAddress = vault.token();

        address latestVaultAddress = registry.latestVault(vaultTokenAddress);
        bool migrationAvailable = latestVaultAddress != vaultAddress;

        AssetMetadata memory metadata =
            AssetMetadata({
                symbol: vault.symbol(),
                pricePerShare: pricePerShare,
                migrationAvailable: migrationAvailable,
                latestVaultAddress: latestVaultAddress,
                depositLimit: vault.depositLimit(),
                emergencyShutdown: vault.emergencyShutdown()
            });

        Asset memory _asset =
            Asset({
                id: vaultAddress,
                typeId: adapterInfo().typeId,
                name: vault.name(),
                version: vault.apiVersion(),
                balance: vault.totalAssets(),
                balanceUsdc: assetTvl(vaultAddress),
                token: token(vaultTokenAddress),
                metadata: metadata
            });
        return _asset;
    }

    function tokens() public view returns (Token[] memory) {
        IV2Registry registry = IV2Registry(registryAddress);
        uint256 numTokens = registry.numTokens();
        Token[] memory _tokens = new Token[](numTokens);
        for (uint256 i = 0; i < numTokens; i++) {
            address tokenAddress = registry.tokens(i);
            Token memory _token = token(tokenAddress);
            _tokens[i] = _token;
        }
        return _tokens;
    }

    function positionAllowances(address accountAddress, address vaultAddress)
        public
        view
        returns (Allowance[] memory)
    {
        V2Vault vault = V2Vault(vaultAddress);
        uint256 numberOfSpenders = positionSpenderAddresses.length;
        Allowance[] memory allowances = new Allowance[](numberOfSpenders);
        for (
            uint256 spenderIdx = 0;
            spenderIdx < numberOfSpenders;
            spenderIdx++
        ) {
            address spenderAddress = positionSpenderAddresses[spenderIdx];
            uint256 allowanceAmount =
                vault.allowance(accountAddress, spenderAddress);
            Allowance memory allowance =
                Allowance({
                    owner: accountAddress,
                    spender: spenderAddress,
                    amount: allowanceAmount
                });
            allowances[spenderIdx] = allowance;
        }
        return allowances;
    }

    function tokenPositionAllowances(
        address accountAddress,
        address vaultAddress
    ) public view returns (Allowance[] memory) {
        V2Vault vault = V2Vault(vaultAddress);
        address tokenAddress = vault.token();
        IERC20 _token = IERC20(tokenAddress);
        Allowance[] memory allowances = new Allowance[](1);
        uint256 allowanceAmount =
            _token.allowance(accountAddress, vaultAddress);
        Allowance memory allowance =
            Allowance({
                owner: accountAddress,
                spender: vaultAddress,
                amount: allowanceAmount
            });
        allowances[0] = allowance;
        return allowances;
    }

    function positionOf(address accountAddress, address vaultAddress)
        public
        view
        returns (Position memory)
    {
        V2Vault vault = V2Vault(vaultAddress);
        address tokenAddress = vault.token();
        IERC20 _token = IERC20(tokenAddress);
        uint256 balance = vault.balanceOf(accountAddress);
        uint256 balanceUsdc =
            oracle.getNormalizedValueUsdc(tokenAddress, balance);
        uint256 tokenBalance = _token.balanceOf(accountAddress);
        uint256 tokenBalanceUsdc =
            oracle.getNormalizedValueUsdc(tokenAddress, tokenBalance);

        Allowance[] memory _tokenPositionAllowances =
            tokenPositionAllowances(accountAddress, vaultAddress);
        Allowance[] memory _positionAllowances =
            positionAllowances(accountAddress, vaultAddress);

        TokenPosition memory tokenPosition =
            TokenPosition({
                tokenId: tokenAddress,
                balance: tokenBalance,
                balanceUsdc: tokenBalanceUsdc,
                allowances: _tokenPositionAllowances
            });

        Position memory position =
            Position({
                assetId: vaultAddress,
                balance: balance,
                balanceUsdc: balanceUsdc,
                tokenPosition: tokenPosition,
                allowances: _positionAllowances
            });
        return position;
    }

    function positionsOf(address accountAddress)
        external
        view
        returns (Position[] memory)
    {
        address[] memory vaultAddresses = assetsAddresses();
        uint256 numberOfVaults = vaultAddresses.length;
        Position[] memory positions = new Position[](numberOfVaults);
        for (uint256 vaultIdx = 0; vaultIdx < numberOfVaults; vaultIdx++) {
            address vaultAddress = vaultAddresses[vaultIdx];
            Position memory position = positionOf(accountAddress, vaultAddress);
            positions[vaultIdx] = position;
        }
        return positions;
    }
}
