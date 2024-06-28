# -*- coding: utf-8 -*-

import numpy as np

from iclothing.const import PWL_DICT_MALE, PWL_DICT_FEMALE, BODY_NAMES, LOWER_LIMIT_DICT_MALE, LOWER_LIMIT_DICT_FEMALE


def log(X, a, b):
    return a * np.log(X) + b


def get_vr(met, va=0.1):
    vr = va
    if met < 1:
        vr = va
    if 1 <= met < 1.2:
        vr = 0.3 * (met-1) + va
    if 1.2 <= met < 2:
        vr = 0.25 * (met**2 + met - 2.4) + va
    if met >= 2:
        vr = 0.5 * met - 0.1 + va
    return max([vr, 0.2])


def _get_icl_i(icl, pwl, lower_limit):
    icl_i = pwl(np.array(icl))
    icl_i = np.maximum(icl_i, lower_limit)
    return np.round(icl_i, decimals=3)


def get_icl_dict(icl, sex, met=1.0):
    if sex == 'male':
        icl_dict = {body_name: _get_icl_i(icl, pwl, LOWER_LIMIT_DICT_MALE[body_name])
                    for body_name, pwl in PWL_DICT_MALE.items()}
    elif sex == 'female':
        icl_dict = {body_name: _get_icl_i(icl, pwl, LOWER_LIMIT_DICT_FEMALE[body_name])
                    for body_name, pwl in PWL_DICT_FEMALE.items()}
    else:
        raise ValueError

    return icl_dict


if __name__ == '__main__':
    import pandas as pd
    icl = [0.3, 0.37, 0.5, 1]
    icli = get_icl_dict(icl, 'female', 1)
    icli = pd.DataFrame.from_dict(icli, orient='index', columns=icl)
    print(icli)
