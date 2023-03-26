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


@pytest.mark.parametrize('cfg,kwargs,expected', [
    [
        {"num": 5, "den": 2},
        {"num_key": "num", "den_key": "den", "integer": False},
        2.5
    ],
    [
        {"num": 5, "den": 2},
        {"num_key": "num", "den_key": "den", "integer": True},
        2
    ],
    [
        {"num": 2, "den": 2},
        {"num_key": "num", "den_key": "den", "integer": False},
        1
    ],
    [
        {"num": 2, "den": 2},
        {"num_key": "num", "den_key": "den", "integer": True},
        1
    ]
])
def test_division(cfg, kwargs, expected):
    out = expressions.division(cfg, **kwargs)
    
    if kwargs["integer"]:
        assert out == expected
    else:
        assert math.isclose(out, expected)


@pytest.mark.parametrize('cfg,expected', [
    [{"a": 2, "b": 3}, 6],
    [{"a": 2.3, "b": 3.5}, 8.05]
])
def test_product(cfg, expected):
    out = expressions.product(cfg, "a", "b")
    assert math.isclose(out, expected, abs_tol=0.01)


@pytest.mark.parametrize('cfg', [
    {"a": None, "b": 3},
    {"a": 2.3, "b": ""}
])
def test_product_value_error(cfg):
    with pytest.raises(TypeError):
        expressions.product(cfg, "a", "b")


@pytest.mark.parametrize('cfg,expected', [
    [{"side_len": 4, "apothem": 2.75}, 5],
    [{"side_len": 4, "apothem": 3.4}, 6],
    [{"side_len": 0.5, "apothem": 79.57}, 1000],
    [{"side_len": 0.5, "apothem": 795.77}, 10000],
    [{"side_len": 0.5, "apothem": 7957.82}, 100001]
])
def test_get_regular_polygon_sides(cfg, expected):
    out = expressions.get_regular_polygon_sides(cfg, "side_len", "apothem")
    assert out == expected


@pytest.mark.parametrize('cfg', [
    {"side_len": "", "apothem": 2.75},
    {"side_len": 4, "apothem": []},
])
def test_get_regular_polygon_sides_value_error(cfg):
    with pytest.raises(TypeError):
        expressions.get_regular_polygon_sides(cfg, "side_len", "apothem")


@pytest.mark.parametrize('cfg,expected', [
    [{"key": 0}, 2],
    [{"key": 0.1}, 2],
    [{"key": 0.5}, 2],
    [{"key": 0.8}, 2],
    [{"key": 99}, 100],
    [{"key": 10057.85}, 10058],
    [{"key": 10057.01}, 10058],
    [{"key": 10056.01}, 10056],
    [{"key": 10056.85}, 10056],
])
def test_round_to_closest_even(cfg, expected):
    out = expressions.round_to_closest_even(cfg, "key")
    assert out == expected


@pytest.mark.parametrize('cfg', [{"key": {}}])
def test_round_to_closest_even_type_error(cfg):
    with pytest.raises(TypeError):
        expressions.round_to_closest_even(cfg, "key")


@pytest.mark.parametrize('cfg,expected', [
    [{"side_len": 4, "n_sides": 5}, 2.75276],
    [{"side_len": 4, "n_sides": 6}, 3.464101],
    [{"side_len": 0.5, "n_sides": 1000}, 79.57720],
    [{"side_len": 0.5, "n_sides": 10000}, 795.77468],
    [{"side_len": 0.5, "n_sides": 100001}, 7957.82672]
])
def test_get_regular_polygon_apothem(cfg, expected):
    out = expressions.get_regular_polygon_apothem(cfg, "side_len", "n_sides")
    assert math.isclose(out, expected, abs_tol=0.0001)


@pytest.mark.parametrize('cfg', [
    {"side_len": "", "apothem": 2.75},
    {"side_len": 4, "apothem": []},
])
def test_get_regular_polygon_sides_value_error(cfg):
    with pytest.raises(TypeError):
        expressions.get_regular_polygon_sides(cfg, "side_len", "apothem")
