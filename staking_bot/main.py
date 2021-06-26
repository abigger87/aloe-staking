'''
Aloe Capital LLC
06-12-2021
MIT License
'''

import os
from time import time, sleep

from dotenv import load_dotenv
from web3.gas_strategies.time_based import fast_gas_price_strategy
from web3 import Web3

from staking_bot.contracts import AloePredictions, Proposal
from staking_bot.predictors import Predictor as MainPredictor


def main():
    # Load environment variables
    load_dotenv()

    # Configure a Web3 Provider, in this case Alchemy
    w3 = Web3(
        Web3.WebsocketProvider(
            'wss://eth-kovan.ws.alchemyapi.io/v2/' +
            os.environ['PROVIDER_ALCHEMY_KEY']
        )
    )
    # Configure gas price strategy. For example, if os.environ['TIME_ALLOTTED_FOR_SENDING']
    # is set to 120 seconds, you may want to use the `fast_gas_price_strategy` to ensure
    # that your proposals are submitted before the end of the epoch
    w3.eth.set_gas_price_strategy(fast_gas_price_strategy)

    # Define key components:
    # - contract: The predictions market to which we'll be submitting proposals
    # - predictor: The algorithm to use for prediction
    contract = AloePredictions(os.environ['PREDICTIONS_CONTRACT_ADDRESS'], w3)
    predictor = MainPredictor()

    epoch_of_most_recent_submission = None

    while True:
        # Call the predictor every 60 seconds so it can do things like fetch price data,
        # update a database, backpropagate an ML model, etc.
        predictor.periodic()

        # Pull in some basic data from the predictions market. This helps us know whether
        # we need to send proposals RIGHT AWAY, or if we have some time to chill
        epoch = contract.get_epoch()
        epoch_end_time = contract.get_epoch_expected_end_time()
        time_left_in_epoch = epoch_end_time - int(time())  # in seconds

        print(f'{time_left_in_epoch / 60} minutes left in epoch')

        # This becomes true just before the epoch ends
        should_submit = time_left_in_epoch < int(
            os.environ['TIME_ALLOTTED_FOR_SENDING']
        ) and (
            epoch_of_most_recent_submission is None or
            epoch > epoch_of_most_recent_submission
        )

        if should_submit:
            # Ask the predictor for proposals to submit. Can return 1, multiple, or 0 -- doesn't matter
            proposals: list[Proposal] = predictor.get_proposals({
                # If you want to use other data from the contract to guide
                # predictions, pass that in here. For example:
                'uniswap_bounds': contract.get_uniswap_bounds(),
                'active_aggregate': contract.get_active_aggregate()
            })

            print(f'Predictor returned {len(proposals)} proposals to submit')

            nonce = w3.eth.get_transaction_count(os.environ['ACCOUNT_ADDRESS'])
            gas_price = w3.eth.generate_gas_price()

            # Send all of the proposals
            for proposal in proposals:
                print(
                    f'SUBMITTING: Lower: {proposal.bounds.lower}\tUpper: {proposal.bounds.upper}\tStake: {proposal.stake}')
                receipt = proposal.submit_to(contract)(
                    nonce,
                    gas_price,
                    os.environ['ACCOUNT_PRIVATE_KEY']
                )
                print('\tSUBMITTED')
                nonce += 1

            epoch_of_most_recent_submission = epoch

        sleep(60)


if __name__ == '__main__':
    main()
