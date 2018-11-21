"""
https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/matplotlib
"""
import io
import base64
from sugartex import sugartex, stex
from IPython.display import display, Markdown, HTML
import numpy as np
import pandas as pd
from typing import Tuple
import pypandoc

from ..knitty import KNITTY, NOIPYTHON, NTERACT
from IPython import get_ipython

ipython = get_ipython()

GR = (1 + 5 ** 0.5) / 2
sugartex.mpl_hack()
sugartex.ready()

_ext = 'svg'
_dpi = 300
_preview_width = '600px'
_readied = False
_interact = True
_hide = False
_magic = None


# noinspection PyShadowingNames,PyIncorrectDocstring
def ready(ext: str='svg',
          dpi: int=300,
          preview_width: str='600px',
          hide: bool=False,
          interact: bool=True,
          magic: str=None,
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
    Should be run before ``import matplotlib.pyplot``. Default magic:
 
    1. In Knitty mode uses ``%matplotlib agg`` magic.
    2. In standard mode (Jupyter / JupyterLab mode) uses
        ``%matplotlib widget`` magic if ``jupyterlab`` and ``ipympl`` modules are found
        othewise uses ``%matplotlib notebook`` magic.
    3. In Hydrogen, Nteract and non-Jupyter (non-IPython) mode uses ``matplotlib.use('Qt5Agg')``. 

    Parameters
    ----------
    magic :
        matplotlib magic without ``%matplotlib `` prefix
    font_size :
        In pt. Default is 12.8pt ~ 17px
    """
    # TODO: change single font to list of fallback fonts

    if magic is not None:
        pass
    elif KNITTY:
        magic = "agg"
    elif NOIPYTHON or NTERACT:
        pass
    else:
        try:
            import jupyterlab
            import ipympl
            magic = "widget"
        except ModuleNotFoundError:
            magic = "notebook"

    if magic is not None:
        ipython.magic("matplotlib " + magic)

    from matplotlib import font_manager
    import matplotlib as mpl

    global _readied;       _readied = True
    global _ext;           _ext = ext
    global _dpi;           _dpi = dpi
    global _preview_width; _preview_width = preview_width
    global _interact;      _interact = interact
    global _hide;          _hide = hide
    global _magic;         _magic = magic

    if NOIPYTHON or NTERACT:
        mpl.use('Qt5Agg')

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
    if mpl.__version__.startswith('2'):
        mpl.rc('text.latex', unicode=True)
    if font_dir is not None:
        font_dirs = [font_dir, ]
        font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
        font_list = font_manager.createFontList(font_files)
        font_manager.fontManager.ttflist.extend(font_list)


def img(plot,
        caption: str='',
        attrs: str='',
        name: str=None,
        ext: str=None,
        dpi: int=None,
        preview_width: str=None,
        hide: bool=None,
        interact: bool=None,
        ret: bool=False,
        ) -> str or None:
    """
    Parameters
    ----------
    plot :
        matplotlib.pyplot
    caption :
        Markdown image caption inside square brackets ![...](...){...}
    attrs :
        Markdown image attributes inside curly brackets ![...](...){...}
    name :
        File name to store image (without extension). If None then use base64 encoding.
    ext :
        File extension
        default ``'svg'`` or the value set in ``ready()``
    dpi :
        DPI for PNG
        default ``300`` or the value set in ``ready()``
    preview_width :
        Hydrogen or nteract image preview width
        default ``'600px'`` or the value set in ``ready()``
    hide :
        Whether to display / print plots or hide them.
        default ``False`` or the value set in ``ready()``
    interact :
        Whether to show interactive plot via Qt or Widget
        default ``True`` or the value set in ``ready()``
    ret :
        Whether to return image URL string

    Returns
    ------
    url :
        Image URL if ret else None
    """
    if not _readied:
        ready()

    ext = ext if (ext is not None) else _ext
    dpi = dpi if (dpi is not None) else _dpi
    preview_width = preview_width if (preview_width is not None) else _preview_width
    interact = interact if (interact is not None) else _interact
    hide = hide if (hide is not None) else _hide

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

    if not hide:
        image = f'![{caption}]({url})' + ('{' + attrs + '}' if attrs else '')
        cap = pypandoc.convert_text(f'[{caption}]{{{attrs}}}', 'html', format='md') if caption or attrs else ''

        if KNITTY:
            print(image)
        elif NOIPYTHON or NTERACT:
            display(Markdown(f'<img src="{base64_url}" style="width: {preview_width};"/>'))
            # there were problems with ``display(HTML(...))``
            if cap:
                display(HTML(cap))
            if interact:
                plot.show()
            else:
                plot.clf()
                plot.close()
        else:
            if interact:
                if cap:
                    display(HTML(cap))
            else:
                ipython.magic("matplotlib agg")
                display(HTML(pypandoc.convert_text(image, 'html', format='md')))
                if _magic:
                    ipython.magic("matplotlib " + _magic)
                else:
                    raise RuntimeError('Unknown bug: reached unreachable code.')
    else:
        plot.clf()
        plot.close()
    if ret:
        return url


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
