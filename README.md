# Pandoctools

Pandoctools is a combination of tools that help write reproducible markdown reports. They rely on Pandoc and Jupyter kernels.

Glueing part of pandoctools is a profile manager of text processing pipelines. It stores short shell (bash or batch) scripts that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK.

Notable parts of Pandoctools.

1. [**Knitty**](https://github.com/kiwi0fruit/knitty) (dependence): Knitty is another CLI for Stitch/Knotr: reproducible report generation tool via Jupyter, Pandoc and Markdown. Insert python code (or other Jupyter kernel code) to the Markdown document and have code's results in the output document.
2. [**SugarTeX**](https://github.com/kiwi0fruit/sugartex) (dependence): SugarTeX is a more readable LaTeX language extension and transcompiler to LaTeX.
3. [**panfl**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/panfl) allows [Panflute](https://github.com/sergiocorreia/panflute) to be run as a command line script so it can be used in Pandoctools shell scripts. It actually actomatically searches for provided Panflute filters in provided directories (python's `sys.path` is the default place to search). See `panfl --help` for options details and format info.  Usage:
    * `panfl -t makdown filter1 filter2 filter3`
4. [**cat-md**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/cat_md) is a simple CLI tool that concatenates input files, joins them with double new lines and prints to stdout. In can have `stdin` as one of it's inputs - reads from stdin.
    * Usage: `cat-md stdin meta.yaml`
5. [**Feather Helper**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/feather) helps to cache 2D numpy arrays and pandas dataframes. Usage example in Atom/Hydrogen:

```py
from pandoctools import feather as fh
# fh.setdir(r"%USERPROFILE%\feather\mydoc")
# %%
fh.name('id1')
try:
    # raise Exception  # <- this is a switch
    A, B, C = fh.pull()
except:
    # calculate stuff
    fh.push(A, B, C)
```

6. [**Matplotlib Helper**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/matplotlib) is my custom helper to tune Matplotlib. I tuned fonts, made some tweaks to use it with SugarTeX, some tweaks to use mpl interactive plots in Atom/Hydrogen. Added export to raw markdown so it nicely works with [`results=pandoc` from Knitty](https://github.com/kiwi0fruit/knitty/blob/master/knitty.md#22-results-pandoc-chunk-option).


# Contents

* [Install](#install)
* [Useful tips](tips.md)


# Install

### Windows:

* Install [Miniconda](https://conda.io/miniconda.html)
* Install [Git together with Bash](https://git-scm.com/downloads)  
  Git is needed for writing text conversion profiles in cross-platform bash language instead of Windows-only batch language (that is supported by Pandoctools anyway).

```
conda install "conda>=4.5.4"
conda create -n myenv python=3
call activale myenv

conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.0,<2.1" matplotlib feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future shutilwhich cython pywin32 pandas
pip install panflute knitty sugartex winshell
pip install git+https://github.com/kiwi0fruit/pandoctools.git
```

* Install [pandoc-crossref v0.3.0.1](https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.0.1) to  
  `<miniconda-path>/envs/myenv/Library/bin`.


### Unix:

* Install [Miniconda](https://conda.io/miniconda.html)
* Install Git. On Ubuntu/Debian: `sudo apt-get install git` Fedora/CentOS and macOS also have such one-liners.

```
conda install "conda>=4.5.4"
conda create -n myenv python=3
source activate myenv

conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.0,<2.1" matplotlib feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future shutilwhich cython pandas
pip install panflute knitty sugartex
pip install git+https://github.com/kiwi0fruit/pandoctools.git
```
* Install [pandoc-crossref v0.3.0.1](https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.0.1) to  
  `<miniconda-path>/envs/myenv/bin`.


# Useful tips

[Useful tips](tips.md)
