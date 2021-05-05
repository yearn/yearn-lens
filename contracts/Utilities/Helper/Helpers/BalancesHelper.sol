pragma solidity ^0.8.2;

interface IPairsHelper {
    function pairsAddresses(
        address factoryAddress,
        uint256 pageSize,
        uint256 pageNbr,
        uint256 offset
    ) external view returns (address[] memory);

    function pairsAddresses(
        address factoryAddress,
        uint256 pageSize,
        uint256 pageNbr
    ) external view returns (address[] memory);

    function pairsAddresses(address factoryAddress)
        external
        view
        returns (address[] memory);

    function tokensAddresses(
        address factoryAddress,
        uint256 pageSize,
        uint256 pageNbr,
        uint256 offset
    ) external view returns (address[] memory);

    function tokensAddresses(
        address factoryAddress,
        uint256 pageSize,
        uint256 pageNbr
    ) external view returns (address[] memory);

    function tokensAddresses(address factoryAddress)
        external
        view
        returns (address[] memory);

    function pagesLength(address factoryAddress, uint256 pageSize)
        external
        view
        returns (uint256);

    function pagesLength(
        address factoryAddress,
        uint256 pageSize,
        uint256 offset
    ) external view returns (uint256);
}

interface IERC20 {
    function decimals() external view returns (uint8);

    function symbol() external view returns (string memory);

    function name() external view returns (string memory);

    function balanceOf(address account) external view returns (uint256);

    function allowance(address spender, address owner)
        external
        view
        returns (uint256);
}

interface IOracle {
    function getNormalizedValueUsdc(
        address tokenAddress,
        uint256 amount,
        uint256 price
    ) external view returns (uint256);

    function getPriceUsdcRecommended(address tokenAddress)
        external
        view
        returns (uint256);
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

contract BalancesHelper {
    address public owner; // Owner can update storage slots
    address public oracleAddress; // Oracle address
    address public pairsHelperAddress; // Pair utility address
    IOracle oracle;
    IPairsHelper pairsHelper;

    struct TokenBalance {
        address tokenId;
        uint256 priceUsdc;
        uint256 balance;
        uint256 balanceUsdc;
    }

    struct TokenPrice {
        address tokenId;
        uint256 priceUsdc;
    }

    constructor(address _oracleAddress, address _pairsHelperAddress) {
        owner = msg.sender;
        oracleAddress = _oracleAddress;
        pairsHelperAddress = _pairsHelperAddress;
        oracle = IOracle(_oracleAddress);
        pairsHelper = IPairsHelper(_pairsHelperAddress);
    }

    /**
     * Fetch token prices given a factory address and pagination settings
     */
    function tokensPrices(
        address factoryAddress,
        uint256 pageSize,
        uint256 pageNbr
    ) public view returns (TokenPrice[] memory) {
        address[] memory tokensAddresses =
            pairsHelper.tokensAddresses(factoryAddress, pageSize, pageNbr);
        return tokensPrices(tokensAddresses);
    }

    /**
     * Fetch LP prices given a factory address and pagination settings
     */
    function pairsPrices(
        address factoryAddress,
        uint256 pageSize,
        uint256 pageNbr
    ) public view returns (TokenPrice[] memory) {
        address[] memory pairsAddresses =
            pairsHelper.pairsAddresses(factoryAddress, pageSize, pageNbr);
        return tokensPrices(pairsAddresses);
    }

    /**
     * Fetch token balances given an array of token addresses and account address
     */
    function tokensBalances(
        address accountAddress,
        address[] memory tokensAddresses
    ) public view returns (TokenBalance[] memory) {
        TokenBalance[] memory _tokensBalances =
            new TokenBalance[](tokensAddresses.length);
        uint256 currentIdx;
        // return tokensAddresses;
        for (
            uint256 tokenIdx = 0;
            tokenIdx < tokensAddresses.length;
            tokenIdx++
        ) {
            address tokenAddress = tokensAddresses[tokenIdx];
            IERC20 token = IERC20(tokenAddress);
            uint256 balance =
                token.balanceOf(0x253c5cBDd08838DaD5493D511E17Aa1ac5eAB51B);
            if (balance == 0) {
                continue;
            }
            uint256 priceUsdc = oracle.getPriceUsdcRecommended(tokenAddress);
            uint256 balanceUsdc =
                oracle.getNormalizedValueUsdc(tokenAddress, balance, priceUsdc);

            _tokensBalances[currentIdx] = TokenBalance({
                tokenId: tokenAddress,
                priceUsdc: 0,
                balance: balance,
                balanceUsdc: 0
            });
            currentIdx++;
        }
        bytes memory encodedBalances = abi.encode(_tokensBalances);
        assembly {
            mstore(add(encodedBalances, 0x40), currentIdx)
        }
        _tokensBalances = abi.decode(encodedBalances, (TokenBalance[]));

        return _tokensBalances;
    }

    function tokensBalances(
        address accountAddress,
        address factoryAddress,
        uint256 pageSize,
        uint256 pageNbr
    ) public view returns (address[] memory) {
        address[] memory tokensAddresses =
            pairsHelper.tokensAddresses(factoryAddress, pageSize, pageNbr);
        return tokensAddresses;
        // TokenBalance[] memory _tokensBalances =
        //     tokensBalances(accountAddress, tokensAddresses);
        // return _tokensBalances;
    }

    /**
     * Fetch token prices given an array of token addresses
     */
    function tokensPrices(address[] memory tokensAddresses)
        public
        view
        returns (TokenPrice[] memory)
    {
        TokenPrice[] memory _tokensPrices =
            new TokenPrice[](tokensAddresses.length);
        for (
            uint256 tokenIdx = 0;
            tokenIdx < tokensAddresses.length;
            tokenIdx++
        ) {
            address tokenAddress = tokensAddresses[tokenIdx];
            _tokensPrices[tokenIdx] = TokenPrice({
                tokenId: tokenAddress,
                priceUsdc: oracle.getPriceUsdcRecommended(tokenAddress)
            });
        }
        return _tokensPrices;
    }

    /**
     * Fetch basic static token metadata
     */
    function tokenMetadata(address tokenAddress)
        public
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

    function updateSlot(bytes32 slot, bytes32 value) external {
        require(msg.sender == owner);
        assembly {
            sstore(slot, value)
        }
    }
}
