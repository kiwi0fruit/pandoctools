"""
https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/matplotlib
"""
import io
import base64
# noinspection PyUnresolvedReferences
from sugartex import sugartex, stex
import matplotlib as mpl
from matplotlib import font_manager
from IPython.display import display, Markdown
import numpy as np
import pandas as pd
from typing import Tuple
from ..knitty import KNITTY


if not KNITTY:
    mpl.use('Qt5Agg')

GR = (1 + 5 ** 0.5) / 2
sugartex.mpl_hack()
sugartex.ready()

_ext = 'svg'
_dpi = 300
_preview_width = '600px'
_readied = False


# noinspection PyShadowingNames,PyIncorrectDocstring
def ready(ext: str='svg',
          dpi: int=300,
          preview_width: str = '600px',
          font_dir: str=None,
          font_size: float=12.8,
          font_family: str="serif",
          font_serif: str="Libertinus Serif",
          font_sans: str="Segoe UI",
          font_cursive: str="Comic Sans MS",
          font_mono: str="Consolas",
          fontm_calig: str="MJ_Cal",
          fontm_regular: str="MJ",
          fontm_italic: str="MJ_Mat",
          fontm_bold: str="MJ",
          fontm_itbold: str="MJ_Mat"):
    """
    Should be run before import matplotlib.pyplot

    Parameters
    ----------
    font_size : float
        In pt. Default is 12.8pt ~ 17px
    """
    # TODO: change single font to list of fallback fonts

    global _readied;       _readied = True
    global _ext;           _ext = ext
    global _dpi;           _dpi = dpi
    global _preview_width; _preview_width = preview_width

    mpl.rcParams.update({
        "text.usetex": False,
        "font.size": font_size,
        "font.family": font_family,
        "font.serif": font_serif,
        "font.sans-serif": font_sans,
        "font.cursive": font_cursive,
        "font.monospace": font_mono,
        "mathtext.fontset": "custom",  # cm
        "mathtext.cal": fontm_calig,
        "mathtext.tt": font_mono,
        "mathtext.rm": fontm_regular,
        "mathtext.it": fontm_italic + ":italic",
        "mathtext.bf": fontm_bold + ":bold",
        "mathtext.sf": fontm_itbold + ":bold:italic"
    })

    mpl.rc('text.latex', unicode=True)
    if font_dir is not None:
        font_dirs = [font_dir, ]
        font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
        font_list = font_manager.createFontList(font_files)
        font_manager.fontManager.ttflist.extend(font_list)


def img(plot,
        name: str=None,
        ext: str=None,
        dpi: int=None,
        preview_width: str=None,
        hide: bool=False,
        qt: bool=False,
        ) -> str:
    """
    Parameters
    ----------
    plot :
        matplotlib.pyplot
    name :
        File name to store image (without extension)
    ext :
        File extension
        default 'svg' or value set in ready()
    dpi :
        DPI for PNG
        default 300 or value set in ready()
    preview_width :
        Hydrogen img preview width
        default '600px' or value set in ready()
    hide :
        Whether to show Hydrogen and Qt plots at all
    qt :
        Whether to show interactive plot via Qt
        Presumably mpl.use('Qt5Agg') was called in finalize()

    Returns
    ------
    url :
        Image URL if KNITTY is True (OS env var)
        else ""
    """
    if not _readied:
        ready()

    ext = ext if (ext is not None) else _ext
    dpi = dpi if (dpi is not None) else _dpi
    preview_width = preview_width if (preview_width is not None) else _preview_width

    if name is None:
        with io.BytesIO() as f:
            plot.savefig(f, format=ext)
            image = f.getvalue()
    else:
        file_name = name + "." + ext
        if ext.upper() == 'PNG':
            plot.savefig(file_name, dpi=dpi)
        else:
            plot.savefig(file_name)
        with open(file_name, "rb") as f:
            image = f.read()

    base64_url = 'data:image/{};base64,' + base64.b64encode(image).decode("utf-8")
    if ext.upper() == 'PNG':
        base64_url = base64_url.format('png')
    elif ext.upper() == 'SVG':
        base64_url = base64_url.format('svg+xml')
    else:
        raise ValueError('{} extension is not supported by matplotlib helper.'.format(ext))

    if name is None:
        url = base64_url
    else:
        url = name + "." + ext

    if KNITTY:
        hide = True
    if not hide:
        # noinspection PyTypeChecker
        display(Markdown('<img src="{}" style="width: {};"/>'.format(base64_url, preview_width)))
    if (not hide) and qt:
        plot.show()
    return url if KNITTY else ""


# noinspection PyPep8Naming
def dump2D(file_path: str,
           matrix: np.ndarray=None,
           x: np.ndarray=None,
           y: np.ndarray=None,
           stack: Tuple[np.ndarray]=None,
           cat: Tuple[np.ndarray]=None,
           header=False) -> None:
    """
    Dumps 2D plot arguments to CSV file. Provide 2D matrix,
    or two 1D arrays, or tuple of 1D or 2D arrays.

    Parameters
    ----------
    file_path :
    matrix :
        2D array [[x, y, ...], ...]
    x :
        1D array
    y :
        1D array
    stack :
        tuple of 1D arrays
    cat :
        tuple of 1D or 2D arrays
    header :
        boolean or list of string, default True
        Write out the column names. If a list of strings is given
        it is assumed to be aliases for the column names
    """
    if not (matrix is None):
        pass
    elif not (x is None) and not (y is None):
        matrix = np.stack((x, y), axis=-1)
    elif not (stack is None):
        matrix = np.stack(stack, axis=-1)
    elif not (cat is None):
        matrix = np.concatenate([arr if len(arr.shape) > 1 else arr[np.newaxis].T
                                 for arr in cat], axis=-1)
    else:
        raise ValueError('Neither matrix, nor x,y, nor stack, nor cat were provided.')
    pd.DataFrame(matrix).to_csv(file_path, header=header, index=None)


# noinspection PyShadowingNames
def inch(cm: float=None, mm: float=None) -> float:
    """ Either cm or mm to inch """
    if (cm is not None) and (mm is None):
        return cm / 2.54
    elif (mm is not None) and (cm is None):
        return (mm / 10) / 2.54
    else:
        raise ValueError('Either cm or mm should be provided.')


# noinspection PyShadowingNames
def cm(inch: float) -> float:
    """ inch to cm """
    return inch * 2.54


# noinspection PyShadowingNames
def mm(inch: float) -> float:
    """ inch to mm """
    return (inch * 2.54) * 10


def figsize(w: float=None, h: float=None) -> Tuple[float, float]:
    """
    Returns (width, height) based on golden ratio
    if either width or height was provided.
    If both specified then they are simply returned.
    """
    if (w is None) and (h is None):
        raise ValueError('Either width or height should be provided.')
    w = (h * GR) if (w is None) else w
    h = (w / GR) if (h is None) else h
    return w, h


# http://blog.alivate.com.au/poppler-windows/
# import subprocess.call
# import os
# _poppler = ""
#   poppler: str=r'C:\Program Files (x86)\poppler\bin',
#   global _poppler; _poppler = poppler
#   plot.savefig(name + ".pdf")  # was useful with external LaTeX renderer instead of matplotlib's
#   subprocess.call([os.path.join(_poppler, "pdftocairo"), "-svg", name + ".pdf", name + ".svg"],
#                   cwd=os.getcwd())
