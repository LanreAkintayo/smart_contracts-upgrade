from brownie import ProxyAdmin, TransparentUpgradeableProxy, Box, BoxV2, Contract
from scripts.helpful_scripts import get_account, encode_data
import pytest


def test_proxy_upgrades():
    account = get_account()

    encoded_function = encode_data()
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box = Box.deploy({"from": account})

    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, encoded_function
    )

    boxv2 = boxv2.deploy({"from": account})
    proxy_boxv2 = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    with pytest.raises(exceptions.VirtualMachineError):
        proxy_boxv2.increment({"from": account})
    
    upgrade(account, proxy, boxv2.address, proxy_admin_contract=proxy_admin)
    
    assert proxy_boxv2.retrieve() == 0

    proxy_boxv2.increment({"from": account})

    assert proxy_boxv2.retrieve() == 1






