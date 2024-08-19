#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from typing import Literal
from types import FunctionType

from iclothing.const import PWL_DICT_MALE, PWL_DICT_FEMALE, LOWER_LIMIT_DICT_MALE, LOWER_LIMIT_DICT_FEMALE, WIND_CORR_DICT


def get_vr(met: float, va: float = 0.1) -> float:
    """
    Calculate relative air velocity.

    Relative air velocity is the sum of absolute air velocity and the walking speed, following the equation:

    .. math:: v_r = v_a + v_w

    For low metabolic rate (met < 1) which indicates behaviors without body movement, the walking speed is equal to 0:

    .. math:: v_w = 0

    For less-defined activities (e.g. conveyor belt work) (1 <= met < 1.2), the walking speed could be calculated using:

    .. math:: v_w= 0.3 \\times (met-1)

    For walking (met >= 2), the walking speed could be estimated using:

    .. math:: v_w = 0.5 \\times met - 0.1

    For other activities (1.2 <= met < 2), the walking speed could be calculated by interpolation of walking speeds for
    less-defined activities and walking:

    .. math:: v_w = 0.25 \\times (met^2 + met - 2.4)

    Args:
        met: A number of metabolic rate (in met).
        va: A number of absolute air velocity (in m/s).

    Returns:
        A number of relative air velocity (in m/s).
    """
    vr = va
    if met < 1:
        vr = va
    if 1 <= met < 1.2:
        vr = 0.3 * (met - 1) + va
    if 1.2 <= met < 2:
        vr = 0.25 * (met ** 2 + met - 2.4) + va
    if met >= 2:
        vr = 0.5 * met - 0.1 + va
    return vr


def _get_icl_i(icl: list | np.ndarray | float,
               pwl: FunctionType,
               lower_limit: float) -> np.ndarray | float:
    """
    Get local clothing insulation for a specific body part.

    Args:
        icl: A number or a list of overall clothing insulation (in clo).
        pwl: A piecewise linear function for a specific body part.
        lower_limit: A number of lower limit of local clothing insulation for a specific body part (in clo).

    Returns:
        A number or a list of local clothing insulation for a specific body part (in clo).
    """
    icl_i = pwl(np.array(icl))
    icl_i = np.maximum(icl_i, lower_limit)
    return np.round(icl_i, decimals=3)


def get_icl_dict(icl: list | np.ndarray | float,
                 sex: Literal["male", "female"],
                 met: float = 1.0,
                 va: float = 0.1) -> dict:
    """
    Get local clothing insulation for each body part.

    The calculation models are based on the following papers:

    Args:
        icl: A number or a list of overall clothing insulation (in clo).
        sex: Sex of human object. The value should be 'male' or 'female'. Default is 'male'.
        met: A number of Metabolic rate of human object (in met). Default is 1.0 met.
        va: A number of absolute air velocity (in m/s). Default is 0.1 m/s.

    Returns:
        A dictionary of local clothing insulation for each body part.

    Examples:
        >>> icl = 0.3
        >>> icli = get_icl_dict(icl=icl, sex="male", met=1)
        >>> print(icli)
        {'Head': 0.13, 'Neck': 0.0, 'Chest': 0.35, 'Back': 0.27, 'Pelvis': 0.91, 'LShoulder': 0.0, 'LArm': 0.0, 'LHand': 0.0, 'RShoulder': 0.0, 'RArm': 0.0, 'RHand': 0.0, 'LThigh': 0.48, 'LLeg': 0.043, 'LFoot': 1.342, 'RThigh': 0.48, 'RLeg': 0.043, 'RFoot': 1.342}
    """
    if sex == 'male':
        icl_dict = {body_name: _get_icl_i(icl, pwl, LOWER_LIMIT_DICT_MALE[body_name])
                    for body_name, pwl in PWL_DICT_MALE.items()}
    elif sex == 'female':
        icl_dict = {body_name: _get_icl_i(icl, pwl, LOWER_LIMIT_DICT_FEMALE[body_name])
                    for body_name, pwl in PWL_DICT_FEMALE.items()}
    else:
        raise ValueError

    vr = get_vr(met, va)
    if vr > 0.2:
        icl_dict = {body_name: (icl_i * WIND_CORR_DICT[body_name](vr))
                    for body_name, icl_i in icl_dict.items()}

    return {body_name: icl_i.astype(type('float', (float,), {})) for body_name, icl_i in icl_dict.items()}


if __name__ == '__main__':
    pass
