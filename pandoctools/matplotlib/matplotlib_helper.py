"""
https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/matplotlib
"""
import io
import base64
# noinspection PyUnresolvedReferences
from sugartex import sugartex, stex
import numpy as np
import pandas as pd
from typing import Tuple, Union, Iterable
import os
from os import path as p
from IPython import get_ipython


class F:
    KNITTY = 'knitty'
    PYTHON = 'python'
    NTERACT = 'nteract'
    LAB = 'lab'
    OTHER = 'other'


def is_notebook_or_qtconsole():
    shell = get_ipython().__class__.__name__
    if shell == 'ZMQInteractiveShell':
        return True   # Jupyter notebook or qtconsole
    elif shell == 'TerminalInteractiveShell':
        return False  # IPython Terminal
    elif shell == 'NoneType':
        return False  # Python interpreter
    else:
        return False


def get_front() -> str:
    if not get_ipython():
        return F.PYTHON
    if os.getenv('KNITTY', '').lower() == 'true':
        return F.KNITTY

    if is_notebook_or_qtconsole():
        path = os.getenv('PATH', '')
        atom_win = os.sep + 'atom' + os.sep + 'app-'
        atom_lin = os.sep + 'atom' + os.pathsep
        nteract_win = os.sep + 'nteract' + os.pathsep
        nteract_lin = '_nterac'
        if (nteract_win in path) or (nteract_lin in path) or (atom_win in path) or (atom_lin in path):
            return F.NTERACT

        try:
            import jupyterlab
            import ipympl

            return F.LAB
        except ModuleNotFoundError:
            pass

    return F.OTHER


def import_matplotlib(magic: str or None):
    """
    Returns matplotlib
    """
    front = get_front()

    if magic == 'auto':
        if front == F.KNITTY:
            magic = "agg"
        elif front == F.NTERACT:
            magic = "qt5"
        elif front == F.LAB:
            magic = "widget"
        elif front == F.PYTHON:
            magic = 'Qt5Agg'  # special case
    elif (magic == 'qt') and (front == F.PYTHON):
        magic = 'Qt5Agg'  # special case

    if magic is None:
        import matplotlib as mpl
    elif magic == 'Qt5Agg':
        import matplotlib as mpl
        mpl.use('Qt5Agg')
    else:
        get_ipython().magic("matplotlib " + magic)
        import matplotlib as mpl

    return mpl


_readied = False
GR = (1 + 5 ** 0.5) / 2
sugartex.mpl_hack()
sugartex.ready()


# noinspection PyIncorrectDocstring
def ready(ext: str='svg',
          dpi: int=300,
          folder: str='./pic',
          hide: bool=False,
          magic: str='auto',
          font_dir: str=None,
          font_size: float=12.8,
          font_family: str="serif",
          font_serif: Union[str, tuple]=('Libertinus Serif', 'PT Astra Serif', 'Libertinus Math'),
          font_sans: Union[str, tuple]=('Segoe UI', 'Noto Sans', 'DejaVu Sans'),
          font_cursive: Union[str, tuple]=None,
          font_mono: Union[str, tuple]=('Open Mono', 'DejaVu Sans Mono'),
          fontm_set: str='custom',
          fontm_mono: str='Open Mono',
          fontm_calig: str="MJ_Cal",
          fontm_regular: str="MJ",
          fontm_italic: str="MJ_Mat",
          fontm_bold: str="MJ",
          fontm_itbold: str="MJ_Mat",
          ):
    """
    Should be run before ``import matplotlib.pyplot``.

    ``magic`` auto-detect for ``f'%matplotlib {magic}'`` (if ``'auto'``):
        * In Knitty mode uses ``agg`` (if ``$KNITTY`` env var is ``TRUE``),
        * In JupyterLab mode uses ``widget``
          (if ``jupyterlab`` and ``ipympl`` modules were found),
        * In Hydrogen and Nteract modes uses ``qt5`` magic,
        * In non-Jupyter and non-IPython modes calls ``matplotlib.use('Qt5Agg')``.

    Parameters
    ----------
    folder :
        folder to save images to.
    magic :
        matplotlib magic without "%matplotlib " prefix
        or None for not changing matplotlib backend
        ("qt5" magic can work even without IPython/Jupyter).
    font_size :
        In pt. Default is 12.8pt ~ 17px.
    fontm_set :
        'cm' is also a good option.
    """
    # Set mpl backend:
    # ----------------
    mpl = import_matplotlib(magic)
    from matplotlib import font_manager

    # Set mpl fonts:
    # ----------------------
    def list_maybe(fonts: Union[str, Iterable]):
        return fonts if isinstance(fonts, str) else list(fonts)

    mpl.rcParams.update({
        "text.usetex": False,
        "font.size": font_size,
        "font.family": font_family,
        "font.serif": list_maybe(font_serif),
        "font.sans-serif": list_maybe(font_sans),
        "font.monospace": list_maybe(font_mono),
        "mathtext.fontset": fontm_set,
        "mathtext.cal": fontm_calig,
        "mathtext.tt": fontm_mono,
        "mathtext.rm": fontm_regular,
        "mathtext.it": fontm_italic + ":italic",
        "mathtext.bf": fontm_bold + ":bold",
        "mathtext.sf": fontm_itbold + ":bold:italic",
    })
    if font_cursive is not None:
        mpl.rcParams["font.cursive"] = list_maybe(font_cursive)

    if mpl.__version__.startswith('2'):
        mpl.rc('text.latex', unicode=True)

    font_dirs = [p.join(p.dirname(__file__), 'fonts')]
    if font_dir is not None:
        font_dirs.append(font_dir)
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    font_list = font_manager.createFontList(font_files)
    font_manager.fontManager.ttflist.extend(font_list)

    # Create prefix folder if needed:
    # -------------------------------
    if folder != '':
        folder = p.normpath(p.expanduser(p.expandvars(folder)))
        if not p.isdir(folder):
            os.makedirs(folder)

    # Export globals:
    # ---------------
    global _readied; _readied = True
    global _ext;     _ext = ext
    global _dpi;     _dpi = dpi
    global _hide;    _hide = hide
    global _folder;  _folder = folder


def img(plot,
        name: str=None,
        ext: str=None,
        dpi: int=None,
        hide: bool=None,
        return_path: bool=False
        ) -> str:
    """
    * If ``name`` is ``None`` then do not save an image.
    * If ``name`` is a relative path then it's relative
      with respect to the ``folder`` if it was specified
      in ``ready()`` otherwise - to the CWD.

    Parameters
    ----------
    plot :
        matplotlib.pyplot
    name :
        File name to store image (without extension).
    ext :
        File extension (or base64 format).
        [Default is 'svg' or the value set in `ready()`]
    dpi :
        DPI for PNG
        [Default is 300 or the value set in `ready()`]
    hide :
        Whether to hide interactive plot via Qt or Widget or not.
        [Default is False or the value set in `ready()`]
    return_path :
        Whether to return file path instead of base64 if `name` was given

    Returns
    ------
    url :
        Image base64 URL (or file path if `return_path`).
    """
    if not _readied:
        ready()

    ext = ext if (ext is not None) else _ext
    dpi = dpi if (dpi is not None) else _dpi
    hide = hide if (hide is not None) else _hide

    if name:
        file = p.normpath(p.expanduser(p.expandvars(name + "." + ext)))
        file = file if p.isabs(file) else p.normpath(p.join(_folder, file))
        if ext.upper() == 'PNG':
            plot.savefig(file, dpi=dpi)
        else:
            plot.savefig(file)
        with open(file, "rb") as f:
            image = f.read()
        if not p.abspath(file):
            file = file.replace('\\', '/')
    else:
        file = None
        with io.BytesIO() as f:
            plot.savefig(f, format=ext)
            image = f.getvalue()

    base64_url = 'data:image/{};base64,' + base64.b64encode(image).decode("utf-8")
    if ext.upper() == 'PNG':
        base64_url = base64_url.format('png')
    elif ext.upper() == 'SVG':
        base64_url = base64_url.format('svg+xml')
    else:
        raise ValueError(f'{ext} extension is not supported by matplotlib helper.')

    if hide:
        plot.close()  # works in Jupyter too
    else:
        plot.show()

    if return_path and name:
        return file
    else:
        return base64_url


def img_path(plot,
             name: str,
             ext: str=None,
             dpi: int=None,
             hide: bool=None,
             ) -> str:
    """
    If ``name`` is a relative path then it's relative
    with respect to the ``folder`` if it was specified
    in ``ready()`` otherwise - to the CWD.

    Parameters
    ----------
    plot :
        matplotlib.pyplot
    name :
        File name to store image (without extension).
    ext :
        File extension (or base64 format).
        [Default is 'svg' or the value set in `ready()`]
    dpi :
        DPI for PNG
        [Default is 300 or the value set in `ready()`]
    hide :
        Whether to hide interactive plot via Qt or Widget or not.
        [Default is False or the value set in `ready()`]

    Returns
    ------
    url :
        Image path
    """
    if not name:
        raise ValueError('Invalid name: ' + name)
    return img(plot, name, ext, dpi, hide, return_path=True)


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
