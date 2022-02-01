// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

// Adapter-specific imports
import "../../interfaces/Yearn/V1Registry.sol";

// Common imports
import "../../interfaces/Common/IERC20.sol";

interface IV1Vault {
  function token() external view returns (address);

  function name() external view returns (string memory);

  function symbol() external view returns (string memory);

  function decimals() external view returns (uint8);

  function controller() external view returns (address);

  function governance() external view returns (address);

  function getPricePerFullShare() external view returns (uint256);

  function balance() external view returns (uint256);

  function totalSupply() external view returns (uint256);

  function balanceOf(address account) external view returns (uint256);

  function deposit(uint256 amount) external;

  function approve(address spender, uint256 amount) external;

  function allowance(address spender, address owner)
    external
    view
    returns (uint256);
}

interface IHelper {
  // Strategies helper
  function assetStrategiesDelegatedBalance(address)
    external
    view
    returns (uint256);

  // Allowances helper
  struct Allowance {
    address owner;
    address spender;
    uint256 amount;
    address token;
  }

  function allowances(
    address ownerAddress,
    address[] memory tokensAddresses,
    address[] memory spenderAddresses
  ) external view returns (Allowance[] memory);
}

interface IAddressesGenerator {
  function assetsAddresses() external view returns (address[] memory);

  function assetsLength() external view returns (uint256);

  function registry() external view returns (address);

  function getPositionSpenderAddresses()
    external
    view
    returns (address[] memory);
}

interface IOracle {
  function getNormalizedValueUsdc(address tokenAddress, uint256 amount)
    external
    view
    returns (uint256);

  function getPriceUsdcRecommended(address tokenAddress)
    external
    view
    returns (uint256);
}

contract RegisteryAdapterV1Vault {
  /*******************************************************
   *           Common code shared by all adapters        *
   *******************************************************/

  IOracle public oracle; // The oracle is used to fetch USDC normalized pricing data
  IHelper public helper; // A helper utility is used for batch allowance fetching and address array merging
  IAddressesGenerator public addressesGenerator; // A utility for fetching assets addresses and length
  address public fallbackContractAddress; // Optional fallback proxy

  /**
   * High level static information about an asset
   */
  struct AssetStatic {
    address id; // Asset address
    string typeId; // Asset typeId (for example "VAULT_V2" or "IRON_BANK_MARKET")
    string name; // Asset Name
    string version; // Asset version
    Token token; // Static asset underlying token information
  }

  /**
   * High level dynamic information about an asset
   */
  struct AssetDynamic {
    address id; // Asset address
    string typeId; // Asset typeId (for example "VAULT_V2" or "IRON_BANK_MARKET")
    address tokenId; // Underlying token address;
    TokenAmount underlyingTokenBalance; // Underlying token balances
    AssetMetadata metadata; // Metadata specific to the asset type of this adapter
  }

  /**
   * Static token data
   */
  struct Token {
    address id; // Token address
    string name; // Token name
    string symbol; // Token symbol
    uint8 decimals; // Token decimals
  }

  /**
   * Information about a user's position relative to an asset
   */
  struct Position {
    address assetId; // Asset address
    address tokenId; // Underlying asset token address
    string typeId; // Position typeId (for example "DEPOSIT," "BORROW," "LEND")
    uint256 balance; // asset.balanceOf(account)
    TokenAmount accountTokenBalance; // User account balance of underlying token (token.balanceOf(account))
    TokenAmount underlyingTokenBalance; // Represents a user's asset position in underlying tokens
    Allowance[] tokenAllowances; // Underlying token allowances
    Allowance[] assetAllowances; // Asset allowances
  }

  /**
   * Token amount representation
   */
  struct TokenAmount {
    uint256 amount; // Amount in underlying token decimals
    uint256 amountUsdc; // Amount in USDC (6 decimals)
  }

  /**
   * Allowance information
   */
  struct Allowance {
    address owner; // Allowance owner
    address spender; // Allowance spender
    uint256 amount; // Allowance amount (in underlying token)
  }

  /**
   * Information about the adapter
   */
  struct AdapterInfo {
    address id; // Adapter address
    string typeId; // Adapter typeId (for example "VAULT_V2" or "IRON_BANK_MARKET")
    string categoryId; // Adapter categoryId (for example "VAULT")
  }

  /**
   * Fetch static information about an array of assets. This method can be used for off-chain pagination.
   */
  function assetsStatic(address[] memory _assetsAddresses)
    public
    view
    returns (AssetStatic[] memory)
  {
    uint256 numberOfAssets = _assetsAddresses.length;
    AssetStatic[] memory _assets = new AssetStatic[](numberOfAssets);
    for (uint256 assetIdx = 0; assetIdx < numberOfAssets; assetIdx++) {
      address assetAddress = _assetsAddresses[assetIdx];
      AssetStatic memory _asset = assetStatic(assetAddress);
      _assets[assetIdx] = _asset;
    }
    return _assets;
  }

  /**
   * Fetch dynamic information about an array of assets. This method can be used for off-chain pagination.
   */
  function assetsDynamic(address[] memory _assetsAddresses)
    public
    view
    returns (AssetDynamic[] memory)
  {
    uint256 numberOfAssets = _assetsAddresses.length;
    AssetDynamic[] memory _assets = new AssetDynamic[](numberOfAssets);
    for (uint256 assetIdx = 0; assetIdx < numberOfAssets; assetIdx++) {
      address assetAddress = _assetsAddresses[assetIdx];
      AssetDynamic memory _asset = assetDynamic(assetAddress);
      _assets[assetIdx] = _asset;
    }
    return _assets;
  }

  /**
   * Fetch static information for all assets
   */
  function assetsStatic() external view returns (AssetStatic[] memory) {
    address[] memory _assetsAddresses = assetsAddresses();
    return assetsStatic(_assetsAddresses);
  }

  /**
   * Fetch dynamic information for all assets
   */
  function assetsDynamic() external view returns (AssetDynamic[] memory) {
    address[] memory _assetsAddresses = assetsAddresses();
    return assetsDynamic(_assetsAddresses);
  }

  /**
   * Fetch underlying token allowances relative to an asset.
   * This is useful for determining whether or not a user has token approvals
   * to allow depositing into an asset
   */
  function tokenAllowances(address accountAddress, address assetAddress)
    public
    view
    returns (Allowance[] memory)
  {
    address tokenAddress = underlyingTokenAddress(assetAddress);
    address[] memory tokenAddresses = new address[](1);
    address[] memory assetAddresses = new address[](1);
    tokenAddresses[0] = tokenAddress;
    assetAddresses[0] = assetAddress;
    bytes memory allowances = abi.encode(
      helper.allowances(accountAddress, tokenAddresses, assetAddresses)
    );
    return abi.decode(allowances, (Allowance[]));
  }

  /**
   * Fetch asset allowances based on positionSpenderAddresses (configurable).
   * This is useful to determine if a particular zap contract is approved for the asset (zap out use case)
   */
  function assetAllowances(address accountAddress, address assetAddress)
    public
    view
    returns (Allowance[] memory)
  {
    address[] memory assetAddresses = new address[](1);
    assetAddresses[0] = assetAddress;
    bytes memory allowances = abi.encode(
      helper.allowances(
        accountAddress,
        assetAddresses,
        addressesGenerator.getPositionSpenderAddresses()
      )
    );
    return abi.decode(allowances, (Allowance[]));
  }

  /**
   * Fetch basic static token metadata
   */
  function tokenMetadata(address tokenAddress)
    internal
    view
    returns (Token memory)
  {
    IERC20 _token = IERC20(tokenAddress);
    return
      Token({
        id: tokenAddress,
        name: _token.name(),
        symbol: _token.symbol(),
        decimals: _token.decimals()
      });
  }

  /**
   * Internal method for constructing a TokenAmount struct given a token balance and address
   */
  function tokenAmount(uint256 amount, address tokenAddress)
    internal
    view
    returns (TokenAmount memory)
  {
    return
      TokenAmount({
        amount: amount,
        amountUsdc: oracle.getNormalizedValueUsdc(tokenAddress, amount)
      });
  }

  /**
   * Fetch the total number of assets for this adapter
   */
  function assetsLength() public view returns (uint256) {
    return addressesGenerator.assetsLength();
  }

  /**
   * Fetch all asset addresses for this adapter
   */
  function assetsAddresses() public view returns (address[] memory) {
    return addressesGenerator.assetsAddresses();
  }

  /**
   * Fetch registry address from addresses generator
   */
  function registry() public view returns (address) {
    return addressesGenerator.registry();
  }

  /**
   * Configure adapter
   */
  constructor(
    address _oracleAddress,
    address _helperAddress,
    address _addressesGeneratorAddress,
    address _fallbackContractAddress
  ) {
    require(_oracleAddress != address(0), "Missing oracle address");
    oracle = IOracle(_oracleAddress);
    helper = IHelper(_helperAddress);
    fallbackContractAddress = _fallbackContractAddress;
    addressesGenerator = IAddressesGenerator(_addressesGeneratorAddress);
  }

  /*******************************************************
   * Common code shared by v1 vaults, v2 vaults and earn *
   *******************************************************/

  /**
   * Fetch asset positions of an account given an array of assets. This method can be used for off-chain pagination.
   */
  function assetsPositionsOf(
    address accountAddress,
    address[] memory _assetsAddresses
  ) public view returns (Position[] memory) {
    uint256 numberOfAssets = _assetsAddresses.length;
    Position[] memory positions = new Position[](numberOfAssets);
    for (uint256 assetIdx = 0; assetIdx < numberOfAssets; assetIdx++) {
      address assetAddress = _assetsAddresses[assetIdx];
      Position memory position = assetPositionsOf(accountAddress, assetAddress)[
        0
      ];
      positions[assetIdx] = position;
    }
    return positions;
  }

  /**
   * Fetch asset positions for an account for all assets
   */
  function assetsPositionsOf(address accountAddress)
    external
    view
    returns (Position[] memory)
  {
    address[] memory _assetsAddresses = assetsAddresses();
    return assetsPositionsOf(accountAddress, _assetsAddresses);
  }

  /*******************************************************
   *                 V1 Adapter (unique logic)           *
   *******************************************************/
  /**
   * Return information about the adapter
   */
  function adapterInfo() public view returns (AdapterInfo memory) {
    return
      AdapterInfo({id: address(this), typeId: "VAULT_V1", categoryId: "VAULT"});
  }

  /**
   * Metadata specific to this asset type
   */
  struct AssetMetadata {
    string symbol;
    uint256 pricePerShare;
    bool migrationAvailable;
    address latestVaultAddress;
    uint256 totalSupply;
  }

  /**
   * Fetch the underlying token address of an asset
   */
  function underlyingTokenAddress(address assetAddress)
    public
    view
    returns (address)
  {
    IV1Vault vault = IV1Vault(assetAddress);
    address tokenAddress = vault.token();
    return tokenAddress;
  }

  /**
   * Fetch static information about an asset
   */
  function assetStatic(address assetAddress)
    public
    view
    returns (AssetStatic memory)
  {
    IV1Vault vault = IV1Vault(assetAddress);
    address tokenAddress = underlyingTokenAddress(assetAddress);
    return
      AssetStatic({
        id: assetAddress,
        typeId: adapterInfo().typeId,
        name: vault.name(),
        version: "1.0.0",
        token: tokenMetadata(tokenAddress)
      });
  }

  /**
   * Fetch dynamic information about an asset
   */
  function assetDynamic(address assetAddress)
    public
    view
    returns (AssetDynamic memory)
  {
    IV1Vault vault = IV1Vault(assetAddress);
    address tokenAddress = underlyingTokenAddress(assetAddress);

    string memory name = vault.name();
    uint256 totalAssets = vault.balance();
    uint256 totalSupply = vault.totalSupply();

    uint256 pricePerShare = 0;
    bool vaultHasShares = totalSupply != 0;
    if (vaultHasShares) {
      pricePerShare = vault.getPricePerFullShare();
    }

    // address latestVaultAddress = registry.latestVault(tokenAddress);
    // bool migrationAvailable = latestVaultAddress != assetAddress;

    AssetMetadata memory metadata = AssetMetadata({
      symbol: vault.symbol(),
      pricePerShare: pricePerShare,
      migrationAvailable: false,
      latestVaultAddress: address(0),
      totalSupply: totalSupply
    });

    uint256 balance = assetBalance(assetAddress);
    TokenAmount memory underlyingTokenBalance = tokenAmount(
      balance,
      tokenAddress
    );

    return
      AssetDynamic({
        id: assetAddress,
        typeId: adapterInfo().typeId,
        tokenId: tokenAddress,
        underlyingTokenBalance: underlyingTokenBalance,
        metadata: metadata
      });
  }

  function assetPositionsOf(address accountAddress, address assetAddress)
    public
    view
    returns (Position[] memory)
  {
    IV1Vault _asset = IV1Vault(assetAddress);
    address tokenAddress = underlyingTokenAddress(assetAddress);
    IERC20 token = IERC20(tokenAddress);

    uint256 balance = _asset.balanceOf(accountAddress);
    uint256 _accountTokenBalance = token.balanceOf(accountAddress);
    uint256 _underlyingTokenBalance = (balance *
      _asset.getPricePerFullShare()) / 10**18;

    Position memory position = Position({
      assetId: assetAddress,
      tokenId: tokenAddress,
      typeId: "DEPOSIT",
      balance: balance,
      underlyingTokenBalance: tokenAmount(
        _underlyingTokenBalance,
        tokenAddress
      ),
      accountTokenBalance: tokenAmount(_accountTokenBalance, tokenAddress),
      tokenAllowances: tokenAllowances(accountAddress, assetAddress),
      assetAllowances: assetAllowances(accountAddress, assetAddress)
    });
    Position[] memory positions = new Position[](1);
    positions[0] = position;
    return positions;
  }

  /**
   * Fetch asset balance in underlying tokens
   */
  function assetBalance(address assetAddress) public view returns (uint256) {
    IV1Vault vault = IV1Vault(assetAddress);
    return vault.balance();
  }

  /**
   * Fallback proxy. Primary use case is to give registry adapters access to TVL adapter logic
   */
  fallback() external {
    assembly {
      let addr := sload(fallbackContractAddress.slot)
      calldatacopy(0, 0, calldatasize())
      let success := staticcall(gas(), addr, 0, calldatasize(), 0, 0)
      returndatacopy(0, 0, returndatasize())
      if success {
        return(0, returndatasize())
      }
    }
  }
}
