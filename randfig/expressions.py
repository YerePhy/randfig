import math
from numbers import Number
from typing import Mapping, Any, List, Optional, Callable
from randfig.utils import (
    add_uniform_jitter,
    search_divisor,
)


def pop(cfg: Mapping, key: str, element: int = 0) -> Any:
    """
    Pops an element of ``cfg[key]`` if
    its value is a ``List``.

    Args:
        cfg: ``dict``-like congifuration.
        key: a key of ``cfg`` which value is a ``List``
        element: which element to pop from the list.

    Returns:
        The poped element.

    Raises:
        TypeError: if the value associeted to
            ``cfg[key]`` is not a ``List``.
    """
    value_list = cfg[key]

    if not isinstance(value_list, List):
        raise TypeError(f"Expected a list but got {value_list} which is a {type(value_list)}.")

    return value_list.pop(element)


def rounding(cfg: Mapping, key: str, decimals: int) -> Any:
    """
    Round the value of ``cfg[key]`` if
    its value is a ``Number``.

    Args:
        cfg: ``dict``-like congifuration.
        key: a key of ``cfg`` which value is a ``Number``

    Returns:
        The rounded value.

    Raises:
        TypeError: if the value associeted to
            ``cfg[key]`` is not a ``Number``.
    """
    value_number = cfg[key]

    if not isinstance(value_number, Number):
        raise TypeError(f"Expected a numeric but got {value_number} which is a {type(value_number)}.")

    return round(value_number, decimals)


def min_threshold_from_resolution(cfg: Mapping, resolution_key: str, peak: Number,
    is_percentage: bool = True, sigmas: Number = 2, jitter: Optional[Number] = None) -> Number:
    """
    Computes a lower threshold (``lower_threshold``) assuming a gaussian distibution:

    .. code-block::

        FWHM_TO_STD = 1 / 2.355
        lower_threshold = peak * (1 - sigmas * FWHM_TO_STD * resolution)

    Args:
        cfg: ``dict``-like config having a resolution as a value.
        resolution_key: key whose value is the gaussian resolution (FWHM).
        peak: peak of the resolution curve.
        sigmas: how many sigmas from the peak will be the lower threshold.
        jitter: a uniform jitter with :py:func:`randfig.utils.add_uniform_jitter`.
            The value added is sampled from an uniform distribution with
            ``a = -jitter * peak``, ``b = jitter * peak``.

    Returns:
        Lower threshold.

    Raises:
        ValueError: if ``is_percentage`` is ``False`` but ``resolution > 1``.
    """
    FWHM_TO_STD = 1 / 2.355

    resolution = cfg[resolution_key]

    if is_percentage:
        resolution /= 100
    if not is_percentage and resolution > 1:
        raise ValueError(f"is_percentage is {is_percentage} but got a number bigger than 1: {resolution}")

    lower_threshold = peak * (1 - sigmas * FWHM_TO_STD * resolution)

    if jitter is not None:
        lower_threshold = add_uniform_jitter(lower_threshold, jitter, peak)

    return lower_threshold


def max_threshold_from_resolution(cfg: Mapping, resolution_key: str, peak: Number,
    is_percentage: bool = True, sigmas: Number = 2, jitter: Optional[Number] = None) -> Number:
    """
    Computes an upper threshold (``upper_threshold``) assuming a gaussian distibution:

    .. code-block::

        FWHM_TO_STD = 1 / 2.355
        lower_threshold = peak * (1 + sigmas * FWHM_TO_STD * resolution)

    Args:
        cfg: ``dict``-like config having a resolution as a value.
        resolution_key: key whose value is the gaussian resolution (FWHM).
        peak: peak of the resolution curve.
        sigmas: how many sigmas from the peak will be the upper threshold.
        jitter: a uniform jitter with :py:func:`randfig.utils.add_uniform_jitter`.
            The value added is sampled from an uniform distribution with
            ``a = -jitter * peak``, ``b = jitter * peak``.

    Returns:
        Upper threshold.

    Raises:
        ValueError: if ``is_percentage`` is ``False`` but ``resolution > 1``.
    """
    FWHM_TO_STD = 1 / 2.355

    resolution = cfg[resolution_key]

    if is_percentage:
        resolution /= 100
    if not is_percentage and resolution > 1:
        raise ValueError(f"is_percentage is {is_percentage} but got a number bigger than 1: {resolution}")

    upper_threshold = peak * (1 + sigmas * FWHM_TO_STD * resolution)

    if jitter is not None:
        upper_threshold = add_uniform_jitter(upper_threshold, jitter, peak)

    return upper_threshold


def division(cfg: Mapping, num_key: str, den_key: str, integer: bool = False) -> Number:
    """
    Computes division or integer division between
    the specified keys of ``cfg``.

    Args:
        cfg: ``dict``-like configuration.
        num_key: numerator key.
        den_key: denominator key.
        integer: whether to perform integer division or not.

    Returns:
        Division between the values of specified keys.

    Raises:
        TypeError: if ``cfg[num_key]`` or ``cfg[den_key]`` are not ``Number`` instances.
    """
    num = cfg[num_key]
    den = cfg[den_key]

    for name, var in [('num', num), ('den', den)]:
        if not isinstance(var, Number):
            raise TypeError(f"Expected {name} to be a number, got {type(var)}.")

    if integer:
        return int(num // den)

    return num / den


def division_by_num(cfg: Mapping, n_key: str, num: Number, integer: bool = False) -> Number:
    """
    Computes division or integer division between ``cfg[n_key]`` and ``num``.

    Args:
        cfg: ``dict``-like configuration.
        n_key: key whose value is the number to be devided.
        num: divisor.
        integer: whether to perform integer division or not.

    Returns:
        Division between ``cfg[n_key]`` and ``num``.

    Raises:
        TypeError: if ``cfg[n_key]`` or ``num`` are not ``Number`` instances.
    """
    n = cfg[n_key]

    for name, var in [('num', num), ('n', n)]:
        if not isinstance(var, Number):
            raise TypeError(f"Expected {name} to be a number, got {type(var)}.")

    if integer:
        return int(n // num)

    return n / num


def product(cfg, a_key: str, b_key: str) -> Number:
    """
    Computes ``cfg[a_key] * cfg[b_key]``.

    Args:
        a_key: key whose value is one factor of the product.
        b_key: key whose value is the other factor of the product.

    Returns:
        ``cfg[a_key] * cfg[b_key]``.

    Raises:
        TypeError: if ``cfg[a_key]`` or ``cfg[b_key]`` are not ``Number``.
    """
    a = cfg[a_key]
    b = cfg[b_key]

    for name, var in [('a', a), ('b', b)]:
        if not isinstance(var, Number):
            raise TypeError(f"Expected {name} to be a number, got {type(var)}.")

    return a * b


def product_by_num(cfg: Mapping, n_key: str, num: Number) -> Number:
    """
    Computes product between ``cfg[n_key]`` and ``num``.

    Args:
        cfg: ``dict``-like configuration.
        n_key: key whose value is the number to be multiplied.
        num: multiplier.

    Returns:
        Multiplication between ``cfg[n_key]`` and ``num``.

    Raises:
        TypeError: if ``cfg[n_key]`` or ``num`` are not ``Number`` instances.
    """
    n = cfg[n_key]

    for name, var in [('num', num), ('n', n)]:
        if not isinstance(var, Number):
            raise TypeError(f"Expected {name} to be a number, got {type(var)}.")

    return n * num


def get_regular_polygon_sides(cfg: Mapping, side_len_key: str, apothem_key: str) -> int:
    """
    Computes the sides of a regular polygon
    given side length and apothem.

    Args:
        cfg: ``dict``-like config.
        side_len_key: key whose value is the length of the polygon's side.
        apothem_key: key whose value is the length of the polygon's apothem.

    Returns:
        The number of sides of the regular polygon.

    Raises:
        TypeError: if ``cfg[side_len_key]`` or ``cfg[apothem_key]`` are not ``Number``.
    """
    side_len = cfg[side_len_key]
    apothem = cfg[apothem_key]

    for name, var in [('side_len', side_len), ('apothem', apothem)]:
        if not isinstance(var, Number):
            raise TypeError(f"Expected {name} to be a number, got {type(var)}.")

    return int(round(math.pi / math.atan(side_len / (2 * apothem)), 0))


def round_to_closest_even(cfg, key_n: str) -> int:
    """
    Rounds ``cfg[key_n]`` value to the closest even number.

    Args:
        cfg: ``dict``-like config.
        key_n: key whose value is a number to round up to the closest even.

    Returns:
        The closest even to ``cfg{key_n]``.

    Raises:
        TypeError: when ``cfg{key_n]`` is not a ``Number`` instance.
    """
    n = int(cfg[key_n])

    for name, var in [('n', n)]:
        if not isinstance(var, Number):
            raise TypeError(f"Expected {name} to be a number, got {type(var)}.")

    return 2 if n < 1 else int(math.ceil(n / 2.) * 2)


def get_regular_polygon_apothem(cfg: Mapping, side_len_key: str,
    n_sides_key: str) -> Number:
    """
    Computes the apothem of a regular polygon
    given its number and length of sides.

    Args:
        cfg: ``dict``-like config.
        side_len_key: key whose value is the length of the polygon's side.
        n_sides_key: key whose value is the number of sides.

    Returns:
        The apothem of the regular polygon

    Raises:
        TypeError: when ``cfg[side_len_key]`` is not a ``Number`` instance
    """
    side_len = cfg[side_len_key]
    n_sides = int(cfg[n_sides_key])

    if not isinstance(side_len, Number):
        raise TypeError(f"Expected {side_len} to be a number, got {type(side_len)}.")

    return side_len / (2 * math.tan(math.pi / n_sides))


def get_divisor(cfg: Mapping, key: str, search_divisor_kwargs: Mapping[str, Any]) -> int:
    """
    Search a divisor of ``cfg[key]`` based on :py:func:`randifg.utils.search_divisor`.

    Args:
        cfg: a ``dict``-like config.
        key: key whose value is an ``int`` or can be casted to ``int``.
        search_divisor_kwargs: kwargs for :py:func:`randifg.utils.search_divisor`,
            unless ``n`` which is ``cfg[key]``.

    Returns:
        A divisor of ``cfg[key]``.
    """
    n = int(cfg[key])
    return search_divisor(n, **search_divisor_kwargs)


def get_jittered_value(cfg: Mapping, key: str, p: Number) -> Number:
    """
    Stub.

    Args:
        cfg: a ``dict``-like config.
        key: key whose value is a ``Number`` to add jitter to.
        p: the amount of jitter to add, see :py:func:`randfig.utils.add_uniform_jitter`.

    Returns:
        Jittered value (``cfg[key] + uniform jitter``).

    Raises:
        TypeError: if ``cfg[key]`` is not a ``Number``.
    """
    value = cfg[key]

    if not isinstance(value, Number):
        raise TypeError(f"Expected a Number but got {value} which is {type(value)}")

    return add_uniform_jitter(value, value, p)


def pick_from_mapping(cfg: Mapping, key: str, mapping: Mapping[str, Any]) -> Any:
    """
    Returns ``mapping[cfg[key]]``.

    Args:
        cfg: a ``dict``-like config.
        key: key whose value will hash ``mapping``.
        mapping: the function returns ``mapping[cfg[key]]``.

    Returns:
        ``mapping[cfg[key]]``.
    """
    return mapping[cfg[key]]


def add(cfg: Mapping, key_a: str, key_b: str) -> Any:
    """
    Adds the values associated to ``key_a`` and ``key_b``
    from ``cfg``.

    Args:
        cfg: a ``dict``-like config.
        key_a: key whose value can be an operand to the ``+`` operator.
        key_b: key whose value can be an operand to the ``+`` operator.

    Returns:
        ``cfg[key_a] + cfg[key_b]``
    """
    return cfg[key_a] + cfg[key_b]


def add_value(cfg: Mapping, key: str, value: Any) -> Any:
    """
    Adds ``cfg[key]`` and ``value``.

    Args:
        cfg: a ``dict``-like config.
        key: key whose value can be an operand to the ``+`` operator.
        value: value that will be added to ``key``.

    Returns:
        ``cfg[key_a] + value``
    """
    return cfg[key] + value


def call(cfg: Mapping, key: str, fn: Callable) -> Any:
    """
    Does the folowing call ``fn(cfg[key])``.

    Args:
        cfg: a ``dict``-like config.
        key: key whose value will be argument to ``fn``.
        fn: a callable.

    Returns:
        ``fn(cfg[key])``
    """
    return fn(cfg[key])


def trunc(cfg: Mapping, key: str, decimals: int) -> Any:
    """
    Truncate the value of ``cfg[key]`` if
    its value is a ``Number``.

    Args:
        cfg: ``dict``-like congifuration.
        key: a key of ``cfg`` which value is a ``Number``

    Returns:
        The truncated value.

    Raises:
        TypeError: if the value associeted to
            ``cfg[key]`` is not a ``Number``.
    """
    value_number = cfg[key]

    if not isinstance(value_number, Number):
        raise TypeError(f"Expected a numeric but got {value_number} which is a {type(value_number)}.")

    return float(f"{value_number:.{decimals}f}")
