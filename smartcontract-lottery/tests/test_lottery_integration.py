# Where we will test on a real live chain
from brownie import network
from scripts.helpful_scripts import get_account, fund_with_link, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy_lottery import  deploy_lottery

import pytest, time

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account(id="eth_metamask")
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value":lottery.getEntranceFee() + 1000})
    lottery.enter({"from":account, "value":lottery.getEntranceFee() + 1000})
    fund_with_link(lottery)
    lottery.endLottery({"from":account})

    # no need to pretend to be a chainlink node - we wait for it to respond as its really on this chain
    time.sleep(5)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0