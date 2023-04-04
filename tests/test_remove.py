import pytest
from randfig.transforms import Remove


@pytest.mark.parametrize('cfg,expected,keys', [
    [
        {"param_root_0": 0, "param_root_1": 1},
        {"param_root_0": 0},
        ["param_root_1"],
    ]
])
def test_insert(cfg, expected, keys):
    remove = Remove(keys=keys)
    removed = remove(cfg)
    assert removed == expected


def test_remove_two_times():
    remove = Remove(keys=["param_root_0"])
    expected = {"param_root_1": 1}
    cfgs = [{"param_root_0": 0, "param_root_1": 1} for _ in range(2)]

    for cfg in cfgs:
        removed = remove(cfg)
        assert expected == removed
