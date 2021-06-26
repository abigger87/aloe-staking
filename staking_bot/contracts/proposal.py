'''
Aloe Capital LLC
06-12-2021
MIT License
'''

from typing import Optional
import warnings

from staking_bot.contracts.bounds import Bounds, inverted


class Proposal():
    _bounds: Bounds
    _stake: int
    _source: Optional[str]
    _epoch: Optional[int]
    _key: Optional[int]

    _is_up_to_date: bool

    def __init__(self, bounds: Bounds, stake: int, source: Optional[str] = None, epoch: Optional[int] = None, key: Optional[int] = None):
        self._bounds = bounds
        self._stake = stake

        if source is None or epoch is None or key is None:
            assert source is None and epoch is None and key is None, 'All-or-nothin with the Nones please'
            self._is_up_to_date = False
        else:
            self._is_up_to_date = True

        self._source = source
        self._epoch = epoch
        self._key = key

    @property
    def is_submitted(self) -> bool:
        return self._key is not None

    @property
    def is_is_up_to_date(self) -> bool:
        return self._is_up_to_date

    @property
    def bounds(self) -> Bounds:
        return self._bounds

    @bounds.setter
    def bounds(self, x):
        self._is_up_to_date = False
        self._bounds = x

    @property
    def stake(self) -> int:
        return self._stake

    @stake.setter
    def stake(self, x):
        if self.is_submitted:
            warnings.warn(
                'Attempt to change stake amount on a submitted proposal: this can\'t be propagated to blockchain!'
            )
            return

        self._stake = x

    @property
    def source(self) -> Optional[str]:
        return self._source

    @property
    def epoch(self) -> Optional[int]:
        return self._epoch

    @property
    def key(self) -> Optional[int]:
        return self._key

    def invert_bounds(self):
        self.bounds = inverted(self.bounds)

    def reset(self):
        self._source = None
        self._epoch = None
        self._key = None

    def submit_to(self, contract):
        if self.is_submitted:
            warnings.warn(
                'Attempt to submit already-submitted proposal. If you want another with the same bounds, call reset() and try again'
            )
            return

        should_invert = contract.get_should_invert_prices()
        bounds: Bounds = self.bounds if should_invert == self.bounds.are_inverted else inverted(
            self.bounds)

        def send(nonce: int, gasPrice: int, private_key: str):
            txn = contract.build_txn_submit_proposal(
                bounds.lower, bounds.upper, self.stake, nonce, gasPrice)
            contract.send(txn, private_key)

        return send
