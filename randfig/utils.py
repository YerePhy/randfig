import operator
import random
from collections import defaultdict
from functools import reduce
from numbers import Number
from typing import Mapping, Sequence, Any, DefaultDict, Dict


def get_nested_value(mapping: Mapping, map_list: Sequence[str]) -> Any:
    """
    Get the value of nested keys.

    .. exec_code::

        # --- hide: start ---
        from randfig.utils import get_nested_value
        # --- hide: stop ---

        nested = {"param_root": {"param_nested": {"param_1": 1, "param_2": 2}}}
        nested_val = get_nested_value(nested, ["param_root", "param_nested"])

        # --- hide: start ---
        print(f"nested_val: {nested_val}")
        # --- hide: stop ---

    Args:
       mapping: an object following ``typing.Mapping`` interface.
       map_list: a sequence of nested keys.

    Returns:
        The value of the last key specified by ``map_list``.
    """
    return reduce(operator.getitem, map_list, mapping)


def mapping_to_defaultdict(mapping: Mapping[str, Any]) -> DefaultDict[str, Any]:
    """
    Convert a nested ``typing.Mapping`` to
    a nested ``typing.DefaultDict`` recursively.

    Args:
        mapping: nested ``typing.Mapping``.

    Returns:
        Nested ``typing.DefaultDict``.
    """
    if isinstance(mapping, Mapping):
        mapping = defaultdict(defaultdict, {k: mapping_to_defaultdict(v) for k, v in mapping.items()})
    return mapping


def mapping_to_dict(mapping: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Convert a nested ``typing.Mapping`` to
    a nested ``typing.Dict`` recursively.

    Args:
        mapping: nested ``typing.Mapping``.

    Returns:
        Nested ``typing.Dict``.
    """
    if isinstance(mapping, Mapping):
        mapping = {k: mapping_to_dict(v) for k, v in mapping.items()}
    return mapping


def insert_nested_key(cfg: Dict[str, Dict], keys: Sequence[str], value: Any) -> None:
    """
    Insert a key, value pair or update a value
    of a nested ``Mapping``.

    .. exec_code::

        # --- hide: start ---
        from randfig.utils import insert_nested_key
        # --- hide: stop ---

        cfg = {"param_root_0": {"param_00": "value_00", "param_01": "value_01"}}
        insert_nested_key(cfg, ["param_root_0", "param_02"], "value_02")

        # --- hide: start ---
        print(f"cfg: {cfg}")
        # --- hide: stop ---

    Args:
        cfg: nested ``Mapping``.
        keys: sequence of nested keys where ``value`` will be inserted.
        value: value to insert.

    Raises:
        TypeError: if one of the values of the nested keys is not a ``Mapping``.
    """
    if isinstance(cfg, Mapping):
        first_key = keys[0]
        remaining_keys = keys[1:]

        if not remaining_keys:
            cfg[first_key] = value
        else:
            insert_nested_key(cfg[first_key], remaining_keys, value)
    else:
        raise TypeError(f"Got: {cfg} for one of the nested values, which is {type(cfg)}, expected a``Mapping``.")


def remove_nested_key(cfg: Dict[str, Dict], keys: Sequence[str]) -> None:
    """
    Remove a key, value pair of a nested ``Mapping``.

    .. exec_code::

        # --- hide: start ---
        from randfig.utils import remove_nested_key
        # --- hide: stop ---

        cfg = {"param_root_0": {"param_00": "value_00", "param_01": "value_01"}}
        remove_nested_key(cfg, ["param_root_0", "param_01"])

        # --- hide: start ---
        print(f"cfg: {cfg}")
        # --- hide: stop ---

    Args:
        cfg: nested ``Mapping``.
        keys: sequence of nested keys, the last one will be removed.

    Raises:
        TypeError: if one of the values of the nested keys is not a ``Mapping``.
    """
    if isinstance(cfg, Mapping):
        first_key = keys[0]
        remaining_keys = keys[1:]

        if not remaining_keys:
            cfg.pop(first_key)
        else:
            remove_nested_key(cfg[first_key], remaining_keys)
    else:
        raise TypeError(f"Got: {cfg} for one of the nested values, which is {type(cfg)}, expected a``Mapping``.")


def add_uniform_jitter(value: Number, p: Number, reference: Number) -> Number:
    """
    Ass jitter to ``value`` based on a fraction, ``p`` of ``reference``:

    .. code-block::

        value = value + random.uniform(-p * reference, p * reference)

    Args:
        value: jitted will be added to this argument.
        p: fraction of ``reference`` that will be added to ``value``.
        reference: the jitter added to ``value`` is sampled from an uniform
            distribution with range ``a = -p * reference``, ``b = p * reference``.

    Returns:
        Jittered value.

    Raises:
        TypeError: if any of the arguments is not a ``Number`` instance.
    """
    for (name, num) in [('value', value), ('p', p), ('reference', reference)]:
        if not isinstance(num, Number):
            raise TypeError(f"Expected {name} to be a number but got {type(num)}.")

    effective_reference = p * reference

    return value + random.uniform(-effective_reference, effective_reference)
