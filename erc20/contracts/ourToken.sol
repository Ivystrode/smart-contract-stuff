// contracts/ourToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ourToken is ERC20 {
    // wei
    constructor(uint256 initialSupply) ERC20("BryToken", "BTK") {
        _mint(msg.sender, initialSupply);
    }
}