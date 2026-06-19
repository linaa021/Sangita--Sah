import math

import pytest

from scs_cn import calculate_runoff


def test_normal_case_p50_cn80() -> None:
    q = calculate_runoff(50.0, 80.0)
    assert q >= 0
    assert q <= 50.0
    assert q > 0


def test_zero_rainfall() -> None:
    assert calculate_runoff(0.0, 80.0) == 0.0


def test_no_runoff_when_p_below_ia() -> None:
    # For CN=80, Ia is > 0, so P very small should yield 0 runoff
    assert calculate_runoff(1.0, 80.0) == 0.0


def test_cn_100_impervious() -> None:
    # With CN=100, S=0 and Ia=0, runoff should equal rainfall
    assert math.isclose(calculate_runoff(25.0, 100.0), 25.0, rel_tol=0, abs_tol=1e-12)


def test_negative_rainfall_raises() -> None:
    with pytest.raises(ValueError):
        calculate_runoff(-1.0, 80.0)


def test_invalid_cn_raises() -> None:
    with pytest.raises(ValueError):
        calculate_runoff(10.0, 0.0)
    with pytest.raises(ValueError):
        calculate_runoff(10.0, 101.0)


def test_physical_q_never_exceeds_p() -> None:
    for cn in [60, 70, 80, 90, 95, 100]:
        for p in [0, 1, 5, 10, 25, 50, 100]:
            q = calculate_runoff(float(p), float(cn))
            assert 0.0 <= q <= float(p)

