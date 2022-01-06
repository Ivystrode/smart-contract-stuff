from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import BREED_MAPPING, get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests, json, os


breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}

def main():
    """
    brownie run scripts/advanced_collectible/create_metadata.py --network rinkeby
    will show all the NFTs you made on rinkeby chain
    """
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} NFTs")
    
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_filename = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        print(metadata_filename)
        
        collectible_metadata = metadata_template
        
        if Path(metadata_filename).exists():
            print(f"{metadata_filename} already exists. Delete it to override.")
        else:
            collectible_metadata['name'] = breed
            collectible_metadata['description'] = f"An adorable {breed}"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            
            image_uri = None
            # so that we dont upload to IPFS (since we have to have the node running)
            if os.getenv("UPLOAD_IPFS") is True:
                image_uri = upload_to_ipfs(image_path)
            # if we are not uploading to IPFS we need to get the image URI, which we will just hardcode
            image_uri = image_uri if image_uri else breed_to_image_uri[breed] # if upload to IPFS happened we got returned a URI - if not, just get it from the hardcoded dict

            collectible_metadata['image'] = image_uri
            print(collectible_metadata)
            with open(metadata_filename, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_filename)
                
                
            print(f"Created metadata file: {metadata_filename}")
            

            
def upload_to_ipfs(filepath):
    """
    This assumes you are going to keep the ipfs node running to host the image
    """
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file":image_binary})
        ipfs_hash = response.json()['Hash']
        filename = filepath.split("/")[-1:][0] # "./img/pug.png" --> "pug.png"
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
        # upload stuff
        # need to download IPFS command line interface