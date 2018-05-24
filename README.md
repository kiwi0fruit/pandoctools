# Pandoctools

Pandoctools is a combination of tools that help write reproducible markdown reports. They rely on Pandoc and Jupyter kernels.

Glueing part of pandoctools is a profile manager of text processing pipelines. It stores short bash (or batch) scripts that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK.

Notable parts of Pandoctools.

1. [Knitty](https://github.com/kiwi0fruit/knitty): Knitty is another CLI for Stitch/Knotr: reproducible report generation tool via Jupyter, Pandoc and Markdown. Insert python code (or other Jupyter kernel code) to the Markdown document and have code's results in the output document.
2. [SugarTeX](https://github.com/kiwi0fruit/sugartex): SugarTeX is a more readable LaTeX language extension and transcompiler to LaTeX.

#### 3. TODO


# Contents

* [Install](#install)
* [Useful tips](#useful-tips)


# Install

### Windows:

* Install [Miniconda](https://conda.io/miniconda.html)
* Install [Git together with Bash](https://git-scm.com/downloads)  
  Git is needed for writing text conversion profiles in cross-platform bash language instead of Windows-only batch language (that is supported by Pandoctools anyway).

```
conda install "conda>=4.5.4"
conda create -n myenv python=3
call activale myenv

conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.0,<2.1" matplotlib feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future shutilwhich cython pyperclip pywin32 pandas
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

conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.0,<2.1" matplotlib feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future shutilwhich cython pyperclip pyqt pandas
pip install panflute knitty sugartex
pip install git+https://github.com/kiwi0fruit/pandoctools.git
```
* Install [pandoc-crossref v0.3.0.1](https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.0.1) to  
  `<miniconda-path>/envs/myenv/bin`.


# Useful tips

* [Tips](tips.md)
