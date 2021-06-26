'''
Aloe Capital LLC
06-12-2021
MIT License
'''

import json
import os
import warnings

from web3 import Web3

from staking_bot.contracts.bounds import Bounds
from staking_bot.contracts.contract import Contract
from staking_bot.contracts.proposal import Proposal


abi = None

abi_path = os.path.split(__file__)[0]
abi_path = os.path.join(abi_path, 'abis', 'AloePredictions.json')

with open(abi_path, 'r') as fp:
    abi = json.load(fp)


class AloePredictions(Contract):

    def __init__(self, address: str, w3: Web3):
        super().__init__(address, abi, w3)

    def get_epoch(self) -> int:
        '''Gets the current epoch ID'''
        return self._inner.functions.epoch().call()

    def get_epoch_start_time(self) -> int:
        '''Gets time (in seconds) at which the current epoch started'''
        return self._inner.functions.epochStartTime().call()

    def get_epoch_expected_end_time(self) -> int:
        '''Gets the expected end time (in seconds) of the current epoch'''
        return self._inner.functions.epochExpectedEndTime().call()

    def get_did_invert_prices(self) -> bool:
        '''Gets whether prices were inverted in the previous epoch'''
        return self._inner.functions.didInvertPrices().call()

    def get_should_invert_prices(self) -> bool:
        '''Gets whether prices should be inverted for submissions in the current epoch'''
        return self._inner.functions.shouldInvertPrices().call()

    def get_active_aggregate(self) -> Bounds:
        '''Gets the aggregate prediction from the previous epoch'''
        res = self._inner.functions.current().call()
        return Bounds(
            lower=res[0][0],
            upper=res[0][1],
            # Equivalent to self._inner.functions.didInvertPrices().call()
            are_inverted=res[1]
        )

    def get_current_aggregate(self) -> Bounds:
        '''Gets the aggregate prediction from the current epoch. Malleable until `advance()`'''
        res = self._inner.functions.aggregate().call()
        return Bounds(
            lower=res[0][0],
            upper=res[0][1],
            are_inverted=self.get_should_invert_prices()
        )

    def get_uniswap_bounds(self) -> Bounds:
        '''Gets Uniswap bounds over the past 60 minutes, independent of epoch state'''
        res = self._inner.functions.fetchGroundTruth().call()
        return Bounds(
            lower=res[0][0],
            upper=res[0][1],
            are_inverted=self.get_did_invert_prices()
        )

    def get_proposal(self, key: int) -> Proposal:
        '''Gets an existing proposal by key'''
        res = self._inner.functions.proposals(key).call()

        epoch_current = self.get_epoch()
        epoch_proposal = res[1]
        inverted = False

        if epoch_proposal == epoch_current:
            inverted = self.get_should_invert_prices()
        elif epoch_proposal == epoch_current - 1:
            inverted = self.get_did_invert_prices()
        else:
            warnings.warn(
                f'Could not quickly determine whether Proposal {key} has inverted bounds. Defaulting to False. Please examine events surrounding Epoch {epoch_proposal} if you need correct data'
            )

        bounds = Bounds(
            lower=res[2],
            upper=res[3],
            are_inverted=inverted
        )
        return Proposal(
            bounds=bounds,
            stake=res[4],
            source=res[0],
            epoch=epoch_proposal,
            key=key
        )

    def is_proposal_reward_claimed(self, key: int) -> bool:
        '''Gets whether an existing proposal's reward has been claimed'''
        res = self._inner.functions.proposals(key).call()
        return res[4] == 0

    def build_txn_submit_proposal(self, lower: int, upper: int, stake: int, nonce: int, gasPrice: int) -> dict:
        return self._inner.functions.submitProposal(lower, upper, stake).buildTransaction({
            'nonce': nonce,
            'gas': 700000,
            'gasPrice': gasPrice,
        })
