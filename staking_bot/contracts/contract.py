'''
Aloe Capital LLC
06-12-2021
MIT License
'''

from web3 import Web3


class Contract:
    _address: str
    _w3: Web3

    def __init__(self, address: str, abi, w3: Web3):
        self._address = address
        self._w3 = w3
        self._inner = w3.eth.contract(address=address, abi=abi)

    def send(self, txn_dict: dict, private_key: str):
        signed_txn = self._w3.eth.account.sign_transaction(
            txn_dict, private_key=private_key)
        self._w3.eth.send_raw_transaction(signed_txn.rawTransaction)
