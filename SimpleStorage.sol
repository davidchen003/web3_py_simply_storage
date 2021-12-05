// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 favoriteNumber = 0;
    // initialized the value to 0
    // otherwise print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}") will cause error when deploying it to Rinkeby (OK with Ganache though): eth_abi.exceptions.InsufficientDataBytes: Tried to read 32 bytes.  Only got 0 bytes

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
