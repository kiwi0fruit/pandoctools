from IPython.display import display, Markdown  # Image, SVG
# from subprocess import call
# import os
import io
import base64
from sugartex import sugartex, stex
import re
import matplotlib as mpl
from matplotlib import font_manager


GR = (1 + 5**0.5) / 2
sugartex.mpl_hack()
sugartex.ready()
options = dict()


class MPLHelper:
    """
    Helper for Matplotlib with Atom/Hydrogen, Knotr/Stitch.
    Can export plots with unicode to SVG via Poppler.

    1. Copy [this folder](https://github.com/mathjax/MathJax/tree/master/fonts/HTML-CSS/TeX/otf)
        (`MathJax_Math`, `MathJax_Main`, `MathJax_Caligraphic` fonts are of
        particular interest) to custom folder (`../Fonts/MathJaxTeX` in my case).
        Command `git clone https://github.com/mathjax/MathJax` can be useful.
    2. LaTeX in Matplotlib [manual](https://matplotlib.org/users/mathtext.html)
    3. Delete `fontList.cache`, `fontList.py3k.cache` or `fontList.json`
        from `%USERPROFILE%\.matplotlib` folder after installing new font.
    4. If fonts become bold without a reason (`"font.family"` affected text) try:
        * clearing font cache (see above) and `tex.cache` folder
        * clearing cache several times (for some reason this can help)
        * updating matplotlib: `conda install -c anaconda matplotlib`
        * deleting matplotlib and installing again
    5. Install [Computer Modern Unicode](https://sourceforge.net/projects/cm-unicode/)
        for bold-italic unicode support: `"mathtext.sf": "CMU Serif:bold:italic"`
        sans-serif command `\mathsf{}` is reassigned because sans-serif font is
        rarely used in serif docs.
    """
    def __init__(self,
                 knitty: bool=False,
                 delay: bool=False,
                 # poppler: str=r'C:\Program Files (x86)\poppler\bin',  # http://blog.alivate.com.au/poppler-windows/
                 font_dir: str='../Fonts/MathJaxTeX',
                 font_size: float=12.8  # 12.8pt ~ 17px
                 ):
        self.options = options
        options['knitty'] = knitty
        # options['poppler'] = poppler
        options['font_dir'] = font_dir
        self.mpl_params = {
            "text.usetex": False,
            "font.size": font_size,
            "font.family": "serif",
            "font.serif": "Times New Roman",
            "font.cursive": "Comic Sans MS",
            "font.monospace": "Consolas",
            "mathtext.fontset": "custom",  # cm
            "mathtext.cal": "MathJax_Caligraphic",
            "mathtext.tt": "Consolas",  # MathJax_Typewriter
            "mathtext.rm": "MathJax_Main",
            "mathtext.it": "MathJax_Math:italic",
            "mathtext.bf": "MathJax_Main:bold",
            "mathtext.sf": "MathJax_Math:bold:italic"  # CMU Serif
        }
        if not delay:
            self.tune()

    def tune(self):
        mpl.use('Qt5Agg')
        mpl.rc('text.latex', unicode=True)
        font_dirs = [options['font_dir'], ]
        font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
        font_list = font_manager.createFontList(font_files)
        font_manager.fontManager.ttflist.extend(font_list)
        mpl.rcParams.update(self.mpl_params)


def img(plot, name: str = None, qt: bool = False) -> str:
    """
    :param: plot: matplotlib.pyplot
    :param: name: File name to store image
    :param: qt: Whether to show interactive plot via Qt
        Presumably mpl.use('Qt5Agg') was called
    :return: url: Image URL if STITCH is True
        else ""
    """
    if name is None:
        with io.BytesIO() as f:
            plot.savefig(f, format='svg')
            svg = f.getvalue()
    else:
        plot.savefig(name + ".svg")
        with open(name + ".svg", "rb") as f:
            svg = f.read()

    # plot.savefig(name + ".pdf")  # was useful with external LaTeX renderer instead of matplotlib's
    # call([os.path.join(options['poppler'], "pdftocairo"), "-svg", name + ".pdf", name + ".svg"],
    #      cwd=os.getcwd())

    base64_url = 'data:image/svg+xml;base64,' + base64.b64encode(svg).decode("utf-8")
    if name is None:
        url = base64_url
    else:
        url = name + ".svg"

    if not options['knitty']:  # noinspection PyTypeChecker
        display(Markdown('![]({})'.format(base64_url)))  # display(SVG(name_svg)) was buggy in Hydrogen.
    if not options['knitty'] and qt:
        plot.show()
    return url if options['knitty'] else ""
