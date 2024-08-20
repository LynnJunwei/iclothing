#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def _get_func(k_b_dict):
    func_dict = {}
    for body_name, k_b_list in k_b_dict.items():
        func_list = [lambda x, k=k_b[0], b=k_b[1]: k * x + b for k_b in k_b_list]
        func_dict[body_name] = func_list
    return func_dict


def _get_cond_func(break_dict):
    cond_dict = {}
    for body_name, break_list in break_dict.items():
        if len(break_list) == 1 and break_list[0] is None:
            cond_list = [lambda x: np.ones_like(x)]
        else:
            breaks_lower = [float('-inf')] + break_list
            breaks_upper = break_list + [float('inf')]
            cond_list = [lambda x, lower=break_lower, upper=break_upper: (lower <= x) & (x < upper)
                         for break_lower, break_upper in zip(breaks_lower, breaks_upper)]
        cond_dict[body_name] = cond_list
    return cond_dict


def _get_pwl(func_dict, cond_func_dict):
    pwl_dict = {}
    for body_name in BODY_NAMES:
        func_list = func_dict[body_name]
        cond_func_list = cond_func_dict[body_name]

        def pwl(x, _cond_func_list=cond_func_list, _func_list=func_list):
            return np.piecewise(x, [cond_func(x) for cond_func in _cond_func_list], _func_list)

        pwl_dict[body_name] = pwl
    return pwl_dict


def _get_wind_corr_func(a_b_dict):
    wind_corr_dict = {}
    for body_name, a_b in a_b_dict.items():
        def wind_corr_func(x, a=a_b[0], b=a_b[1]):
            return a * np.log(x) + b

        wind_corr_dict[body_name] = wind_corr_func
    return wind_corr_dict


BODY_NAMES: list = [
    "Head", "Neck", "Chest", "Back", "Pelvis",
    "LShoulder", "LArm", "LHand",
    "RShoulder", "RArm", "RHand",
    "LThigh", "LLeg", "LFoot",
    "RThigh", "RLeg", "RFoot"]
"""List of body names."""

_K_B_DICT_MALE: dict = {  # [(k1, b1), (k2, b2), ...]
    "Head": [(0, 0.13)],
    "Neck": [(0, 0)],
    "Chest": [(3.212, -0.962)],
    "Back": [(1.726, -0.276)],
    "Pelvis": [(0.977, 0.591)],
    "LShoulder": [(1.941, -0.632)],
    "LArm": [(1.580, -0.658)],
    "LHand": [(0, 0)],
    "RShoulder": [(1.941, -0.632)],
    "RArm": [(1.580, -0.658)],
    "RHand": [(0, 0)],
    "LThigh": [(0.684, 0.269)],
    "LLeg": [(2.656, -0.754), (0.570, 0.226)],
    "LFoot": [(4.473, 0), (0.117, 1.326), (1.246, -0.236)],
    "RThigh": [(0.684, 0.269)],
    "RLeg": [(2.656, -0.754), (0.570, 0.226)],
    "RFoot": [(4.473, 0), (0.117, 1.326), (1.246, -0.236)]
}
"""Dictionary of k and b values of piecewise functions for male."""

_K_B_DICT_FEMALE: dict = {  # [(k1, b1), (k2, b2), ...]
    "Head": [(0, 0.13)],
    "Neck": [(0, 0)],
    "Chest": [(3.120, -0.748)],
    "Back": [(1.671, -0.263)],
    "Pelvis": [(0.986, 0.571)],
    "LShoulder": [(2.030, -0.817)],
    "LArm": [(1.562, -0.700)],
    "LHand": [(0, 0)],
    "RShoulder": [(2.030, -0.817)],
    "RArm": [(1.562, -0.700)],
    "RHand": [(0, 0)],
    "LThigh": [(0.684, 0.269)],
    "LLeg": [(2.656, -0.754), (0.570, 0.226)],
    "LFoot": [(4.473, 0), (0.117, 1.326), (1.246, -0.236)],
    "RThigh": [(0.684, 0.269)],
    "RLeg": [(2.656, -0.754), (0.570, 0.226)],
    "RFoot": [(4.473, 0), (0.117, 1.326), (1.246, -0.236)]
}
"""Dictionary of k and b values of piecewise functions for female."""

_FUNC_DICT_MALE: dict = _get_func(_K_B_DICT_MALE)
"""Dictionary of functions for piecewise functions for male."""

_FUNC_DICT_FEMALE: dict = _get_func(_K_B_DICT_FEMALE)
"""Dictionary of functions for piecewise functions for female."""

_BREAK_DICT: dict = {
    "Head": [None],
    "Neck": [None],
    "Chest": [None],
    "Back": [None],
    "Pelvis": [None],
    "LShoulder": [None],
    "LArm": [None],
    "LHand": [None],
    "RShoulder": [None],
    "RArm": [None],
    "RHand": [None],
    "LThigh": [None],
    "LLeg": [0.470],
    "LFoot": [0.304, 1.382],
    "RThigh": [None],
    "RLeg": [0.470],
    "RFoot": [0.304, 1.382]
}
"""Dictionary of break points for piecewise functions."""

_COND_FUNC_DICT: dict = _get_cond_func(_BREAK_DICT)
"""Dictionary of conditional functions for piecewise functions."""

PWL_DICT_MALE: dict = _get_pwl(_FUNC_DICT_MALE, _COND_FUNC_DICT)
"""
Dictionary of piecewise functions for male.

Examples:
    >>> from iclothing.const import PWL_DICT_MALE
    >>> icl_dict = {body_name: pwl(0.3) for body_name, pwl in PWL_DICT_MALE.items()}
"""

PWL_DICT_FEMALE: dict = _get_pwl(_FUNC_DICT_FEMALE, _COND_FUNC_DICT)
"""
Dictionary of piecewise functions for female.

Examples:
    >>> from iclothing.const import PWL_DICT_FEMALE
    >>> icl_dict = {body_name: pwl(0.3) for body_name, pwl in PWL_DICT_MALE.items()}
"""

LOWER_LIMIT_DICT_MALE: dict = {
    "Head": 0,
    "Neck": 0,
    "Chest": 0.35,
    "Back": 0.27,
    "Pelvis": 0.91,
    "LShoulder": 0,
    "LArm": 0,
    "LHand": 0,
    "RShoulder": 0,
    "RArm": 0,
    "RHand": 0,
    "LThigh": 0.48,
    "LLeg": 0,
    "LFoot": 0.41,
    "RThigh": 0.48,
    "RLeg": 0,
    "RFoot": 0.41
}
"""Dictionary of lower limits of local clothing insulation for male."""

LOWER_LIMIT_DICT_FEMALE: dict = {
    "Head": 0,
    "Neck": 0,
    "Chest": 0.57,
    "Back": 0.27,
    "Pelvis": 0.91,
    "LShoulder": 0,
    "LArm": 0,
    "LHand": 0,
    "RShoulder": 0,
    "RArm": 0,
    "RHand": 0,
    "LThigh": 0.48,
    "LLeg": 0,
    "LFoot": 0.41,
    "RThigh": 0.48,
    "RLeg": 0,
    "RFoot": 0.41
}
"""Dictionary of lower limits of local clothing insulation for female."""

_A_B_DICT: dict = {
    "Head": (-0.233, 0.625),
    "Neck": (0, 1),
    "Chest": (-0.120, 0.807),
    "Back": (-0.089, 0.856),
    "Pelvis": (-0.092, 0.852),
    "LShoulder": (-0.137, 0.780),
    "LArm": (-0.128, 0.794),
    "LHand": (0, 1),
    "RShoulder": (-0.137, 0.780),
    "RArm": (-0.128, 0.794),
    "RHand": (0, 1),
    "LThigh": (-0.116, 0.814),
    "LLeg": (-0.089, 0.857),
    "LFoot": (-0.054, 0.913),
    "RThigh": (-0.116, 0.814),
    "RLeg": (-0.089, 0.857),
    "RFoot": (-0.054, 0.913)
}
"""Dictionary of a and b values of wind correction functions."""

WIND_CORR_DICT: dict = _get_wind_corr_func(_A_B_DICT)
"""
Dictionary of wind correction functions.

Examples:
    >>> from iclothing.const import WIND_CORR_DICT
    >>> vr = 0.3
    >>> icl_dict = get_icl_dict(0.3)
    >>> icl_dict_corr = {body_name: (icl_i * WIND_CORR_DICT[body_name](vr) for body_name, icl_i in icl_dict.items()}
"""

BSA_DICT: dict = {
    "Head": 0.100,
    "Neck": 0,
    "Chest": 0.144,
    "Back": 0.133,
    "Pelvis": 0.182,
    "LShoulder": 0.073,
    "LArm": 0.052,
    "LHand": 0.0375,
    "RShoulder": 0.073,
    "RArm": 0.052,
    "RHand": 0.0375,
    "LThigh": 0.1625,
    "LLeg": 0.089,
    "LFoot": 0.042,
    "RThigh": 0.1625,
    "RLeg": 0.089,
    "RFoot": 0.042
}
"""Dictionary of body surface area (in m\\ :sup:`2`)."""

BSA_TOTAL: float = sum(list(BSA_DICT.values()))
"""Total body surface area (in m\\ :sup:`2`)."""

BSA_RATIO_DICT: dict = {body_name: np.round(bsa / BSA_TOTAL, decimals=3).astype(type('float', (float,), {}))
                        for body_name, bsa in BSA_DICT.items()}
"""Dictionary of body surface area ratio."""

if __name__ == '__main__':
    pass
