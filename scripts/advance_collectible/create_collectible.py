from brownie import AdvancedCollectible, accounts, config, network
from scripts.helpful_scripts import get_breed
import time

STATIC_SEED = 1123

def main():
    dev_account = accounts.add(config['wallets']['from_key'])
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    transanction = advanced_collectible.createCollectible(
        STATIC_SEED, "None", {'from': dev_account})
    transanction.wait(1)

    requestId = transanction.events['requestedCollectible']['requestId']
    token_id = advanced_collectible.requestIdToTokenId(requestId)

    time.sleep(55)

    breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))

    print("Dog Breed of TokenId {} is {}".format(token_id, breed))
    print(f"Dog Breed of TokenId {token_id} is {breed}")
