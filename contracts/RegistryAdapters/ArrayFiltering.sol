// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

contract FilterArray {
    function removeZerosFromArray() external view returns (uint256[] memory) {
        uint256[] memory uintArray = new uint256[](5);
        uintArray[0] = 1;
        uintArray[1] = 0;
        uintArray[2] = 3;
        uintArray[3] = 0;
        uintArray[4] = 44;

        uint256 currentIdx;
        for (
            uint256 uintArrayIdx = 0;
            uintArrayIdx < uintArray.length;
            uintArrayIdx++
        ) {
            uint256 value = uintArray[uintArrayIdx];
            if (value > 0) {
                uintArray[currentIdx] = value;
                currentIdx++;
            }
        }

        bytes memory encodedData = abi.encode(uintArray);
        assembly {
            // Manually truncate array
            mstore(add(encodedData, 0x40), currentIdx)
        }
        uint256[] memory filteredArray = abi.decode(encodedData, (uint256[]));
        require(filteredArray.length == 3);
        return filteredArray;
    }
}
