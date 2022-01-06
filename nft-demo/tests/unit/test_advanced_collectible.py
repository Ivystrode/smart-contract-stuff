from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from brownie import network
import pytest 

def test_can_create_advanced_collectible():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    advanced_collectible, creation_tx = deploy_and_create()
    
    # test the mock vrf coordinator was deployed
    requestId = creation_tx.events['requestedCollectible']['requestId']
    randomnumber = 777
    get_contract("vrf_coordinator").callBackWithRandomness(requestId, randomnumber, advanced_collectible.address, {"from":account})
    
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == randomnumber % 3 # test the breed of dog 0 is 1 of the 3