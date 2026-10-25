import numpy as np
import pandas as pd

from gtfp_sbm.open_methods import calculate_open_ml


def test_global_ml_returns_complete_stationary_panel():
    frame = pd.DataFrame(
        {
            "period": [2000, 2000, 2001, 2001],
            "dmu": ["A", "B", "A", "B"],
            "capital": [1.0, 2.0, 1.0, 2.0],
            "labor": [1.0, 2.0, 1.0, 2.0],
            "energy": [1.0, 2.0, 1.0, 2.0],
            "desirable_output": [1.0, 1.0, 1.0, 1.0],
            "undesirable_output": [1.0, 2.0, 1.0, 2.0],
        }
    )
    result = calculate_open_ml(frame, method="global-ml")
    assert result["score_valid"].all()
    assert np.allclose(result["gtfp"], 1.0)
    assert np.allclose(result["gtfp"], result["ec"] * result["tc"])
