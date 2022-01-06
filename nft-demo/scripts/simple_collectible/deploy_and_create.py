from brownie import network, SimpleCollectible
from scripts.helpful_scripts import get_account, OPENSEA_URL

sample_token_uri = 'https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json'


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from":account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from":account})
    tx.wait(1)
    print(f"We should now be able to see this at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}")
    return simple_collectible

def main():
    deploy_and_create()