import pytest
from randfig.transforms import Insert


@pytest.mark.parametrize('cfg,expected,keys,value', [
    [
        {"param_root_0": 0},
        {"param_root_0": 0, "param_root_1": 1},
        ["param_root_1"],
        1
    ]
])
def test_insert(cfg, expected, keys, value):
    insert = Insert(keys=keys, value=value)
    inserted = insert(cfg)
    assert expected == inserted


def test_insert_two_times():
    insert = Insert(keys=["param_root_1"], value=1)
    expected = {"param_root_1": 1}
    cfgs = [{} for _ in range(2)]

    for cfg in cfgs:
        inserted = insert(cfg)
        assert expected == inserted
