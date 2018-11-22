"""
https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/matplotlib
"""
import io
import base64
# noinspection PyUnresolvedReferences
from sugartex import sugartex, stex
from IPython.display import display as _display, Markdown, HTML
import numpy as np
import pandas as pd
from typing import Tuple, Union
import pypandoc

from ..knitty import front as frontend, Front
from IPython import get_ipython

ipython = get_ipython()
# noinspection PyTypeChecker
def display(x: object): return _display(x)

GR = (1 + 5 ** 0.5) / 2
sugartex.mpl_hack()
sugartex.ready()

_ext = 'svg'
_dpi = 300
_preview_width = '600px'
_readied = False
_interactive = True
_hide = False
_magic = None
_front = None


# noinspection PyShadowingNames,PyIncorrectDocstring
def ready(ext: str='svg',
          dpi: int=300,
          preview_width: str='600px',
          hide: bool=False,
          interactive: bool=True,
          magic: str=None,
          front: str=None,
          font_dir: str=None,
          font_size: float=12.8,
          font_family: str="serif",
          font_serif: Union[str, tuple]=('Libertinus Serif', 'PT Astra Serif', 'Libertinus Math'),
          font_sans: Union[str, tuple]=('Segoe UI', 'Noto Sans', 'DejaVu Sans'),
          font_cursive: Union[str, tuple]=None,
          font_mono: Union[str, tuple]=('Open Mono', 'DejaVu Sans Mono'),
          fontm_mono: str='Open Mono',
          fontm_calig: str="MJ_Cal",
          fontm_regular: str="MJ",
          fontm_italic: str="MJ_Mat",
          fontm_bold: str="MJ",
          fontm_itbold: str="MJ_Mat",
          ):
    """
    Should be run before ``import matplotlib.pyplot``.

    ``magic`` defaults:
        * In Knitty mode uses ``%matplotlib agg`` magic,
        * In standard Jupyter mode uses ``%matplotlib notebook`` magic,
        * In JupyterLab mode uses ``%matplotlib widget`` magic
          (if ``jupyterlab`` and ``ipympl`` modules were found),
        * In Hydrogen, Nteract and non-Jupyter (non-IPython) mode calls
          ``matplotlib.use('Qt5Agg')``.
        * Notable magic: ``%matplotlib qt5``.

    ``front`` possible values:
        * ``KNITTY``,
        * ``NONE`` (stands for neither IPython nor Jupyter),
        * ``NTERACT`` (stans for Nteract or Atom/Hydrogen),
        * ``LAB`` (stands for Jupyter Lab),
        * ``NOTEBOOK`` (stands for Jupyter Notebook).
          Can also be changed by setting ``$KNITTY`` env var
          to the values above
          (additionally ``TRUE`` means ``KNITTY``).

    Parameters
    ----------
    magic :
        matplotlib magic without ``%matplotlib `` prefix
    front :
        Frontend. Default value is guessed automatically.
    font_size :
        In pt. Default is 12.8pt ~ 17px
    """
    global _front
    front = front.lower() if isinstance(front, str) else ''
    if front in frontend.keys:
        _front = Front(**{front: True})
    else:
        _front = frontend

    if magic is not None:
        pass
    elif _front.KNITTY:
        magic = "agg"
    elif _front.NONE or _front.NTERACT:
        pass  # magic is None
    elif _front.LAB:
        magic = "widget"
    elif _front.NOTEBOOK:
        magic = "notebook"

    if magic is not None:
        ipython.magic("matplotlib " + magic)

    from matplotlib import font_manager
    import matplotlib as mpl

    global _readied;       _readied = True
    global _ext;           _ext = ext
    global _dpi;           _dpi = dpi
    global _preview_width; _preview_width = preview_width
    global _interactive;    _interactive = interactive
    global _hide;          _hide = hide
    global _magic;         _magic = magic

    if (_front.NONE or _front.NTERACT) and (magic is None):
        mpl.use('Qt5Agg')

    def list_maybe(fonts):
        return fonts if isinstance(fonts, str) else list(fonts)

    mpl.rcParams.update({
        "text.usetex": False,
        "font.size": font_size,
        "font.family": font_family,
        "font.serif": list_maybe(font_serif),
        "font.sans-serif": list_maybe(font_sans),
        "font.monospace": list_maybe(font_mono),
        "mathtext.fontset": "custom",  # cm
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
    print(__file__)
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
        interactive: bool=None,
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
    interactive :
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
    interactive = interactive if (interactive is not None) else _interactive
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

        if _front.KNITTY:
            if ret:
                return url
            else:
                print('\n\n' + image + '\n\n')
        elif _front.NONE or _front.NTERACT:
            display(Markdown(f'<img src="{base64_url}" style="width: {preview_width};"/>'))
            # there were problems with ``display(HTML(...))``
            if cap:
                display(HTML(cap))
            if interactive:
                plot.show()
            else:
                plot.close()
        elif _front.LAB or _front.NOTEBOOK:
            if interactive:
                if cap:
                    display(HTML(cap))
            else:
                ipython.magic("matplotlib agg")
                display(HTML(pypandoc.convert_text(image, 'html', format='md')))
                if _magic is not None:
                    # noinspection PyTypeChecker
                    ipython.magic("matplotlib " + _magic)
                else:
                    raise RuntimeError('Unknown bug')
        else:
            raise RuntimeError('Unknown bug')
    else:
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
