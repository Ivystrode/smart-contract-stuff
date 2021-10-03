from brownie import Lottery, accounts, config, network
from web3 import Web3

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(config['networks'][network.show_active()]['eth_usd_price_feed'],{"from":account})

    assert lottery.getEntranceFee() > Web3.toWei(0.013, "ether") # instead of hard coding we should really use the live ethereum value of $50 because this will always change...
    assert lottery.getEntranceFee() < Web3.toWei(0.016, "ether") 