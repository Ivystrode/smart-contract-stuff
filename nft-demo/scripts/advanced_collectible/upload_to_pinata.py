"""
https://www.pinata.cloud/
"""
import os, requests
from pathlib import Path

PINATA_BASE_URL = "https://api.pinata.cloud"
endpoint = "/pinning/pinFileToIPFS"

# change this filepath or make dynamic etc
filepath = "./img/pug.png"
filename = filepath.split("/")[-1:][0]
headers = {"pinata_api_key": os.getenv("PINATA_API_KEY"), "pinata_secret_api_key": os.getenv("PINATA_API_SECRET")}

def main():
    """
    A third party service to upload it to as well as your own ipfs node
    This is a file management service for ipfs - it pins it on their node as well as ours
    """
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(PINATA_BASE_URL + endpoint, files={"file": (filename, image_binary)}, headers=headers)
        print(response.json())
        
main()