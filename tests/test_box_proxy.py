from brownie import ProxyAdmin, TransparentUpgradeableProxy, Box, Contract, BoxV2, exceptions
from scripts.helpful_scripts import get_account, encode_data, upgrade
import pytest

def test_proxy_delegates_call():
    """
    Check if after attaching implementation contract to the proxy contract, we can still call the methods of the implementation contract with the proxy contract
    """
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    data = encode_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        data,
        {"from": account}
    )

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    assert proxy_box.retrieve() == 0

    proxy_box.store(1, {"from": account})

    assert proxy_box.retrieve() == 1

def test_proxy_upgrades():
    account = get_account()

    encoded_function = encode_data()
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box = Box.deploy({"from": account})

    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, encoded_function, {"from": account}
    )

    boxv2 = BoxV2.deploy({"from": account})
    proxy_boxv2 = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    with pytest.raises(exceptions.VirtualMachineError):
        proxy_boxv2.increment({"from": account})
    
    upgrade(account, proxy, boxv2.address, proxy_admin_contract=proxy_admin)
    
    assert proxy_boxv2.retrieve() == 0

    proxy_boxv2.increment({"from": account})

    assert proxy_boxv2.retrieve() == 1