// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BoxV2 {
    uint256 private value;
    
    event valueChanged(uint256 newValue);

    function store(uint256 newValue) public {
        value = newValue;
        emit valueChanged(newValue);
    }

    function retrieve() public view returns(uint256) {
        return value;
    }

    function increment() public {
        // if we can call this function then the contract has been upgraded as it doesn't exist in the older one
        value = value + 1;
        emit valueChanged(value);
    }

}
