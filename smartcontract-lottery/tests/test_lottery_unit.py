import pytest

from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3

from scripts import helpful_scripts, deploy_lottery

# unit test is a way of testing the smallest pieces of code in an isolated system - local
# integration test is testing across multiple complex pieces - testnet
# often people create separate dirs for this but for now we'll do all in here

def test_get_entrance_fee():
    # since this is a unit test we only really want to run this when working on a local blockchain environment/local dev network
    if network.show_active() not in helpful_scripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    # arrange
    lottery = deploy_lottery.deploy_lottery()
    
    # act
    # if eth is 2000usd and entry fee is 50usd if 2000/1 == 50/x == 0.025
    # why cant i do this with the ACTUAL eth price? because its a local chain and it cant actually look it up and we hard coded it with that price?
    # i think it is because it comes from the "fee" in the config file
    expected_entrance_fee = Web3.toWei(50/2000, "ether")
    print(f"Entrance fee should be: {expected_entrance_fee}")
    entrance_fee = lottery.getEntranceFee()
    print(entrance_fee)
    print(expected_entrance_fee)
    
    # assert
    assert expected_entrance_fee == entrance_fee
    
def test_cant_enter_unless_started():
    # since this is a unit test we only really want to run this when working on a local blockchain environment/local dev network
    
    # arrange
    if network.show_active() not in helpful_scripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
        
    lottery = deploy_lottery.deploy_lottery()
    
    # act/assert
    with pytest.raises(exceptions.VirtualMachineError): # guessing virtual machine error is an error with ganache (it runs like a virtual machine...?)
        lottery.enter({"from":helpful_scripts.get_account(), "value": lottery.getEntranceFee()})
    
def test_can_start_and_enter_lottery():
    # since this is a unit test we only really want to run this when working on a local blockchain environment/local dev network
    
    # arrange
    if network.show_active() not in helpful_scripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    lottery = deploy_lottery.deploy_lottery()
    account = helpful_scripts.get_account()
    lottery.startLottery({"from":account})
    
    # act
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})
    
    # assert
    assert lottery.players(0) == account # we have our players array and we assert that we are pushing them onto our array correctly
    
def test_can_end_lottery():
    # since this is a unit test we only really want to run this when working on a local blockchain environment/local dev network
    
    # arrange
    if network.show_active() not in helpful_scripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
        
    lottery = deploy_lottery.deploy_lottery()
    account = helpful_scripts.get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})
    
    # act
    # need to fund with link to do the randomness
    helpful_scripts.fund_with_link(lottery)
    lottery.endLottery({"from":account})
    # when we call end lottery we're only changing our state - so we check our calculating winner state
    assert lottery.lottery_state() == 2 # calculating_winner is index 2 of that enum
    
def test_can_pick_winner_correctly():
    """Most important test of all"""
    # since this is a unit test we only really want to run this when working on a local blockchain environment/local dev network
    # this is close to being an integration tets but meh
    
    # arrange
    if network.show_active() not in helpful_scripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    print("bla1")
        
    lottery = deploy_lottery.deploy_lottery()
    account = helpful_scripts.get_account()
    account2 = helpful_scripts.get_account(index=1)
    account3 = helpful_scripts.get_account(index=2)
    lottery.startLottery({"from":account})
    print("bla2")
    # use a couple of accounts to test (obvciously because it needs to pick!)
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})
    lottery.enter({"from":account2, "value":lottery.getEntranceFee()})
    lottery.enter({"from":account3, "value":lottery.getEntranceFee()})
    print("bla3")
    helpful_scripts.fund_with_link(lottery)
    print("bla4")
    # act
    # need to fund with link to do the randomness
    # in order to test this we need to cal fulfillRandomness function...which gets called by the VRFCoordinator when it returns the radomn number
    # we also have to pass the original request id
    # we want to emit an event to track when the contract goes into the calculating_winner state
    # events are kind of like the print statements of the blockchain
    # etherscan logs show all the events - you would see randonnessRequest in the logs, in which you'd see a requestId
    # so we need to emit an event in the endLottery function of the contract
    
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    
    transaction = lottery.endLottery({"from":account})
    request_id = transaction.events['RequestedRandomness']['requestId']
    STATIC_RNG = 777 # any random number
    print("bla5")
    # dummy getting a response from a chainlink node with the random number STATIC_RNG
    helpful_scripts.get_contract("vrf_coordinator").callBackWithRandomness(request_id, STATIC_RNG, lottery.address, {"from":account}) # this is making a state change
    
    print("bla6")
    
    # 777 % 3 = 259
    # we know this means the answer is 0 then
    
    # check account[0] is the winner
    assert lottery.recentWinner() == account
    # check lottery has sent out all funds
    assert lottery.balance() == 0
    # check account[0] has been awarded the money
    assert account.balance() == starting_balance_of_account + balance_of_lottery