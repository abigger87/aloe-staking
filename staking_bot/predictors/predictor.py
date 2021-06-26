'''
Aloe Capital LLC
06-12-2021
MIT License
'''

from abc import ABC, abstractmethod
from collections import namedtuple
from staking_bot.contracts import Proposal, Bounds


class Predictor(ABC):
    @abstractmethod
    def periodic(self):
        '''A place for performing periodic work, like fetching prices from an off-chain API,
        updating an ML model, or querying a remote database.
        '''
        pass

    @abstractmethod
    def get_proposals(self, extra_info: dict) -> list[Proposal]:
        '''A place to generate and/or finalize proposals that should be submitted in the current epoch

        Args:
            extra_info: Extra information from the contract that may be useful in formulating proposals.

        Returns:
            An array of proposals that should be submitted ASAP
        '''
        return [
            Proposal(
                bounds=Bounds(
                    lower=0,
                    upper=1,
                    are_inverted=False
                ),
                stake=10
            )
        ]
