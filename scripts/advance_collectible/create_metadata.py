from ctypes.wintypes import ULARGE_INTEGER
import os
import requests
from brownie import AdvancedCollectible, accounts, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_breed
from pathlib import Path

def main():
    active_network = network.show_active()
    print(f"Working on {active_network}")
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print(f"Number tokens: {number_of_tokens}")

    write_data(number_of_tokens, advanced_collectible)


def write_data(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        breed = get_breed(nft_contract.tokenIdToBreed(token_id))

        # ./metadata/rinkeby/0-SHINA_INU.json
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active()) + str(token_id) + "-" + breed + ".json"
        )

        if Path(metadata_file_name).exists():
            print("{} already found!".format(metadata_file_name))
        else:
            print("Creating Metadata File {}".format(metadata_file_name))

            collectible_metadata['name']  = get_breed(nft_contract.tokenIdToBreed(token_id))
            collectible_metadata['description'] = "An adorable {} pup!".format(collectible_metadata['name'])
            print(collectible_metadata)

            image_upload = None
            if os.getenv("UPLOAD_IPFS") == 'true':
                image_path = "./img/{}.png".format(
                    breed.lower().replace("_", "-")
                )
                image_to_upload = upload_to_ipfs(image_path)

# 127.0.0.1:5001
# curl -X POST -F file=@img/pug.png http://localhost:5001/api/v0/add
# {"Name":"pug.png","Hash":"QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8","Size":"5699"}

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()['Hash']
        filename = filepath.split("/")[-1:][0]
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)
        print(uri)
        return uri
    return None