import pytest
import randfig.utils as utils
from collections import defaultdict


@pytest.mark.parametrize("mapping,map_list,expected",
    [
        (
            {"param_nested": 0},
            ["param_nested"],
            0
        ),
        (
            {"param_root": {"param_nested": {"param_0": 0, "param_1": 1}}},
            ["param_root", "param_nested"],
            {"param_0": 0, "param_1": 1}
        ),
        (
            {"param_root": {"param_nested": {"param_0": 0, "param_1": 1}}},
            ["param_root", "param_nested", "param_0"],
            0
        )
    ])
def test_get_nested_value(mapping, map_list, expected):
    nested_val = utils.get_nested_value(mapping, map_list)
    assert nested_val == expected


@pytest.mark.parametrize("mapping,expected",
    [
        (
            {"param_nested": 0},
            defaultdict(defaultdict, {"param_nested": 0})
        ),
        (
            {
                "param_root_0": {"param_00": "value_00", "param_01": "value_01"},
                "param_root_1": {"param_10": "value_10", "param_20": {"param_200": "value_200"}}
            },
            defaultdict(defaultdict, {
                "param_root_0": defaultdict(defaultdict, {
                    "param_00": "value_00",
                    "param_01": "value_01"
                }),
                "param_root_1": defaultdict(defaultdict, {
                    "param_10": "value_10",
                    "param_20": defaultdict(defaultdict, {"param_200": "value_200"})
                })
            }),
        )
    ])
def test_mapping_to_defaultdict(mapping, expected):
    out = utils.mapping_to_defaultdict(mapping)
    assert out == expected


@pytest.mark.parametrize("expected,mapping",
    [
        (
            {"param_nested": 0},
            defaultdict(defaultdict, {"param_nested": 0})
        ),
        (
            {
                "param_root_0": {"param_00": "value_00", "param_01": "value_01"},
                "param_root_1": {"param_10": "value_10", "param_20": {"param_200": "value_200"}}
            },
            defaultdict(defaultdict, {
                "param_root_0": defaultdict(defaultdict, {
                    "param_00": "value_00",
                    "param_01": "value_01"
                }),
                "param_root_1": defaultdict(defaultdict, {
                    "param_10": "value_10",
                    "param_20": defaultdict(defaultdict, {"param_200": "value_200"})
                })
            }),
        )
    ])
def test_mapping_to_dict(expected, mapping):
    out = utils.mapping_to_dict(mapping)
    assert out == expected


@pytest.mark.parametrize('cfg,expected,keys,value', [
    [
        {"param_root_0": {"param_00": "value_00"}},
        {"param_root_0": {"param_00": "value_00"}, "param_root_1": "value_1"},
        ["param_root_1"],
        "value_1"
    ],
    [
        {"param_root_0": {"param_00": "value_00"}},
        {"param_root_0": {"param_00": "value_00", "param_01": "value_01"}},
        ["param_root_0", "param_01"],
        "value_01"
    ],
    [
        {"param_root_0": {"param_00": {"param_000": "value_000"}}},
        {"param_root_0": {"param_00": {"param_000": "value_000", "param_001": "value_001"}}},
        ["param_root_0", "param_00", "param_001"],
        "value_001"
    ]
])
def test_insert_nested_key(cfg, expected, keys, value):
    utils.insert_nested_key(cfg, keys, value)
    assert cfg == expected


@pytest.mark.parametrize('cfg,expected,keys,value', [
    [
        {"param_root_0": {"param_00": "value_00"}},
        {"param_root_0": "value_0"},
        ["param_root_0"],
        "value_0"
    ],
    [
        {"param_root_0": {"param_00": "value_00"}},
        {"param_root_0": {"param_00": "update_00"}},
        ["param_root_0", "param_00"],
        "update_00"
    ],
    [
        {"param_root_0": {"param_00": {"param_000": "value_000"}}},
        {"param_root_0": {"param_00": {"param_000": "update_000"}}},
        ["param_root_0", "param_00", "param_000"],
        "update_000"
    ]
])
def test_update_nested_key(cfg, expected, keys, value):
    utils.insert_nested_key(cfg, keys, value)
    assert cfg == expected


@pytest.mark.parametrize('cfg,keys', [
    [
        "not_mapping_0",
        ["not_mapping_0"]
    ],
    [
        {"param_root_0": "not_mapping_0"},
        ["param_root_0", "param_00"]
    ],
    [
        {"param_root_0": {"param_00": "not_mapping_00"}},
        ["param_root_0", "param_00", "param_000"]
    ]
])
def test_raise_error_nested_key(cfg, keys):
    with pytest.raises(TypeError):
        utils.insert_nested_key(cfg, keys, "value")


@pytest.mark.parametrize('cfg,expected,keys', [
    [
        {"param_root_0": "value_0"},
        {},
        ["param_root_0"],
    ],
    [
        {"param_root_0": {"param_00": "value_00", "param_01": "value_01"}},
        {"param_root_0": {"param_00": "value_00"}},
        ["param_root_0", "param_01"]
    ],
    [
        {"param_root_0": {"param_00": {"param_000": "value_000", "param_001": "value_001"}}},
        {"param_root_0": {"param_00": {"param_000": "value_000"}}},
        ["param_root_0", "param_00", "param_001"]
    ]
])
def test_remove_nested_key(cfg, expected, keys):
    utils.remove_nested_key(cfg, keys)
    assert cfg == expected


@pytest.mark.parametrize('cfg,keys', [
    [
        "not_mapping_root_0",
        ["not_mapping_root_0"],
    ],
    [
        {"param_root_0": "not_mapping_0"},
        ["param_root_0", "param_01"]
    ],
    [
        {"param_root_0": {"param_00": "not_mapping_00"}},
        ["param_root_0", "param_00", "param_001"]
    ]
])
def test_remove_nested_key(cfg, keys):
    with pytest.raises(TypeError):
        utils.remove_nested_key(cfg, keys)


@pytest.mark.parametrize('value,p,reference,tries', [
    [460, 0.01, 511, 10]
])
def test_add_uniform_jitter(value, p, reference, tries):
    max_allowed = value + p * reference
    min_allowed = value - p * reference

    for _ in range(tries + 1):
        out = utils.add_uniform_jitter(value, p, reference)
        assert min_allowed <= out and out <= max_allowed


@pytest.mark.parametrize('value,p,reference', [
    ['', 0.1, 511],
    [460, '', 511],
    [460, 0.1, '']
])
def test_add_uniform_jitter_type_error(value, p, reference):
    with pytest.raises(TypeError):
        utils.add_uniform_jitter(value, p, reference)


@pytest.mark.parametrize('num,expected', [
    [1, [1]],
    [2, [1, 2]],
    [25, [1, 5, 25]],
    [210, [1, 2, 3, 5, 6, 7, 10, 14, 15, 21, 30, 35, 42, 70, 105, 210]],
])
def test_get_divisors(num, expected):
    out = utils.get_divisors(num)
    assert out == expected


def test_get_divisors_zero_value_error():
    with pytest.raises(ValueError):
        utils.get_divisors(0)


@pytest.mark.parametrize('n,divisors,expected', [
    [1, [0, 15], None],
    [1, [1, 15], 1],
    [1, [2, 15], None],
    [210, [21], 21],
    [210, [7, 21], 7],
    [210, [106], None],
    [210, [9, 106], None],
    [210, [210], 210]
])
def test_find_divisor(n, divisors, expected):
    out = utils.find_divisor(n, divisors)
    assert out == expected


@pytest.mark.parametrize('n,divisors', [
    [0, [1, 0]],
    [1, [0]],
    [1, [0, 0]],
    [1, []]
])
def test_find_divisor_value_error(n, divisors):
    with pytest.raises(ValueError):
        utils.find_divisor(n, divisors)


@pytest.mark.parametrize('n,threshold,expected', [
    [1, 1, 1],
    [1, 2, 1],
    [210, 31, 30],
    [210, 34, 30],
    [210, 35, 30],
    [210, 211, 210]
])
def test_find_immediately_lower_divisor(n, threshold, expected):
    out = utils.find_immediately_lower_divisor(n, threshold)
    assert out == expected


@pytest.mark.parametrize('n,threshold', [
    [0, 2],
    [2, 0]
])
def test_find_immediately_lower_divisor_value_error(n, threshold):
    with pytest.raises(ValueError):
        utils.find_immediately_lower_divisor(n, threshold)


@pytest.mark.parametrize('n,threshold,expected', [
    [1, 1, 1],
    [1, 2, 1],
    [210, 29, 30],
    [210, 30, 35],
    [210, 34, 35],
    [210, 104, 105],
    [210, 105, 210],
    [210, 210, 210],
    [210, 211, 210]
])
def test_find_immediately_upper_divisor(n, threshold, expected):
    out = utils.find_immediately_upper_divisor(n, threshold)
    assert out == expected


@pytest.mark.parametrize('n,threshold', [
    [0, 2],
    [2, 0]
])
def test_find_immediately_upper_divisor_value_error(n, threshold):
    with pytest.raises(ValueError):
        utils.find_immediately_upper_divisor(n, threshold)


@pytest.mark.parametrize('n,divisors,not_found_strategy,threshold,expected', [
    [1, [4, 9], "min", 1, 1],
    [1, [4, 9], "max", 1, 1],
    [1, [1], "max", 1, 1],
    [1, [1], "max", 1, 1],
    [210, [4, 9, 7, 10], "min", 1, 7],
    [210, [4, 9], "min", 8, 7],
    [210, [4, 9], "min", 7, 6],
    [210, [4, 9], "max", 11, 14],
    [210, [4, 9], "max", 14, 15],
    [210, None, "min", 8, 7],
    [210, None, "max", 11, 14],
])
def test_search_divisor(n, divisors, not_found_strategy, threshold, expected):
    out = utils.search_divisor(
        n=n,
        divisors=divisors,
        not_found_strategy=not_found_strategy,
        threshold=threshold
    )
    assert out == expected


@pytest.mark.parametrize('cfg,new_keys,expected,remove', [
    [
        {"key": [0]},
        ["new_0"],
        {"key": [0], "new_0": 0},
        False
    ],
    [
        {"key": [0, 1]},
        ["new_0", "new_1"],
        {"key": [0, 1], "new_0": 0, "new_1": 1},
        False
    ],

    [
        {"key": [0, 1]},
        ["new_0", "new_1"],
        {"key": [0, 1], "new_0": 0, "new_1": 1},
        False
    ],
    [
        {"key": (0, 1)},
        ["new_0", "new_1"],
        {"key": (0, 1), "new_0": 0, "new_1": 1},
        False
    ],
    [
        {"key": (0, 1)},
        ["new_0", "new_1"],
        {"new_0": 0, "new_1": 1},
        True
    ],
])
def test_unpack(cfg, new_keys, expected, remove):
    out = utils.unpack(cfg=cfg, key="key", new_keys=new_keys, remove=remove)
    assert out == expected


@pytest.mark.parametrize('cfg,new_keys', [
    [
        {"key": [0, 1]},
        ["new_0", "new_1", "new_2"]
    ],
    [
        {"key": [0, 1, 2]},
        ["new_0", "new_1"]
    ]
])
def test_unpack_value_error(cfg, new_keys):
    with pytest.raises(ValueError):
        utils.unpack(cfg=cfg, key="key", new_keys=new_keys)


@pytest.mark.parametrize('cfg,new_keys', [
    [
        {"key": 0},
        ["new_0", "new_1", "new_2"]
    ]
])
def test_unpack_type_error(cfg, new_keys):
    with pytest.raises(TypeError):
        utils.unpack(cfg=cfg, key="key", new_keys=new_keys)
