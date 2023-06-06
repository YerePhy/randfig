import math
import operator
import random
import warnings
from bisect import bisect_left, bisect_right
from collections import defaultdict
from functools import reduce
from numbers import Number
from typing import (
    Mapping,
    Sequence,
    Any,
    DefaultDict,
    Dict,
    List,
    Union,
    Optional,
    Iterable
)


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
    Add jitter to ``value`` based on a fraction, ``p`` of ``reference``:

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


def get_divisors(n: Number) -> List[int]:
    """
    Get the divisors of a number.

    Args:
        n: taget number (internally casted to ``int``).

    Returns:
        The divisors of the input number.

    Raises:
        ValueError: When ``n==0``.
    """
    num = int(n)

    if num == 0:
        raise ValueError("For convinience 0 is not a valid number.")
    if num == 1:
        return [num]

    factors = [1]

    for t in range(2, math.ceil((num // 2) + 1)):
        if num % t == 0:
            factors.append(int(t))

    factors.append(num)

    return factors


def find_divisor(n: Number, divisors: Sequence[Number]) -> Union[int, None]:
    """
    Sequentially, tries to find each item of ``divisors`` in the
    divisors of ``n``. The first item of ``divisors`` that matches
    a divisor of ``n`` is returned. If none of ``divisors`` is found
    in the divisors of ``n``, ``None`` is returned.

    Args:
        n: number to find the divisor of (internally casted to ``int``)
        divisors: seuquence of divisors to find (internally casted to ``int``).

    Returns:
        The first item of divisors that matches a divisor of ``n``.

    Raises:
        ValueError: If ``n==0``.
        ValueError: If ``divisors`` is empty after removing the zeros.
    """
    n_ = int(n)
    divisors_ = list(dict.fromkeys([int(m) for m in divisors]))

    if n_ == 0:
        raise ValueError("For convinience 0 is not a valid number.")
    if 0 in divisors_:
        warnings.warn("Excluding 0 from divisors")
        divisors_ = [i for i in divisors_ if i != 0]
    if not divisors_:
        raise ValueError("Empty list of divisors to find after excluding 0.")

    real_divisors = get_divisors(n_)

    for div in divisors_:
        if div in real_divisors:
            return div


def find_immediately_lower_divisor(n: Number, threshold: Number) -> int:
    """
    Find the divisor of ``n``  immediately smaller than
    a given threshold.

    Args:
        n: the number to find the divisor of (internally casted to ``int``).
        threshold: the divisor returned is the biggest
            divisor of ``n`` smaller than this threshold
            (internally casted to ``int``).

    Returns:
        The biggest divisor of ``n`` smaller than ``threshold``.

    Raises:
        ValueError: if ``threshold_==0``.
    """
    n_ = int(n)
    threshold_ = int(threshold)

    if threshold_ == 0:
        raise ValueError("There is no divisors equal or smaller than 0.")

    divisors_ = get_divisors(n_)

    return divisors_[bisect_left(divisors_, threshold_)-1]


def find_immediately_upper_divisor(n: Number, threshold: Number) -> int:
    """
    Find the divisor of ``n``  immediately bigger than
    a given threshold.

    Args:
        n: the number to find the divisor of (internally casted to ``int``).
        threshold: the divisor returned is the smallest
            divisor of ``n`` bigger than this threshold
            (internally casted to ``int``).

    Returns:
        The smallest divisor of ``n`` bigger than ``threshold``.

    Raises:
        ValueError: if ``threshold_==0``.
    """
    n_ = int(n)
    threshold_ = int(threshold)

    if threshold_ == 0:
        raise ValueError("There is no divisors equal or smaller than 0.")

    # this will raise ValueError if n_ is 0
    divisors_ = get_divisors(n_)

    if threshold_ >= n_:
        warnings.warn(f"Threshold {threshold_} is bigger than n {n_}, returning n.")
        return n_


    return divisors_[bisect_right(divisors_, threshold_)]


def search_divisor(n: Number, not_found_strategy: str, threshold: Number, divisors: Optional[Sequence[Number]] = None) -> int:
    """
    Checks sequentially if the items of ``divisors``
    are actually divisors of ``n`` the first match
    is returned (see :py:func:`randfig.utils.find_divisor`).
    If there is no match, a divisor can be found using
    one of the following strategies:

    * ``not_found_strategy=="min"``: the smallest
        divisor bigger than ``threshold`` is returned.
        See :py:func:`find_immediately_lower_divisor`.
    * ``not_found_strategy=="max"``: the biggest
        divisor smaller than ``threshold`` is returned.
        See :py:func:`find_immediately_upper_divisor`.

    .. exec_code::
        
        # --- hide: start ---
        from randfig.utils import search_divisor
        # --- hide: stop ---

        # divisors of 45: 1, 3, 5, 9, 15.

        # no ``divisors`` provided and "min" strategy
        n=45
        not_found_strategy = "min"
        threshold = 7
        min_strategy_divisor = search_divisor(n, not_found_strategy, threshold)
        
        # --- hide: start ---
        print(f"Divisor found with min strategy: {min_strategy_divisor}")
        # --- hide: stop ---

        # no ``divisors`` provided and "max" strategy
        n=45
        not_found_strategy = "max"
        threshold = 7
        max_strategy_divisor = search_divisor(n, not_found_strategy, threshold)
        
        # --- hide: start ---
        print(f"Divisor found with max strategy: {max_strategy_divisor}")
        # --- hide: stop ---

        # ``divisors`` provided and "max" strategy (strategy not used in this case).
        n=45
        divisors = [8, 15]
        no_strategy_divisor = search_divisor(n, not_found_strategy, threshold, divisors)
        
        # --- hide: start ---
        print(f"Divisor found with divisors provided: {no_strategy_divisor}")
        # --- hide: stop ---

    Args:
        n: number to find the divisor of.
        not_found_strategy: one of ``"min"``, ``"max"``.
            Strategy to follow if there is no match.
        divisors: the items of this sequence
            are matched sequentially against the divisors of
            ``n`` the first match is returned. If ``None``
            the selected strategy is directly applied.

    Returns:
        A divisor of ``n``.

    Raises:
        ValueError: if ``not_found_strategy`` is not ``"min"`` or ``"max"``.
    """
    if divisors is not None:
        if div_ := find_divisor(n, divisors):
            return div_

    if not_found_strategy == "min":
        return find_immediately_lower_divisor(n, threshold)
    elif not_found_strategy == "max":
        return find_immediately_upper_divisor(n, threshold)
    else:
        raise ValueError(f"not_found_strategy={not_found_strategy} is not a valid strategy, available strategies are 'min' and 'max'")


def unpack(cfg: Mapping[str, Any], key: str, new_keys: Sequence[str], remove: bool = False) -> Mapping:
    """
    Stub.

    Args:
        cfg: a ``dict``-like config.
        key: key whose value will be unpacked
        new_keys: a key for each value associated to ``key``

    Returns:
        Input config with new key, value pairs. These new
        keys are ``new_keys`` and the associated values
        are provided by ``cfg[key]``.

    Raises:
        TypeError: if ``cfg[key]`` is not an ``Iterable``.
        TypeError: if ``cfg[key]`` and ``new_keys`` have different lengths.
        ValueError: if any of the keys in ``new_keys`` already exists in ``cfg``.
    """
    unpacking = cfg[key]

    if not isinstance(unpacking, Iterable):
        raise TypeError(f"Got {type(unpacking)}, expected Iterable")

    unpacking_len = len(unpacking)
    new_keys_len = len(new_keys)

    if new_keys_len != unpacking_len:
        raise ValueError(f"new_keys has len: {new_keys_len} and cfg[key] has len: {unpacking_len}.")

    for nk, val in zip(new_keys, unpacking):
        if nk not in cfg.keys():
            cfg.update({nk: val})
        else:
            raise ValueError(f"key: {nk} already exists in cfg.")

    if remove:
        cfg.pop(key, None)

    return cfg
