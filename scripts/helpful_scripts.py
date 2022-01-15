from brownie import network, config, accounts
import eth_utils

FORKED_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["ganache-local", "development"]


def get_account(index=None, id=None):
    """
    1. if index is specified, use accounts[index]
    2. if accountId is specified, use that account
    3. if we are on a development environment, use accounts[0]
    4. if we are on a test network generate your account from the private key in brownie-config.yaml,
    """

    # 1
    if index:
        return accounts[index]

    # 2
    if id:
        return accounts.load(id)

    # 3
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENTS
    ):
        return accounts[0]

    # 4
    return accounts.add(config["wallets"]["from_key"])


def encode_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")

    return initiazer.encode_input(*args)


def upgrade(
    account,
    proxy_contract,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_data = encode_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(proxy_contract.address, new_implementation_address, encoded_function_data, {"from": account})
        else:
            transaction = proxy_admin_contract.upgrade(proxy_contract.address, new_implementation_address, {"from": account})

    else:
        if initializer:
            encoded_function_data = encode_data(initializer, *args)
            transaction = proxy_contract.upgradeToAndCall(
                new_implementation_address, encoded_function_data, {"from": account}
            )
        else:
            transaction = proxy_contract.upgradeTo(new_implementation_address, {"from": account})
    
    
    return transaction
