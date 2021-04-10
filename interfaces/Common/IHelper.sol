// SPDX-License-Identifier: MIT

pragma solidity >=0.8.2;

interface IHelper {
    function mergeAddresses(address[][] memory addressesSets)
        external
        view
        returns (address[] memory);

    function assetStrategiesDelegatedBalance(address)
        external
        view
        returns (uint256);

    function assetsStrategiesDelegatedBalance() external view returns (uint256);

    function assetStrategiesLength(address) external view returns (uint256);

    function assetsStrategiesLength() external view returns (uint256);
}
