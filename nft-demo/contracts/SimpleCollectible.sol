//SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    // This is a factory contract
    // The main contract has a list of all types of NFTs and Owners
    uint256 public tokenCounter;
    
    constructor() public ERC721 ("Doggie", "DOG"){
        tokenCounter = 0;
    }

    function createCollectible(string memory tokenURI) public returns (uint256){
        // creating a new NFT is just mapping a tokenID to an address
        // we use openzeppelin safeMint to create a new NFT - this checks to see if a token ID has already been used or not so we dont override who owns tokens/IDs
        // since we inherited this contract from openzeppelin ERC721 (NFT) contract we can use this function
        uint256 newTokenId = tokenCounter; // iterate this every time we make a new token
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter +1;
        return newTokenId;
    }
}