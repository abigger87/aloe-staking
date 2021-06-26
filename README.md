# staking-bot-template

_Author: Aloe Capital LLC_

If you want to write a bot that submits trading range predictions to Aloe's
Prediction Markets, but you've never worked with Web3 before, this is a great
place to start. We've laid the foundation required to interact with the blockchain
so that you can **focus on predictions, statistics, and the like.**

## Getting started

### Installation

If you already have a relatively new version of Python installed, and you've used
something like `pip`, `conda`, or `virtualenv` to install [`web3`](https://web3py.readthedocs.io/en/stable/index.html)
then you probably don't need to install anything else. Skip to the
[Environment Variables section](https://github.com/Aloe-Capital/staking-bot-template#Environment-Variables).
But if something isn't working or you just want to make sure you're using the same
setup we are, read on.

We're using [Poetry](https://python-poetry.org/) for dependency management. They've
put together some really nice documentation [here](https://python-poetry.org/docs/)
if you're unfamiliar. Once you have Poetry, install the staking bot like so:

```shell
poetry install
```

> If this doesn't work, install Python 3.9 (`apt-get install python3.9 python3.9-dev`) and try again.

### Environment Variables

Create a file named `.env` in the same folder as this `README`. You can use the
`.env.template` as a starting point. Fill in each value:

- `PROVIDER_ALCHEMY_KEY`: The Alchemy project key that the bot will run through
- `ACCOUNT_ADDRESS`: The Ethereum address you want to send from
- `ACCOUNT_PRIVATE_KEY`: The private key corresponding to that address
- `PREDICTIONS_CONTRACT_ADDRESS`: The predictions contract to which proposals will be sent
- `TIME_ALLOTTED_FOR_SENDING`: The bot will start submitting proposals this many seconds before the end of the epoch

> Note: The bot is configured for Kovan right now, so your Alchemy project should be associated with Kovan too. This is easy to change in [main.py](staking_bot/main.py), and you don't have to use Alchemy if you don't want to.

### Approving the contract

Before the bot can do its thing, you'll need to approve the predictions contract
to transfer your ALOE. You can do this on Etherscan or in our web app.

### Running

```shell
poetry run python staking_bot/main.py
```

## Adding your prediction algorithm

Now comes the fun part! To write your own prediction algorithm, just implement the
[`Predictor` interface](staking_bot/predictors/predictor.py). You can find an
example implementation [here](staking_bot/predictors/example.py).

After you've added your logic, make sure to add a new line to [`__init__.py`](staking_bot/predictors/__init__.py),
otherwise the rest of the code won't be able to find your algorithm. Now go to [main.py](staking_bot/main.py)
and import your predictor like so:

```python
from staking_bot.predictors import MyPredictor
```

Then find the following lines and adjust them appropriately:

```python
# Define key components:
# - contract: The predictions market to which we'll be submitting proposals
# - predictor: The algorithm to use for prediction
contract = AloePredictions(os.environ['PREDICTIONS_CONTRACT_ADDRESS'], w3)
predictor = ExamplePredictor()  # TODO change to MyPredictor()
```

That's it!

### Ideas

While you're still getting a feel for things, it may be helpful to start simple. Try
writing a `Predictor` that looks at Uniswap trading ranges over the past hour, and uses
that as its prediction for the next hour.

If you choose to do this, you'll find that the `extra_info` dictionary in `get_proposals()` contains a `'uniswap_bounds'` entry. This is a `Bounds` object that you could use to
construct a `Proposal` -- all you have to choose is the amount to stake.

Taking this one step further, you could modify the code to pass in a similar
`extra_info` dictionary to the predictor's `periodic()` function, and store a series of
Uniswap ranges. Then when it comes time to generate proposals, find a way to combine the
series you've collected (maybe use it to compute measurement uncertainty, and adjust your proposal accordingly)

That should give you a pretty good feel for the API. Now experiment! We've written this
in Python so that you can easily work with data science & ML libraries, so please take
advantage!
