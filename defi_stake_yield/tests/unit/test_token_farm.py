from brownie import network, exceptions
from scripts.helpful_scripts import INITIAL_PRICE_FEED_VALUE, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.deploy import deploy_token_farm_and_dapp_token
import pytest


def test_set_price_feed_contract():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Local testing only")
    account = get_account()
    non_owner = get_account(index=1)
    
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    
    price_feed_address = get_contract("eth_usd_price_feed")
    
    token_farm.setPriceFeedContract(dapp_token.address, price_feed_address, {"from":account})

    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address
    
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(dapp_token.address, price_feed_address, {"from":non_owner})
        
def test_stake_tokens(amount_staked):
    """
    Pytest/brownie will wrap the amount_staked from conftest fixtures to this function parameter
    """
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Local testing only")
    account = get_account()
    non_owner = get_account(index=1)
    
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    
    dapp_token.approve(token_farm.address, amount_staked, {"from":account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from":account})

    assert token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    return token_farm, dapp_token # now we can use this test in some of our other tests (see below)...a little bit integration-y
    
        
def test_issue_tokens(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Local testing only")
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)
    
    print("=====================")
    print(starting_balance)
    print(dapp_token.balanceOf(account.address))
    print(INITIAL_PRICE_FEED_VALUE)
    print("=====================")
    token_farm.issueTokens({"from":account})
    print(dapp_token.balanceOf(account.address))
    # we are staking 1 ETH WORTH OF DAPP TOKENS
    # so we should get 2000 dapp tokens since the price of eth is 2000usd (in our mock contract)    
    assert dapp_token.balanceOf(account.address) == starting_balance + INITIAL_PRICE_FEED_VALUE
    
    