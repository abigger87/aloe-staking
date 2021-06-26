# ** Author: Andreas Bigger <bigger@usc.edu>

from staking_bot.predictors.predictor import Predictor
from staking_bot.contracts import Proposal
from staking_bot.contracts import Bounds


class AggroPredictor(Predictor):
    def __init__(self, example_argument='Hello World'):
        self._example_argument = example_argument
        self.step = 0

    def increment_step(self):
        # ** Increment step
        self.step += 1

    def periodic(self):
        super().periodic()

        # TODO: Fetch price feeds
        # TODO: Cache price in rapid time-series database

        # ** Increment step
        self.increment_step()

    def get_proposals(self, extra_info: dict) -> list[Proposal]:
        print(extra_info)
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
