iclothing
=======================

iclothing is a Python package to obtain local clothing insulation for overall clothing insulation.

Please cite us if you use this package:

Installation
-----

```bash
pip install iclothing
```

Dependencies
-----

- numpy

License
-----

GNU General Public License v3.0


Example
-----

```python
import iclothing

icl = 0.3
icli = iclothing.get_icl_dict(icl=icl, sex="male", met=1)
print(icli)
```
output:
```
{
    'Head': 0.13,
    'Neck': 0.0,
    'Chest': 0.35,
    'Back': 0.27,
    'Pelvis': 0.91,
    'LShoulder': 0.0,
    'LArm': 0.0,
    'LHand': 0.0,
    'RShoulder': 0.0,
    'RArm': 0.0,
    'RHand': 0.0,
    'LThigh': 0.48,
    'LLeg': 0.043,
    'LFoot': 1.342,
    'RThigh': 0.48,
    'RLeg': 0.043,
    'RFoot': 1.342
}
```


