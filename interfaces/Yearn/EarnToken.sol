pragma solidity ^0.8.2;

interface EarnToken {
    function token() external view returns (address);

    function name() external view returns (string memory);

    function symbol() external view returns (string memory);

    function decimals() external view returns (uint8);

    function getPricePerFullShare() external view returns (uint256);

    function pool() external view returns (uint256);

    function totalSupply() external view returns (uint256);

    function calcPoolValueInToken() external view returns (uint256);

    function aaveToken() external view returns (address);
}
