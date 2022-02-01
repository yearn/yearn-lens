// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

contract Introspection {
    function implementsMethod(address _address, string memory _signature)
        public
        view
        returns (bool)
    {
        bytes4 _selector = bytes4(keccak256(bytes(_signature)));
        uint256 contractSize;
        assembly {
            contractSize := extcodesize(_address)
        }
        bytes memory code = new bytes(contractSize);
        assembly {
            extcodecopy(_address, add(code, 0x20), 0, contractSize)
        }
        uint256 ptr = 0;
        while (ptr < contractSize) {
            // PUSH4 0x000000 (selector)
            if (code[ptr] == 0x63) {
                bytes memory selectorBytes = new bytes(64);
                selectorBytes[0] = code[ptr + 1];
                selectorBytes[1] = code[ptr + 2];
                selectorBytes[2] = code[ptr + 3];
                selectorBytes[3] = code[ptr + 4];
                bytes4 selector = abi.decode(selectorBytes, (bytes4));
                if (selector == _selector) {
                    return true;
                }
            }
            ptr++;
        }
        return false;
    }

    function implementsInterface(address _address, string[] memory _interface)
        external
        view
        returns (bool)
    {
        for (
            uint256 methodIdx = 0;
            methodIdx < _interface.length;
            methodIdx++
        ) {
            string memory method = _interface[methodIdx];
            bool methodIsImplemented = implementsMethod(_address, method);
            if (!methodIsImplemented) {
                return false;
            }
        }
        return true;
    }
}
