// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; // safemath included by default?

import '@openzeppelin/contracts/access/Ownable.sol';
import '@openzeppelin/contracts/token/ERC20/IERC20.sol';
import '@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol';

contract TokenFarm is Ownable {

    address[] public allowedTokens;
    // mapping of token to staker to amount - how mcuh of each token each staker has staked
    // map the token (address) to a mapping of user (address) to a number [of tokens]
    mapping(address => mapping(address => uint256)) public stakingBalance;
    // how many DIFFERENT tokens each address has staked
    mapping(address => uint256) public uniqueTokensStaked;
    // a lis of all the stakers so we can loop through it
    address[] public stakers;
    // the dapp token [interface]
    IERC20 public dappToken;
    // mapping of each token to its price feed address
    mapping(address => address) public tokenPriceFeedMapping;
    
    // 100 ETH 1:1 for every 1 ETH, we give 1 DappToken
    // 50 ETH and 50 DAI stakes, we want to give a reward of 1 DappToken per DAI
    // wd have to convert all of our ETH into DAI

    // we need to know the address of our reward token (DappToken)
    constructor(address _dappTokenAddress) public {
        dappToken = IERC20(_dappTokenAddress); // now we can call functions on our dapptoken ie transfer etc
    }

    function setPriceFeedContract(address _token, address _priceFeed) public onlyOwner {
        tokenPriceFeedMapping[_token] = _priceFeed;
    }


    function issueTokens() public onlyOwner {
        // issue tokens to all 
        for (uint256 stakersIndex = 0; stakersIndex < stakers.length; stakersIndex++){
            address recipient = stakers[stakersIndex];
            // send them a token reward based on their total value locked
            uint256 userTotalValue = getUserTotalValue(recipient);

            // transfer the user an amount of tokens as reward based on their total value locked
            // in this case, howevber much value they have staked on our platform, we will issue equal value in our token as a reward
            dappToken.transfer(recipient, userTotalValue);
        }
    }

    function getUserTotalValue(address _user) public view returns(uint256) {
        // a lot of protocols just have people claiming tokens as it is a lot more gas efficient!
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_user] > 0, "No tokens staked!");

        // loop over all the allowed tokens and if a user has any get the total value of them and add it to totalValue
        for (uint256 i = 0; i < allowedTokens.length; i++){
            totalValue = totalValue + getUserSingleTokenValue(_user, allowedTokens[i]);
        }
        return totalValue;
    }

    function getUserSingleTokenValue(address _user, address _token) public view returns(uint256){
        // if staked 1ETH at a price of 2kUSD we return 2000...etc
        // get the value of all the tokens of type that the user has staked i.e. 1ETH at 2000USD returns 2000, 10 DAI at 10USD returns 100
        if(uniqueTokensStaked[_user] <= 0){
            return 0; // dont watn the tx to revert if this is 0
        }

        // price of the token * stakingBalance[_token][_user]
        (uint256 price, uint256 decimals) = getTokenValue(_token);

        // take the amount of tokens the user has stacked...lets say 10 ETH
        // take the price of ETH - in USD - therefore price feed contract is ETH/USD
        // if ETH --> USD is $100;
        // 10 ETH with its full decimansl is 10000000000000000000 (18 decimals I think)
        // 10 ETH times $100 = $1000...but we also have to divide by the decimals otherwise we get a fuckhuge number
        return (stakingBalance[_token][_user] * price / (10**decimals));
    }

    function getTokenValue(address _token) public view returns (uint256, uint256){
        // price feed address
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddress);
        (, int256 price,,,) = priceFeed.latestRoundData();
        // how many decimals the pricefeed has
        uint256 decimals = priceFeed.decimals();
        return (uint256(price), decimals); // since decimals actually gives us a int/uint8 we wrap it into a uint256
    }

    function stakeTokens(uint256 _amount, address _token) public {
        // what tokens can they stake
        // how much can they stake
        require(_amount > 0, "Amount must be more than 0");
        require(tokenIsAllowed(_token), "Token is currently not allowed");
        // call the transferFrom function of the ERC20
        // transfer works if its being called from the wallet that owns the tokens
        // transferFrom works to transfer them from another wallet ie from a user to this contract

        // so we use the ERC20 interface to use the transferFrom function of the ERC20
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);

        // get an idea of how many unique tokens the user has - if they have more than one they've already been added to the stakers list
        updateUniqueTokensStaked(msg.sender, _token);
        // update the user's balance
        stakingBalance[_token][msg.sender] = stakingBalance[_token][msg.sender] + _amount;
        // now we know if we need to put them on the stakers list
        if (uniqueTokensStaked[msg.sender] == 1) {
            // if this is their first unique token
            stakers.push(msg.sender);
        }
    }

    function unstakeTokens(address _token) public {
        // get the staked balance of the user
        uint256 balance = stakingBalance[_token][msg.sender];
        require(balance > 0, "Staking balance cannot be 0");
        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] == 0;
        // RE-ENTRANCY ATTACK VULN??
        uniqueTokensStaked[msg.sender] == uniqueTokensStaked[msg.sender] - 1;
        // remove this person from the stakers array if they have nothing stakced?
    }

    function updateUniqueTokensStaked(address _user, address _token) internal {
        // internal - only this contract can call this
        if (stakingBalance[_token][_user] <= 0) {
            uniqueTokensStaked[_user] = uniqueTokensStaked[_user] + 1;
        }
    }

    function addAllowedTokens(address _token) public {
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        for(uint256 allowedTokensIndex=0; allowedTokensIndex < allowedTokens.length; allowedTokensIndex++) {
            if(allowedTokens[allowedTokensIndex] == _token) {
                return true;
            }
        }
        return false;
    }


}