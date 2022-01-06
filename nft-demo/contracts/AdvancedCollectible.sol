// an NFT contract where the token URI can be one of three different dogs randomly selected

//SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester); // emitted when we request Id to sender
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(address _VRFCoordinator, 
                address _linkToken, 
                bytes32 _keyhash, 
                uint256 _fee) 
                public 
                VRFConsumerBase(_VRFCoordinator, _linkToken) 
                ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns(bytes32) {
        // the user who calls this must also be assigned the tokenID
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender; // so that we can send the creator's address to fulfilrandomness
        // since fulfilrandomness is called by the vrfcoordinator contract we need to tell it who the creator was to assign the NFT to them

        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        // override so only the VRF Coordinator can call this (?)
        Breed breed = Breed(randomNumber % 3); // since there are 3 breeds
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;

        emit breedAssigned(newTokenId, breed);

        // mint the NFT
        // the vrf coordinator is the msg.sender here so we need to do it like this:
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);

        // set the token URI
        // we only know the breed once the randomness is returned...so there isn't a tokenURI until it is actually created

//        _setTokenURI(newTokenId, tokenURI);

        tokenCounter = tokenCounter + 1; // DON'T FORGET!!
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // a URI for each dog
        // but only the owner of the token id can update the token uri
        // use an openzeppeling function
        // only the owner or approved address can work with the token uri
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: Caller is not owner or approved");
        _setTokenURI(tokenId, _tokenURI);
    }
    
}