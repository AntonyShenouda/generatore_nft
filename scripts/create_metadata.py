from brownie import NFTFactory, network
from scripts.helpful_scripts import get_character
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

character_to_image_uri = {
    "OBAMA": "https://ipfs.io/ipfs/QmSb52Y1pbfEd99HJm4BdXtaLeNzJNDjkgcH8UQ9CMi9iG?filename=obama.png",
    "STEVE_JOBS": "https://ipfs.io/ipfs/QmdgvkSoFKKp7NmAd96Vw3y5EU1r1MPCYmTbEwoJmTbUz2?filename=steve-jobs.png",
    "EMMA_WATSON": "https://ipfs.io/ipfs/QmPiYg33VMrSALJErC92CectncDHNrcWEjNGMU7gKAw15C?filename=emma-watson.png",
    "TRUMP": "https://ipfs.io/ipfs/QmVVgdDSZDBDuVbNrAryUU1AntRB7VY1YW3qrFjgvQcf6a?filename=trump.png",
    "RONALDO": "",
}
character_to_attributes = {
    "OBAMA": [
        {"trait_type": "charismatic", "value": 80},
        {"trait_type": "inspirational", "value": 90},
        {"trait_type": "thoughtful", "value": 70},
    ],
    "STEVE_JOBS": [
        {"trait_type": "innovative", "value": 90},
        {"trait_type": "visionary", "value": 80},
        {"trait_type": "creative", "value": 90},
    ],
    "EMMA_WATSON":[
        {"trait_type": "talented", "value": 80},
        {"trait_type": "empowering", "value": 70},
        {"trait_type": "elegant", "value": 80},
    ],
    "TRUMP": [
        {"trait_type": "controversial", "value": 70},
        {"trait_type": "influential", "value": 70},
        {"trait_type": "polarizing", "value": 80},
    ],
    "RONALDO": [
        {"trait_type": "athletic", "value": 90},
        {"trait_type": "skilled", "value": 90},
        {"trait_type": "determined", "value": 80},
    ],
}

def main():
    nft_factory = NFTFactory[-1]
    print(nft_factory)
    number_of_nfts = nft_factory.tokenCounter()
    print(f"You have created {number_of_nfts} nfts!")
    for token_id in range(number_of_nfts):
        character = get_character(nft_factory.tokenIdToCharacter(token_id))
        print(f"Character to use for the following token is {character}")
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{character}.json"
        )
        nft_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            nft_metadata["name"] = character
            nft_metadata["description"] = f"An image of {character}!"
            nft_metadata["attributes"] = character_to_attributes[character]

            image_path = "./img/" + character.lower().replace("_", "-") + ".png"

            image_uri = None
            if os.getenv("UPLOAD_IPFS"):
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else character_to_image_uri[character]

            nft_metadata["image"] = image_uri
            with open(metadata_file_name, mode="w") as file:
                json.dump(nft_metadata, file)
            if os.getenv("UPLOAD_IPFS"):
                upload_to_ipfs(metadata_file_name)



## start ipfs locally by using ipfs deamon
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
