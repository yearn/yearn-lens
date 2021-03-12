pragma solidity ^0.8.2;

interface V1Registry {
    function getVaults() external view returns (address[] memory);

    function getVaultsLength() external view returns (uint256);

    // function getVaultsInfo()
    //     external
    //     view
    //     returns (
    //         address[] memory,
    //         address[] memory,
    //         address[] memory,
    //         address[] memory,
    //         address[] memory
    //     );
}
