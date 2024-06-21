# -*- coding: utf-8 -*-

body_part_list = ['head', 'chest', 'back', 'pelvis', 'shoulder', 'arm', 'hand', 'thigh', 'leg', 'foot']

pwl_coeff_dict = {
    'head': {'k': 0, 'b': 0.13},
    'chest-male': {'k': 3.212, 'b': -0.962},
    'chest-female': {'k': 3.120, 'b': -0.748},
    'back-male': {'k': 1.726, 'b': -0.276},
    'back-female': {'k': 1.671, 'b': -0.263},
    'pelvis-male': {'k': 0.977, 'b': 0.591},
    'pelvis-female': {'k': 0.986, 'b': 0.571},
    'shoulder-male': {'k': 1.941, 'b': -0.632},
    'shoulder-female': {'k': 2.030, 'b': -0.817},
    'arm-male': {'k': 1.580, 'b': -0.658},
    'arm-female': {'k': 1.562, 'b': -0.700},
    'hand': {'k': 0, 'b': 0},

    'thigh': {'k': 0.684, 'b': 0.269},
    'leg': {'k1': 2.656, 'b1': -0.754, 'k2': 0.570, 'b2': 0.226, 'x1': 0.470},
    'foot': {'k1': 4.473, 'b1': 0, 'k2': 0.117, 'b2': 1.326, 'k3': 1.246, 'b3': -0.236, 'x1': 0.304, 'x2': 1.382}
}

lower_limit_dict_female = {
    'head': 0,
    'chest': 0.57,
    'back': 0.27,
    'pelvis': 0.91,
    'shoulder': 0.42,
    'arm': 0,
    'hand': 0,
    'thigh': 0.48,
    'leg': 0,
    'foot': 0.41
}


lower_limit_dict_male = {
    'head': 0,
    'chest': 0.35,
    'back': 0.27,
    'pelvis': 0.91,
    'shoulder': 0,
    'arm': 0,
    'hand': 0,
    'thigh': 0.48,
    'leg': 0,
    'foot': 0.41
}

log_coeff_dict = {
    'head': {'a': -0.233, 'b': 0.625},
    'chest': {'a': -0.120, 'b': 0.807},
    'back': {'a': -0.089, 'b': 0.856},
    'pelvis': {'a': -0.092, 'b': 0.852},
    'shoulder': {'a': -0.137, 'b': 0.780},
    'arm': {'a': -0.128, 'b': 0.794},
    'hand': {'a': 0, 'b': 1},
    'thigh': {'a': -0.116, 'b': 0.814},
    'leg': {'a': -0.089, 'b': 0.857},
    'foot': {'a': -0.054, 'b': 0.913},
    'overall': {'a': -0.116, 'b': 0.813}
}

bsa_coeff_dict = {
    'head': 0.068,
    'chest': 0.098,
    'back': 0.090,
    'pelvis': 0.124,
    'shoulder': 0.099,
    'arm': 0.071,
    'hand': 0.051,
    'thigh': 0.221,
    'leg': 0.121,
    'foot': 0.057
}