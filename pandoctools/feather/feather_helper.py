import pandas as pd
import os
from os import path as p
import feather
import numpy as np

_dir = ""
_cwd = ""


def name(name_: str):
    global _cwd, _dir
    if _dir == "":
        _dir = p.join('.', 'feather')
        if not p.isdir(_dir):
            os.makedirs(_dir)
    _cwd = p.join(_dir, name_)
    if not p.isdir(_cwd):
        os.makedirs(_cwd)


def setdir(dir_: str):
    global _dir, _cwd
    _dir = p.abspath(p.expandvars(dir_))
    if not p.isdir(_dir):
        os.makedirs(_dir)
    name('default')


class FeatherHelperError(Exception):
    pass


def push(*data_frames, e: Exception=None):
    """
    Stores data frames. Prints exception ``e`` if it's not empty.
    """
    global _cwd
    if str(e):
        print(e)

    for i, df in enumerate(data_frames):
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)
            dot_ext = '.np'
        elif isinstance(df, pd.DataFrame):
            dot_ext = '.df'
        else:
            raise ValueError('Unsupported input type. Only numpy.ndarray and pandas.DataFrame are supported.')
        if len(df.values.shape) > 2:
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
            ret.append(df.values)
        elif dot_ext == '.df':
            ret.append(df)
        else:
            raise FeatherHelperError('Wrong file ext in {}'.format(_cwd))
    if not ret:
        raise FeatherHelperError()
    _cwd = p.join(_dir, 'default')
    return ret if (len(ret) > 1) else ret[0]
