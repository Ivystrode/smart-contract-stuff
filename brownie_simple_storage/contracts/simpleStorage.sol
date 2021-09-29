// SPDX-Licence-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 public favnumber;
    
    struct People {
        uint256 favnumber;
        string name;
    }
    
    People[] public people;
    
    mapping(string => uint256) public nameTofavnumber;
    
    function store(uint256 _favnumber) public {
        favnumber = _favnumber;
    }
    
    // view, pure
    // view means we want to read something off the blockchain - not make state change/transaction
    // pure functions just do some type of maths, and still not change state of blockchain
    function retrieve() public view returns(uint256) {
        return favnumber;
    }
    
    function addPerson(string memory _name, uint256 _favnumber) public {
        people.push(People(_favnumber, _name));
        nameTofavnumber[_name] = _favnumber;
    }
}