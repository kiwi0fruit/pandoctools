# Pandoctools

Pandoctools is a combination of tools that help write reproducible markdown reports. They rely on Pandoc and Jupyter kernels.

**Introduction article**: [**Convenient and easily tweakable Atom+Markdown+Pandoc+Jupyter experience (can export to ipynb)**](https://github.com/kiwi0fruit/pandoctools/blob/master/atom_jupyter_pandoc_markdown.md).

“Glueing” part of pandoctools is a profile manager of text processing pipelines. It stores short shell (bash or batch) scripts that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK.


# Contents

* [Pandoctools](#pandoctools)
* [Contents](#contents)
* [Notable parts of Pandoctools](#notable-parts-of-pandoctools)
* [Examples markdown to ipynb](#examples-markdown-to-ipynb)
* [Install](#install)
* [Useful tips (reload imported modules in Hydrogen, R kernel, LyX)](#useful-tips-reload-imported-modules-in-hydrogen-r-kernel-lyx)
* [Alternatives to R Markdown (Markdown-based Literate Programming)](#alternatives-to-r-markdown-markdown-based-literate-programming)


# Notable parts of Pandoctools

* [**Pandoc**](https://pandoc.org/), [**Jupyter**](http://jupyter.org/), [**pandoc-crossref**](https://github.com/lierdakil/pandoc-crossref) (dependence) - classical tools.
* [**Pandoctools CLI app**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/cli): profile manager of text processing pipelines. It stores short shell (bash or batch) scripts - called profiles - that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK. Profiles can be used to convert any document of choise in the specified manner.
* [**Knitty**](https://github.com/kiwi0fruit/knitty) (dependence): Knitty is another CLI for Stitch/Knotr: reproducible report generation tool via Jupyter, Pandoc and Markdown. Insert python code (or other Jupyter kernel code) to the Markdown document and have code's results in the output document. Can even export to Jupyter ipynb notebooks.
* [**SugarTeX**](https://github.com/kiwi0fruit/sugartex) (dependence): SugarTeX is a more readable LaTeX language extension and transcompiler to LaTeX.
* [**Feather Helper**](https://github.com/kiwi0fruit/pandoctools/blob/master/pandoctools/feather) helps to cache 2D numpy arrays and pandas dataframes.
* [**Matplotlib Helper**](https://github.com/kiwi0fruit/pandoctools/blob/master/pandoctools/matplotlib) is my custom helper to tune Matplotlib experience.
* [**Pandas Helper**](https://github.com/kiwi0fruit/pandoctools/blob/master/pandoctools/pandas) helps print dataframes to Markdown.

Pandoctools is a tool for converting markdown document. But we also need tools for writing markdown and deploying python/Jupyter code blocks.  
And the best one for it is:

* [**Atom editor with plugins**](https://github.com/kiwi0fruit/pandoctools/blob/master/atom.md). It helps easily type Unicode, interactively run highlighed python/Jupyter code blocks and instantly see results (+ completions from the running Jupyter kernel), can convert basic pandoc markdown to html with live preview.
* Must have plugins: [**SugarTeX Completions**](https://github.com/kiwi0fruit/pandoctools/blob/master/atom.md#sugartex-completions), [**Unix Filter**](https://github.com/kiwi0fruit/pandoctools/blob/master/atom.md#unix-filter), [**Hydrogen**](https://github.com/kiwi0fruit/pandoctools/blob/master/atom.md#hydrogen), [**Markdown Preview Plus**](https://github.com/kiwi0fruit/pandoctools/blob/master/atom.md#markdown-preview-plus)


# Examples markdown to ipynb

Here are [**examples**](https://github.com/kiwi0fruit/pandoctools/blob/master/examples) that demonstrate converting documents:

* from markdown `.md` with Jupyter python code blocks, SugarTeX math and cross-references to `ipynb` notebook.
* from Hydrogen/python notebook `.py` with Atom/Hydrogen code cells, Knitty markdown incerts (again with SugarTeX math and cross-references) to `.ipynb` notebook.


# Install

## Windows:

Via conda:

* Install [Miniconda](https://conda.io/miniconda.html),
* Install [Git together with Bash](https://git-scm.com/downloads).  
  Git is needed for writing text conversion profiles in cross-platform bash language instead of Windows-only batch language (that is supported by Pandoctools anyway),
* :
  ```
  call activate root
  conda update conda
  conda create -n myenv python=3 pip setuptools

  call activate myenv
  conda update python pip setuptools

  conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.3.1" matplotlib ^
  feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters ^
  pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future ^
  shutilwhich cython pywin32 pandas

  pip install panflute knitty sugartex shortcutter pandoctools pandoctools-ready
  ```
* Install latest stable [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref/releases) (compatible with pandoc version) to `<miniconda-path>/envs/myenv/Library/bin`,
* Tips:
  - if pip install fails try to change codepage: `chcp 1252`, 
  - If Pandoc errors try downgrade to `"pandoc>=2.0,<2.1"` and pandoc-crossref v0.3.0.1,
  - Should be `"conda>=4.5.4"` (`conda update conda` should be enough).


Via pip:

* :
  ```
  pip install pandoctools pandoctools-ready
  ```
* Install latest stable [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref/releases) (compatible with pandoc version) to `<miniconda-path>/envs/myenv/Scripts`,


## Unix:

Via conda:

* Install [Miniconda](https://conda.io/miniconda.html),
* :
  ```
  source activate root
  conda update conda
  conda create -n myenv python=3 pip setuptools

  source activate myenv
  conda update python pip setuptools

  conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.3.1" matplotlib \
  feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters \
  pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future \
  shutilwhich cython pandas

  pip install panflute knitty sugartex shortcutter pandoctools pandoctools-ready
  ```
* Install latest stable [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref/releases) (compatible with pandoc version) to `<miniconda-path>/envs/myenv/bin`,
* Tips:
  - If Pandoc errors try downgrade to `"pandoc>=2.0,<2.1"` and pandoc-crossref v0.3.0.1,
  - Should be `"conda>=4.5.4"` (`conda update conda` should be enough).


Via pip:

* :
  ```
  pip install pandoctools pandoctools-ready
  ```
* Install latest stable [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref/releases) (compatible with pandoc version) to `<miniconda-path>/envs/myenv/bin`.


# Useful tips (reload imported modules in Hydrogen, R kernel, LyX)

[Useful tips](https://github.com/kiwi0fruit/pandoctools/blob/master/tips.md)


# Alternatives to R Markdown (Markdown-based Literate Programming)

[Alternatives to R Markdown](https://github.com/kiwi0fruit/pandoctools/blob/master/alternatives_to_r_markdown.md)
