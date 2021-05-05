// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

/*******************************************************
 *                     Ownable
 *******************************************************/
contract Ownable {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Ownable: caller is not the owner");
        _;
    }
}
