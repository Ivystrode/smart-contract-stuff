// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol"; 
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    address payable[] public players; // "players" is a public list/array of addresses - listing the people who have entered the lottery
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10**18); // 50 dollars - given 18 decimals
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    function enter() public payable {
        // $50 min
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "Not enough ETH - must be $50 equivalent");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns(uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData(); // this func returns a tuple of many datapoints - we only want price, which is at index 1/position 2
        uint256 adjustedPrice = uint256(price) * 10 ** 10; // gives it 18 decimals (from 8 - the price feed has 8 decimals)
        uint256 costToEnter = (usdEntryFee * 10 ** 18) / adjustedPrice; // this way USD entry fee has 18 decimals
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, "LOTTERY IS CLOSED");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public {

    }
}