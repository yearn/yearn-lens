pragma solidity ^0.8.2;

interface V2Registry {
    function getVaults() external view returns (address[] memory);

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
