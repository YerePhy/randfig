import math
from numbers import Number
from typing import Mapping, Any, List, Optional
from randfig.utils import add_uniform_jitter


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
        num_key: numberator key.
        den_key: denominator key.
        integer: whether to perform integer division or not.

    Returns:
        Division between the values of specified keys.
    """
    num = cfg[num_key]
    den = cfg[den_key]

    if integer:
        return int(num // den)

    return num / den


def product(cfg, a_key: str, b_key: str) -> Number:
    """
    Computes ``cfg[a_key] * cfg[b_key]``.

    Args:
        a_key:
        b_key:

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
    Stub.

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
