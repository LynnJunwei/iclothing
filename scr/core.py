# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from scr.const import body_part_list, pwl_coeff_dict, lower_limit_dict_male, lower_limit_dict_female, log_coeff_dict


def pwl1(X, k, b):
    return k * X + b


def pwl2(X, k1, k2, b1, b2, x1):
    return np.piecewise(X, [X < x1, X >= x1],
                        [lambda x: k1 * x + b1, lambda x: k2 * x + b2])


def pwl3(X, k1, k2, k3, b1, b2, b3, x1, x2):
    return np.piecewise(X, [X < x1, (X >= x1) & (X < x2), X >= x2],
                        [lambda x: k1 * x + b1, lambda x: k2 * x + b2, lambda x: k3 * x + b3])


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


def get_icli(icl, sex, met=1.0):

    icl_head = pwl1(icl, pwl_coeff_dict['head']['k'], pwl_coeff_dict['head']['b'])
    icl_chest = pwl1(icl, pwl_coeff_dict['chest-{}'.format(sex)]['k'], pwl_coeff_dict['chest-{}'.format(sex)]['b'])
    icl_back = pwl1(icl, pwl_coeff_dict['back-{}'.format(sex)]['k'], pwl_coeff_dict['back-{}'.format(sex)]['b'])
    icl_pelvis = pwl1(icl, pwl_coeff_dict['pelvis-{}'.format(sex)]['k'], pwl_coeff_dict['pelvis-{}'.format(sex)]['b'])
    icl_shoulder = pwl1(icl, pwl_coeff_dict['shoulder-{}'.format(sex)]['k'], pwl_coeff_dict['shoulder-{}'.format(sex)]['b'])
    icl_arm = pwl1(icl, pwl_coeff_dict['arm-{}'.format(sex)]['k'], pwl_coeff_dict['arm-{}'.format(sex)]['b'])
    icl_hand = pwl1(icl, pwl_coeff_dict['hand']['k'], pwl_coeff_dict['hand']['b'])
    icl_thigh = pwl1(icl, pwl_coeff_dict['thigh']['k'], pwl_coeff_dict['thigh']['b'])
    icl_leg = pwl2(icl, pwl_coeff_dict['leg']['k1'], pwl_coeff_dict['leg']['k2'],
                   pwl_coeff_dict['leg']['b1'], pwl_coeff_dict['leg']['b2'], pwl_coeff_dict['leg']['x1'])
    icl_foot = pwl3(icl, pwl_coeff_dict['foot']['k1'], pwl_coeff_dict['foot']['k2'], pwl_coeff_dict['foot']['k3'],
                    pwl_coeff_dict['foot']['b1'], pwl_coeff_dict['foot']['b2'], pwl_coeff_dict['foot']['b3'],
                    pwl_coeff_dict['foot']['x1'], pwl_coeff_dict['foot']['x2'])

    icli_ser = pd.Series({'head': icl_head, 'chest': icl_chest, 'back': icl_back, 'pelvis': icl_pelvis,
                          'shoulder': icl_shoulder, 'arm': icl_arm, 'hand': icl_hand, 'thigh': icl_thigh,
                          'leg': icl_leg, 'foot': icl_foot})
    icli_min_ser = pd.Series(lower_limit_dict_female) if sex == 'female' else pd.Series(lower_limit_dict_male)

    icli_ser = pd.concat([icli_ser, icli_min_ser], axis=1).max(axis=1)
    icli_ser['overall'] = icl

    log_coeff_df = pd.DataFrame(log_coeff_dict).T
    corr_ser = log(get_vr(met), log_coeff_df['a'], log_coeff_df['b'])

    icli_ser = icli_ser * corr_ser

    return icli_ser.astype(float).round(3)


if __name__ == '__main__':
    icli = get_icli(0.37, 'female', 1)
    print(icli)
