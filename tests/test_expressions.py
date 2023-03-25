import pytest
import math
from decimal import Decimal
import randfig.expressions as expressions


@pytest.mark.parametrize('cfg,key,element,expected', [
    [
        {"not_list": 1, "list": [1]},
        "list",
        0,
        1
    ],
    [
        {"not_list": 1, "list": [1, 2]},
        "list",
        1,
        2
    ]
])
def test_pop(cfg, key, element, expected):
    out = expressions.pop(cfg, key, element)
    assert out == expected


@pytest.mark.parametrize('cfg,key', [
    [
        {"not_list": 1, "list": [1]},
        "not_list"
    ],
    [
        {"not_list": 1, "list": [1, 2]},
        "not_list"
    ]
])
def test_pop_not_list(cfg, key):
    with pytest.raises(TypeError):
        expressions.pop(cfg, key, 0)


@pytest.mark.parametrize('cfg,key,expected,expected_decimals', [
    [
        {"not_number": "1", "number": 1.1111},
        "number",
        1.11,
        2
    ]
])
def test_rounding(cfg, key, expected, expected_decimals):
    out = expressions.rounding(cfg, key, expected_decimals)
    Decimal(str(out)).as_tuple().exponent == expected_decimals
    assert out == expected


@pytest.mark.parametrize('cfg,key', [
    [
        {"not_number": "1", "number": 1.1111},
        "not_number"
    ]
])
def test_rounding_not_number(cfg, key):
    with pytest.raises(TypeError):
        expressions.rounding(cfg, key, 0)


@pytest.mark.parametrize('fn,cfg,kwargs,expected',
    [
        [
            expressions.min_threshold_from_resolution,
            {"resolution": 10, "non_affected_key": None},
            {"resolution_key": "resolution", "peak": 511, "sigmas": 2, "is_percentage": True},
            467.60297
        ],
        [
            expressions.min_threshold_from_resolution,
            {"resolution": 0.1, "non_affected_key": None},
            {"resolution_key": "resolution", "peak": 511, "sigmas": 2, "is_percentage": False},
            467.60297
        ],
        [
            expressions.max_threshold_from_resolution,
            {"resolution": 10, "non_affected_key": None},
            {"resolution_key": "resolution", "peak": 511, "sigmas": 2, "is_percentage": True},
            554.39702
        ],
        [
            expressions.max_threshold_from_resolution,
            {"resolution": 0.1, "non_affected_key": None},
            {"resolution_key": "resolution", "peak": 511, "sigmas": 2, "is_percentage": False},
            554.39702
        ]
])
def test_threshold_from_resolution(fn, cfg, kwargs, expected):
    out = fn(cfg, **kwargs)
    assert math.isclose(out, expected, abs_tol=0.00001)


@pytest.mark.parametrize('fn,cfg,kwargs,expected',
    [
        [
            expressions.min_threshold_from_resolution,
            {"resolution": 10, "non_affected_key": None},
            {"resolution_key": "resolution", "peak": 511, "sigmas": 2, "is_percentage": False},
            467.60297
        ],
        [
            expressions.max_threshold_from_resolution,
            {"resolution": 10, "non_affected_key": None},
            {"resolution_key": "resolution", "peak": 511, "sigmas": 2, "is_percentage": False},
            554.39702
        ]
])
def test_threshold_from_resolution_non_valid_resolution(fn, cfg, kwargs, expected):
    with pytest.raises(ValueError):
        fn(cfg, **kwargs)
