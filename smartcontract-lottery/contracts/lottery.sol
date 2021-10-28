// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol"; 
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players; // "players" is a public list/array of addresses - listing the people who have entered the lottery
    address payable public recentWinner;
    uint256 public randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed; // variable ethUsdPriceFeed is an AggregatorV3Interface
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee; // associated with the link token needed to pay for requests (for random number gen)
    bytes32 public keyhash; // keyhash - uniquely identifies a chainlink vrf node

    // we include the constructor of VRFConsumerBase in this constructor - pass the params to it from the main constructor params
    constructor(address _priceFeedAddress, address _vrfCoordinator, address _link, uint256 _fee, bytes32 _keyhash) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18); // 50 dollars - given 18 decimals
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
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

    function endLottery() public onlyOwner {
        // get a random winner - must be a safe random number generator, not exploitable
        // we can use a globally available variable and hash it to do this on a blockchain (since on a blockchain all nodes must agree on the number...)
        // see below - we will have to go outside the blockchain to get a truly random number
        // so we use chainlink VRF (Verifiable Randomness I think - https://docs.chain.link/docs/get-a-random-number/ - go to contracts section of VRF to select desired chain?)
        // see points 8-10 in readme
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        requestRandomness(keyhash, fee); // returns a bytes32 called requestId (see in VRFConsumerBase) - the name of this variable is dictated as a bytes32 called requestId
        // the first transaction is this function that gives us the ID of our request. The oracle then calls a callback function that we need to define here
        // that gives us our random number - it has to be called fulfillRandomness as that is what it calls in the oracle
    }

    // internal somehow means only the VRF coordinator can call this function (since this contract called it...?)
    // override - overrides the original declaration of the fulfillRandomness function in the oracle (it is just a virtual function so we have to)
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "You aren't there yet");
        require(_randomness > 0, "random-not-found");
        // use modulus with length of players array
        uint256 indexOfWinner = _randomness % players.length;
        // if 7 players sign up and rand is 22 - we do 22 % 7 - 7 divides into 22 3 times with 1 left over - diff is 1 - therefore rand number is 1 - player 1 wins
        recentWinner = players[indexOfWinner];
        // pay the winner all the money that was paid in
        recentWinner.transfer(address(this).balance);
        // reset the lottery
        players = new address payable[](0); // players is now an empty list
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness; // to keep track of most recent random number
    }
}



// the problem with making random numbers on the blockchain

// uint(keccak256(                 // <-- hashing algorithm
//         abi.encodePacked(nonce, // take a bunch of numbers and hash them all together to make a fairly random number
//         msg.sender,             // but a hashing algo will always hash the same way, so it wont be totally random
//         block.difficulty, // difficulty can be manipulated by miners
//         block.timestamp   // timestamp and nonce are predictable as is msg.sender 
//         );                  // therefore this is not an acceptable way to get a random number as miners can predict it...
//     )
// ) % players.length;