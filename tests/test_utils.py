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