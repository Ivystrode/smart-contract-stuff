//SPDX-Licence-Identifier: MIT 

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol"; // this imports the/an npm package
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol"; // this imports a safe maths set of functions to stop ints/uints from going around back to 0 when they reach their max

contract FundMe {
    using SafeMathChainlink for uint256; // uses safemath to make sure we don't overflow/go round to 0 again with uint256's
    
    mapping(address => uint256) public addressToAmountFunded; // for each person who donates, link their address to a total amount integer
    address[] public funders;
    address public owner; // variable for the owner's address
    AggregatorV3Interface public priceFeed;
    
    // constructor func - gets called when the contract is deployed
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender; // whoever deploys the smart contract
    }
    
    function fund() public payable {
        uint minimumUSD = 50 * 10 ** 18; // make it have 18 decimals
        require(getConversionRate(msg.value) >= minimumUSD, "You need to send at least 50 dollars"); // if less than 50USD then revert
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender); // add the sender to the funders list/array
    }
    
    function getVersion() public view returns (uint256) {
        // there is a contract at this address that will return the priceFeed
        // but we dont need it if we do it in the constructor function
        // AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331); 

        return priceFeed.version(); // we make a function call to another contract and get the result
    }
    
    function getPrice() public view returns (uint256) {
        (
            ,
            int256 answer,
            ,
            ,// to get rid of unwanted return variables just put in the commas with nothing between them except for the var you want
            
            ) = priceFeed.latestRoundData();
            return uint256(answer * 10000000000); // remove the decimal places
    }
    
    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns(uint256){
        // minimum usd required
        uint256 minimumUSD = 50* 10**18;
        uint256 price = getPrice();
        uint256 precision = 1* 10**18;
        return (minimumUSD*precision) / price;
    }
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _; // this is where it runs the rest of the code (wherever the modifier is used)
    }
    
    function withdraw() payable onlyOwner public { // make sure the person/ account withdrawing is the owner using the onlyOwner modifier!
        msg.sender.transfer(address(this).balance); // address of "this" - the contract you are currently in - so whoever calls the withdraw func, transfer them all our money
        for (uint256 funderIndex=0; funderIndex<funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0; // this updates the mmapping for that donor
        }
        funders = new address[](0); // re-create the funders list (of addresses), blank
    }
}

// currently 3hrs into vid