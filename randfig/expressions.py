from numbers import Number
from typing import Mapping, Any, List


def pop(cfg: Mapping, key: str, element: int = 0) -> Any:
    """
    Pops an element of ``cfg[key]`` if
    its value is a ``List``. It is intended to use
    it with :py:func:`randfig.formula.Formula` and ``_partial_: true``
    in facebook-hydra configs.

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
    its value is a ``Number``. It is intended to use
    it with :py:func:`randfig.formula.Formula` and ``_partial_: true``
    in facebook-hydra configs.

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
    is_percentage: bool = True, sigmas: Number = 2) -> Number:
    """
    Computes a lower threshold (``lower_threshold``) assuming a gaussian distibution:

    .. code-block::

        FWHM_TO_STD = 1 / 2.355
        lower_threshold = peak * (1 - sigmas * FWHM_TO_STD * resolution)

    It is intended to use it with :py:func:`randfig.formula.Formula` and ``_partial_: true``
    in facebook-hydra configs.

    Args:
        cfg: ``dict``-like config having a resolution as a value.
        resolution_key: key whose value is the gaussian resolution (FWHM).
        peak: peak of the resolution curve.
        sigmas: how many sigmas from the peak will be the lower threshold.

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

    return lower_threshold


def max_threshold_from_resolution(cfg: Mapping, resolution_key: str, peak: Number,
    is_percentage: bool = True, sigmas: Number = 2) -> Number:
    """
    Computes an upper threshold (``upper_threshold``) assuming a gaussian distibution:

    .. code-block::

        FWHM_TO_STD = 1 / 2.355
        lower_threshold = peak * (1 + sigmas * FWHM_TO_STD * resolution)

    It is intended to use it with :py:func:`randfig.formula.Formula` and ``_partial_: true``
    in facebook-hydra configs.

    Args:
        cfg: ``dict``-like config having a resolution as a value.
        resolution_key: key whose value is the gaussian resolution (FWHM).
        peak: peak of the resolution curve.
        sigmas: how many sigmas from the peak will be the upper threshold.

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

    return upper_threshold
