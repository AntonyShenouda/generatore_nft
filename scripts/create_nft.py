from brownie import NFTFactory
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()
    nft_factory = NFTFactory[-1]
    fund_with_link(nft_factory.address, amount=Web3.toWei(0.1, "ether"))
    creation_transaction = nft_factory.createCollectible({"from": account})
    creation_transaction.wait(1)
    print("Nft created!")
