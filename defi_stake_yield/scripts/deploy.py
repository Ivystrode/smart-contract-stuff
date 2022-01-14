from brownie import accounts, network, DappToken, TokenFarm, config
from scripts.helpful_scripts import get_account, get_contract
from web3 import Web3
import yaml, json, shutil, os

KEPT_BALANCE = Web3.toWei(100, "ether")

def deploy_token_farm_and_dapp_token(front_end_update=False):
    account = get_account() 
    dapp_token = DappToken.deploy({"from":account})
    token_farm = TokenFarm.deploy(dapp_token.address, {"from":account}, publish_source=config['networks'][network.show_active()]['verify'])
    
    # we need to send the dapp tokens to the contract so it can send them as rewards
    tx = dapp_token.transfer(token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from":account})
    tx.wait(1)
    
    # need to add allowed tokens and price feeds
    # at first we will use the dapp token, WETH, and FAU_token (a faucet token, we will pretend it is DAI - we can just get it from a fake ERC20 token faucet so we can test with it)

    # we want to do a get_contract call so we can deploy them as mocks if we run a development chain
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    
    # list the allowed tokens with their price feed address as well
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"), # we're just gonna peg this to DAI...test it with another price feed later
        weth_token: get_contract("eth_usd_price_feed")
    }
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    if front_end_update:
        update_front_end()
    return token_farm, dapp_token
    
def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedTokens(token.address, {"from":account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(token.address, dict_of_allowed_tokens[token], {"from":account})
        set_tx.wait(1)
    return token_farm

def update_front_end():
    """
    We don't have set contracts yet as we're deploying in development and changing the contract addresses all the time
    So we need to send the brownie-config and build folder to the src folder as these will have access to all the contract addresses we need
    TS needs JSON not yaml
    """
    copy_folders_to_front_end("./build", "./front_end/src/chain-info")
    
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
    with open("./front_end/src/brownie-config.json", "w") as brownie_config_json:
        json.dump(config_dict, brownie_config_json)
    print("Front end updated")
    
def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    


def main():
    deploy_token_farm_and_dapp_token(front_end_update=True)