"""
Helper for Matplotlib with Atom/Hydrogen/Knitty.
Can export plots with unicode to SVG or PNG.
See default fonts in default keyword arguments.

MJ fonts:
    https://github.com/kiwi0fruit/open-fonts/tree/master/Fonts/MJ/oft

Hints:

1. Delete `fontList.cache`, `fontList.py3k.cache` or `fontList.json`
    from `%USERPROFILE%\.matplotlib` folder after installing new font.
2. If fonts become bold without a reason (`"font.family"` affected text) try:
    * clearing font cache (see above) and `tex.cache` folder
    * clearing cache several times (for some reason this can help)
    * updating matplotlib: `conda install -c anaconda matplotlib`
    * deleting matplotlib and installing again
3. Install [Computer Modern Unicode](https://sourceforge.net/projects/cm-unicode/)
    for bold-italic unicode support: `"mathtext.sf": "CMU Serif:bold:italic"`
    sans-serif command `\mathsf{}` is reassigned because sans-serif font is
    rarely used in serif docs.
"""
import io
import base64
# noinspection PyUnresolvedReferences
from sugartex import sugartex, stex, stex2
import matplotlib as mpl
from matplotlib import font_manager
from IPython.display import display, Markdown
import numpy as np
import pandas as pd
from typing import Tuple
# import subprocess.call
# import os


GR = (1 + 5 ** 0.5) / 2
mpl_params = {}
sugartex.mpl_hack()
sugartex.ready()

_knitty = False
_font_dir = None
_ext = 'svg'
_dpi = 300
_preview_width = '600px'
# _poppler = ""


def finalize():
    if not _knitty:
        mpl.use('Qt5Agg')
    mpl.rc('text.latex', unicode=True)
    if _font_dir is not None:
        font_dirs = [_font_dir, ]
        font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
        font_list = font_manager.createFontList(font_files)
        font_manager.fontManager.ttflist.extend(font_list)
    mpl.rcParams.update(mpl_params)


_finalize = finalize


# noinspection PyShadowingNames
def ready(knitty: bool=False,
          finalize: bool=True,
          ext: str='svg',
          dpi: int=300,
          preview_width: str = '600px',
          font_dir: str=None,
          font_size: float=12.8,  # 12.8pt ~ 17px
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

    # poppler: str=r'C:\Program Files (x86)\poppler\bin',
    #   http://blog.alivate.com.au/poppler-windows/
    # global _poppler
    # _poppler = poppler
    global mpl_params
    global _knitty;        _knitty = knitty
    global _font_dir;      _font_dir = font_dir
    global _preview_width; _preview_width = preview_width
    global _ext;           _ext = ext
    global _dpi;           _dpi = dpi

    mpl_params.update({
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
    # TODO: change single font to list of fallback fonts
    if finalize:
        _finalize()


def img(plot,
        name: str=None,
        ext: str=None,  # default 'svg'
        dpi: int=None,  # default 300
        preview_width: str=None,  # default '600px'
        hide: bool=False,
        qt: bool=False,
        ) -> str:
    """
    :plot: matplotlib.pyplot
    :name: File name to store image (without extension)
    :ext: File extension
        default 'svg'
    :dpi: DPI for PNG
        default 300
    :preview_width: Hydrogen img preview width
        default '600px'
    :hide: Whether to show Hydrogen and Qt plots at all
    :qt: Whether to show interactive plot via Qt
        Presumably mpl.use('Qt5Agg') was called

    :return: url: Image URL if KNITTY is True
        else ""
    """
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

    # plot.savefig(name + ".pdf")  # was useful with external LaTeX renderer instead of matplotlib's
    # subprocess.call([os.path.join(_poppler, "pdftocairo"), "-svg", name + ".pdf", name + ".svg"],
    #                  cwd=os.getcwd())

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

    if _knitty:
        hide = True

    if not hide:
        # noinspection PyTypeChecker
        display(Markdown('<img src="{}" style="width: {};"/>'.format(base64_url, preview_width)))
    if (not hide) and qt:
        plot.show()
    return url if _knitty else ""


def dump2D(file_path: str,
            matrix: np.ndarray=None,
            x: np.ndarray=None,
            y: np.ndarray=None,
            header=False) -> None:
    """
    Dumps 2D plot agruments to CSV. Provide 2D marrix OR two 1D arrays.

    :matrix: 2D marrix
    :x: 1D array
    :y: 1D array
    :header: boolean or list of string, default True
        Write out the column names. If a list of strings is given
        it is assumed to be aliases for the column names
    """
    df = pd.DataFrame(np.array((x, y)).T if (matrix is None) else matrix)
    df.to_csv(file_path, header=header, index=None)


def inch(cm: float) -> float:
    """cm to inch"""
    return cm / 2.54


def cm(inch: float) -> float:
    """inch to cm"""
    return inch * 2.54


def figsize(w: float=None, h: float=None) -> Tuple[float, float]:
    """Returns (width, height) based on golden ratio
    if either width or height was provided.
    """
    if (w is None) and (h is None):
        raise ValueError('Either width or height should be provided (now they are both None).')
    w = (h * GR) if (w is None) else w
    h = (w / GR) if (h is None) else h

    return (w, h)
