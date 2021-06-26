'''
Aloe Capital LLC
06-12-2021
MIT License
'''

from staking_bot.predictors.predictor import Predictor

from staking_bot.contracts import Proposal
from staking_bot.contracts import Bounds


class Example(Predictor):
    def __init__(self, example_argument='Hello World'):
        # Your Predictor class is allowed to be stateful
        self._example_argument = example_argument

    def periodic(self):
        super().periodic()

        print(
            '''
            If you need to do periodic work, like fetching prices from some API,
            you can do that here
            '''
        )

    def get_proposals(self, extra_info: dict) -> list[Proposal]:
        print(extra_info)
        return [
            Proposal(
                bounds=Bounds(
                    lower=0,
                    upper=1,
                    are_inverted=False
                ),
                stake=1000000000000000000
            )
        ]
