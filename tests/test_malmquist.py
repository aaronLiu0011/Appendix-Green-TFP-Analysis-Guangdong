import numpy as np
import pandas as pd

from gtfp_sbm.malmquist import calculate_malmquist_panel


def test_unchanged_panel_has_unit_indices():
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
    result = calculate_malmquist_panel(frame)
    assert np.allclose(result["gtfp"], 1.0)
    assert np.allclose(result["ec"], 1.0)
    assert np.allclose(result["tc"], 1.0)
    assert np.allclose(result["gtfp"], result["ec"] * result["tc"])
