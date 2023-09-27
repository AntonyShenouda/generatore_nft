from brownie import network
import time
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
)
from scripts.deploy_and_create import deploy_and_create


def test_can_create_nft_factory_integration():
    # deploy the contract
    # create an NFT
    # get a random character back
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    # Act
    nft_factory, creation_transaction = deploy_and_create()
    time.sleep(60)
    # Assert
    assert nft_factory.tokenCounter() == 1
