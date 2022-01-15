from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract, BoxV2

from scripts.helpful_scripts import get_account, encode_data, upgrade

def main():
    account = get_account()
    box_contract = Box.deploy({"from": account})

    proxy_admin_contract = ProxyAdmin.deploy({"from": account})

    # store_transaction = box_contract.store(1)
    # store_transaction.wait(1)

    initializer = box_contract.store, 1
    encoded_function = encode_data()

    proxy_contract = TransparentUpgradeableProxy.deploy(
         box_contract.address,
        proxy_admin_contract.address,
        encoded_function,
        {"from": account, "gas_limit": 1000000}
    )

    # Attaching Box contract to the proxy
    proxy_box_contract = Contract.from_abi("Box", proxy_contract.address, Box.abi)

    proxy_box_contract.store(1, {"from": account})

    boxv2_contract = BoxV2.deploy({"from": account})

    # We upgrade the proxy contract to the newest implementation of box contract (boxv2_contract)
    transaction = upgrade(account, proxy_contract, boxv2_contract.address, proxy_admin_contract=proxy_admin_contract)

    transaction.wait(1)

    proxy_box_contract = Contract.from_abi("BoxV2", proxy_contract.address, BoxV2.abi)
    increment_transaction = proxy_box_contract.increment({"from": account})
    increment_transaction.wait(1)

    print(proxy_box_contract.retrieve())


