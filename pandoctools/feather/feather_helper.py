"""
Usage example in Atom/Hydrogen:

# %%
from pandoctools import feather as fh  # Feather Helper
# fh.setdir(r"%USERPROFILE%\feather\mydoc")

# %%
fh.name('1')
try:
    # raise Exception  # <- this is a switch
    A, B, C = fh.pull()
except:
    # calculate stuff
    fh.push(A, B, C)
"""

import pandas as pd
import os
from os import path as p
import feather
import numpy as np

_dir = ""
_cwd = ""


def setdir(dir_: str):
    global _dir, _cwd
    _dir = p.abspath(p.expandvars(dir_))
    if not p.isdir(_dir):
        os.makedirs(_dir)
    _cwd = p.join(_dir, 'default')


setdir(p.join('.', 'feather'))


class FeatherHelperError(Exception):
    pass


def name(name_: str):
    global _cwd
    _cwd = p.join(_dir, name_)


def push(*data_frames):
    global _cwd
    for i, df in enumerate(data_frames):
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)
            dot_ext = '.np'
        elif isinstance(df, pd.DataFrame):
            dot_ext = '.df'
        else:
            raise ValueError('Unsupported input type. Only numpy.ndarray and pandas.DataFrame are supported.')
        if len(df.as_matrix().shape) > 2:
            raise ValueError('3D and multidimensional arrays are not supported.')
        feather.write_dataframe(df, p.join(_cwd, str(i) + dot_ext))
        pass
    _cwd = p.join(_dir, 'default')


def pull():
    global _cwd
    file_names = sorted([p.basename(os.fsdecode(file))  # may be p.basename() is redundant
                         for file in os.listdir(os.fsencode(_cwd))],
                        key=lambda filename: int(p.splitext(filename)[0]))
    ret = []
    for i, file_name in enumerate(file_names):
        if i != int(p.splitext(file_name)[0]):
            raise FeatherHelperError('Wrong file name in {}'.format(_cwd))
        dot_ext = p.splitext(file_name)[1]
        df = feather.read_dataframe(p.join(_cwd, file_name))
        if dot_ext == '.np':
            ret.append(df.as_matrix())
        elif dot_ext == '.df':
            ret.append(df)
        else:
            raise FeatherHelperError('Wrong file ext in {}'.format(_cwd))
    _cwd = p.join(_dir, 'default')
    return ret
