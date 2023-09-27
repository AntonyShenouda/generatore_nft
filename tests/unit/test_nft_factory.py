from brownie import network
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
    get_character,
)
from scripts.deploy_and_create import deploy_and_create


def test_can_create_nft_factory():
    # deploy the contract
    # create an NFT
    # get a random character back
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # Act
    nft_factory, creation_transaction = deploy_and_create()
    requestId = creation_transaction.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, nft_factory.address, {"from": get_account()}
    )
    # Assert
    print( nft_factory.tokenIdToCharacter(0))
    assert nft_factory.tokenCounter() == 1
    assert nft_factory.tokenIdToCharacter(0) == random_number % 5


def test_get_character():
    # Arrange / Act
    character = get_character(0)
    # Assert
    assert character == "OBAMA"
