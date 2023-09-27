from brownie import network, NFTFactory
from scripts.helpful_scripts import OPENSEA_URL, get_character, get_account


character_to_metadata = {
    "OBAMA": "https://ipfs.io/ipfs/QmVuS382gyKob937SRTHC92NLPLRERmgnqUf3DKgAD19tE?filename=1-OBAMA.json",
    "STEVE_JOBS": "https://ipfs.io/ipfs/Qmf1eYagq2dxGdLKWsnd7YJW4UVBF7Z9J58cfdgvxTknGZ?filename=4-STEVE_JOBS.json",
    "EMMA_WATSON": "https://ipfs.io/ipfs/QmbfLf6QYyyyFj8f3uk7f4tNj5PaAsGsJoea8PVZRkkLGK?filename=2-EMMA_WATSON.json",
    "TRUMP": "https://ipfs.io/ipfs/Qmd78zWzYttqq6xMgrrSFioj2W28gnaDYWoFSfcudWQCTC?filename=0-TRUMP.json",
    "RONALDO": "",
}
def main():
    print(f"Working on {network.show_active()}")
    nft_factory = NFTFactory[-1]
    number_of_nfts = nft_factory.tokenCounter()
    print(f"You have {number_of_nfts} tokenIds")
    for token_id in range(number_of_nfts):
        breed = get_character(nft_factory.tokenIdToCharacter(token_id))
        if not nft_factory.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, nft_factory, character_to_metadata[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
