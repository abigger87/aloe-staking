from staking_bot.predictors.aggropredictor import AggroPredictor


def test_instantiation():
    ap = AggroPredictor()
    assert ap.step == 0


def test_periodic_step():
    ap = AggroPredictor()
    assert ap.step == 0
    ap.increment_step()
    assert ap.step == 1
