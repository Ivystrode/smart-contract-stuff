from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from brownie import network
import pytest, time

def test_can_create_advanced_collectible_integration():
    account = get_account()
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("only for integration testing ie on a real chain")
        pytest.skip()
    advanced_collectible, creation_tx = deploy_and_create()
    
    # don't need the randomness request id any more since the chainlink node is responding
    # so the breed will definitely be random - we don't have to make sure we did deploy the mock randomness contract
    time.sleep(60)
    
    assert advanced_collectible.tokenCounter() == 1