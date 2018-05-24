# %%
from pandoctools.feather import FeatherHelper

fh = FeatherHelper(dir='feather')
# dir=r"%USERPROFILE%\feather\document"
# dir="feather" same as
# dir="./feather" (default)


# %%
fh.name('1')
try:
    # raise Exception
    A, B, C = fh.pull()
except:
    # calculate stuff
    fh.push(A, B, C)


import pandas as pd
from os.path import join, normpath, isabs, basename
import feather
import numpy as np


class FeatherHelper:
    """
    Helps save-to and load-from Feather format data frames.
    """
    def __init__(self, folder: str=None, ext: str=''):
        self.dir = folder
        self.ext = ('.' + ext) if (ext is not '') else ''

    def save(self, arr: np.ndarray, path: str):
        self.save_df(pd.DataFrame(arr), path)

    def save_df(self, df: pd.DataFrame, path: str):
        """
        if basename(path) == path then extension is appended
        """
        if basename(path) == path:
            path = path + self.ext
        if self.dir is not None:
            if not isabs(path):
                path = normpath(join(self.dir, path))
        feather.write_dataframe(df, path)

    def load(self, path: str) -> np.ndarray:
        return self.load_df(path).as_matrix()

    def load_df(self, path: str) -> pd.DataFrame:
        """
        if basename(path) == path then extension is appended
        """
        if basename(path) == path:
            path = path + self.ext
        if self.dir is not None:
            if not isabs(path):
                path = normpath(join(self.dir, path))
        return feather.read_dataframe(path)
