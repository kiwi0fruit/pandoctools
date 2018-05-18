from IPython.display import display, Markdown  # Image, SVG
# from subprocess import call
# import os
import io
import base64
from sugartex import sugartex, stex
import matplotlib as mpl
from matplotlib import font_manager


GR = (1 + 5**0.5) / 2
sugartex.mpl_hack()
sugartex.ready()
options = {}


class MPLHelper:
    """
    Helper for Matplotlib with Atom/Hydrogen/Knitty.
    Can export plots with unicode to SVG or PNG.
    See default keyword arguments for default fonts.
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
    
    TODO: change single font to list of fallback fonts.
    """
    def __init__(self,
                 knitty: bool=False,
                 delay: bool=False,
                 # poppler: str=r'C:\Program Files (x86)\poppler\bin',
                 # http://blog.alivate.com.au/poppler-windows/
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
                 fontm_itbold: str="MJ_Mat"  # "CMU Serif"
                 ):
        self.options = options
        options['knitty'] = knitty
        # options['poppler'] = poppler
        options['font_dir'] = font_dir
        self.mpl_params = {
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
        }
        if not delay:
            self.tune()

    def tune(self):
        mpl.use('Qt5Agg')
        mpl.rc('text.latex', unicode=True)
        if options['font_dir'] is not None:
            font_dirs = [options['font_dir'], ]
            font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
            font_list = font_manager.createFontList(font_files)
            font_manager.fontManager.ttflist.extend(font_list)
        mpl.rcParams.update(self.mpl_params)


def img(plot,
        name: str=None,
        ext: str='svg',
        dpi: int=300,
        hide: bool=False,
        qt: bool=False,
        ) -> str:
    """
    :param: plot: matplotlib.pyplot
    :param: name: File name to store image (without extension)
    :param: ext: File extension
    :param: dpi: DPI for PNG
    :param: hide: Whether to show Hydrogen and Qt plots at all
    :param: qt: Whether to show interactive plot via Qt
        Presumably mpl.use('Qt5Agg') was called
    :return: url: Image URL if STITCH is True
        else ""
    """
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
    # call([os.path.join(options['poppler'], "pdftocairo"), "-svg", name + ".pdf", name + ".svg"],
    #      cwd=os.getcwd())

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

    if options['knitty']:
        hide = True

    if not hide:  # noinspection PyTypeChecker
        display(Markdown('![]({})'.format(base64_url)))  # display(SVG(name_svg)) was buggy in Hydrogen.
    if (not hide) and qt:
        plot.show()
    return url if options['knitty'] else ""
