import pytest
from randfig.transforms import Unpack


@pytest.mark.parametrize('cfg,expected,keys,new_keys,remove', [
    [
        {"key_0": [0, 1], "key_1": [2, 3]},
        {
            "key_0": [0, 1], "key_1": [2, 3],
            "key_00": 0, "key_01": 1,
            "key_10": 2, "key_11": 3,
        },
        ["key_0", "key_1"],
        [["key_00", "key_01"], ["key_10", "key_11"]],
        False
    ],
    [
        {"key_0": [0, 1], "key_1": [2, 3]},
        {
            "key_00": 0, "key_01": 1,
            "key_10": 2, "key_11": 3,
        },
        ["key_0", "key_1"],
        [["key_00", "key_01"], ["key_10", "key_11"]],
        True
    ]
])
def test_unpack(cfg, expected, keys, new_keys, remove):
    unpack = Unpack(keys=keys, new_keys=new_keys, remove=remove)
    unpacked = unpack(cfg)
    assert expected == unpacked
