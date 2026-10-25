import numpy as np

from gtfp_sbm.model import solve_sbm


def test_single_reference_dmu_is_efficient():
    result = solve_sbm(
        x=np.array([1.0]),
        y=np.array([1.0]),
        bad=np.array([1.0]),
        reference_x=np.array([[1.0]]),
        reference_y=np.array([[1.0]]),
        reference_bad=np.array([[1.0]]),
    )
    assert np.isclose(result.score, 1.0)
    assert np.allclose(result.input_slack, 0.0)
    assert np.allclose(result.desirable_slack, 0.0)
    assert np.allclose(result.undesirable_slack, 0.0)


def test_inefficient_observation_has_score_below_one():
    result = solve_sbm(
        x=np.array([2.0]),
        y=np.array([1.0]),
        bad=np.array([2.0]),
        reference_x=np.array([[1.0]]),
        reference_y=np.array([[1.0]]),
        reference_bad=np.array([[1.0]]),
    )
    assert np.isclose(result.score, 0.4)
