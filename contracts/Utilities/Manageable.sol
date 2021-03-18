// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;
pragma experimental ABIEncoderV2;

contract Manageable {
    string public name;
    address public owner;
    uint256 public managersCount;
    mapping(uint256 => address) public managerAddressByIdx;
    mapping(address => uint256) public managerIdxByAddress;

    constructor(string memory _name) public {
        name = _name;
        owner = msg.sender;
        managersCount = 1;
        managerAddressByIdx[0] = owner;
        managerIdxByAddress[owner] = 1;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Manageable: caller is not the owner");
        _;
    }

    modifier onlyManagers() {
        bool isManager = managerIdxByAddress[msg.sender] > 0;
        require(isManager, "Manageable: caller is not a manager");
        _;
    }

    function managersList() external view returns (address[] memory) {
        address[] memory managersList = new address[](managersCount);
        for (uint256 i = 0; i < managersCount; i++) {
            address managerAddress = managerAddressByIdx[i + 1];
            managersList[i] = managerAddress;
        }
        return managersList;
    }

    function isManager(address managerAddress) public view returns (bool) {
        return managerIdxByAddress[managerAddress] > 0;
    }

    function addManager(address managerAddress) public onlyManagers {
        require(
            isManager(managerAddress) == false,
            "Manageable: user is already a manager"
        );
        managersCount += 1;
        managerAddressByIdx[managersCount] = managerAddress;
        managerIdxByAddress[managerAddress] = managersCount;
    }

    function removeManager(address managerAddress) public onlyManagers {
        require(
            isManager(managerAddress),
            "Manageable: non-managers cannot be removed"
        );
        require(managerAddress != owner, "Managable: owner cannot be removed");
        uint256 managerIdx = managerIdxByAddress[managerAddress];
        delete managerAddressByIdx[managerIdx];
        delete managerIdxByAddress[managerAddress];
        managersCount -= 1;
    }

    function resetManagers() public onlyOwner {
        for (uint256 i = 0; i < managersCount; i++) {
            address managerAddress = managerAddressByIdx[i + 2];
            removeManager(managerAddress);
        }
    }
}
