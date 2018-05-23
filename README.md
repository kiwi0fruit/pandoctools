# Pandoctools

Pandoc profile manager (stores any CLI filter pipelines), CLI wrapper for Panflute, other helpers.

**Pandoctools is not finished yet!**

## Install

### Windows:

* Install [Miniconda](https://conda.io/miniconda.html)
* Install [Git together with Bash](https://git-scm.com/downloads)  
  Git is needed for writing text conversion profiles in cross-platform bash language instead of Windows-only batch language (that is supported by Pandoctools anyway).

```
conda install "conda>=4.5.4"
conda create -n myenv python=3
call activale myenv

conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.0,<2.1" matplotlib feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future shutilwhich cython pyperclip pywin32
pip install panflute knitty sugartex winshell
pip install git+https://github.com/kiwi0fruit/pandoctools.git
```

* Install [pandoc-crossref v0.3.0.1](https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.0.1) to  
  `<miniconda-path>/envs/myenv/Library/bin`.
* Remember, that opening right-click context menu while holding Shift gives "Copy as Path" menu option. Feel free to use it as Pandoctools strips double quotes.


### Unix:

* Install [Miniconda](https://conda.io/miniconda.html)
* Install Git. On Ubuntu/Debian: `sudo apt-get install git` Fedora/CentOS and macOS also have such one-liners.

```
conda install "conda>=4.5.4"
conda create -n myenv python=3
source activate myenv

conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.0,<2.1" matplotlib feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future shutilwhich cython pyperclip pyqt
pip install panflute knitty sugartex
pip install git+https://github.com/kiwi0fruit/pandoctools.git
```
* Install [pandoc-crossref v0.3.0.1](https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.0.1) to  
  `<miniconda-path>/envs/myenv/bin`.
* If there be problems with the desktop shortcut then delete the shortcut and install pandoctools again.
