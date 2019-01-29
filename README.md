# Pandoctools

Pandoctools is a combination of tools that help write reproducible markdown reports. They rely on Pandoc and Jupyter kernels.

**Introduction articles**:

* [**Best Python/Jupyter/PyCharm experience + report generation with Pandoc filters**](https://github.com/kiwi0fruit/pandoctools/blob/master/docs/best_python_jupyter_pycharm_experience.md).
* [**Convenient and easily tweakable Atom+Markdown+Pandoc+Jupyter experience (can export to ipynb)**](https://github.com/kiwi0fruit/pandoctools/blob/master/docs/atom_jupyter_pandoc_markdown.md).  


“Glueing” part of pandoctools is a profile manager of text processing pipelines. It stores short crossplatform bash scripts that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK.


## Update instructions

(*Update instructions to v.1.4.2*)

* Switch to bash profiles as batch profiles are no longer supported (and install bash if needed),
* `results=pandoc` was a misunderstanding. The right way to output Markdown is to use  
  `from IPython.display import Markdown; Markdown('hello')`.
* Import pandas, matplotlib and feather helpers from separate modules: [matplotlibhelper](https://github.com/kiwi0fruit/matplotlibhelper), [featherhelper](https://github.com/kiwi0fruit/featherhelper), [tabulatehelper](https://github.com/kiwi0fruit/tabulatehelper),
* **v1.4.2** is not backward compatible but profiles can be easily fixed. Uninstall Pandoctools before updating. Update your custom bash scripts as names and logic changed. References: [**Default_args**](https://github.com/kiwi0fruit/pandoctools/blob/master/pandoctools/sh/Default_args), [**Default**](https://github.com/kiwi0fruit/pandoctools/blob/master/pandoctools/sh/Default) (profile), [**Default_pipe**](https://github.com/kiwi0fruit/pandoctools/blob/master/pandoctools/sh/Default_pipe).
* Since **v1.4.2** bash on Windows first rearched in the python environment, then in the $PATH, then
by path from config, then in the `%PROGRAMFILES%\Git`.


# Contents

* [Pandoctools](#pandoctools)
  * [Update instructions](#update-instructions)
* [Contents](#contents)
* [Notable parts of Pandoctools](#notable-parts-of-pandoctools)
* [Examples](#examples)
* [Install](#install)
* [Useful tips (reload imported modules in Hydrogen, Python kernel, R kernel, Typescript kernel)](#useful-tips-reload-imported-modules-in-hydrogen-python-kernel-r-kernel-typescript-kernel)
* [Alternatives to R Markdown (Markdown-based Literate Programming)](#alternatives-to-r-markdown-markdown-based-literate-programming)


# Notable parts of Pandoctools

* [**Pandoc**](https://pandoc.org/), [**Jupyter**](http://jupyter.org/), [**pandoc-crossref**](https://github.com/lierdakil/pandoc-crossref) (dependence) - classical tools.
* [**Pandoctools CLI app**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/cli): profile manager of text processing pipelines. It stores short bash scripts - called profiles - that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK. Profiles can be used to convert any document of choise in the specified manner.
* [**Knitty**](https://github.com/kiwi0fruit/knitty) (dependence): Knitty is a Pandoc filter and another CLI for Stitch/Knotr: reproducible report generation tool via Jupyter, Pandoc and Markdown. Insert python code (or other Jupyter kernel code) to the Markdown document and have code's results in the output document. Can even export to Jupyter ipynb notebooks. You can use [ipynb-py-convert](https://github.com/kiwi0fruit/ipynb-py-convert) to convert .ipynb to .py to use with Knitty.
* [**SugarTeX**](https://github.com/kiwi0fruit/sugartex) (dependence): SugarTeX is a more readable LaTeX language extension and transcompiler to LaTeX.
* [**Pyppdf**](https://github.com/kiwi0fruit/pyppdf) (dependence): Pyppeteer PDF. Prints html output to pdf via patched Pyppeteer.
* (*optional*) [**Tabulate Helper**](https://github.com/kiwi0fruit/tabulatehelper) converts tabular data like Pandas dataframe to GitHub Flavored Markdown pipe table.
* (*optional*) [**Matplotlib Helper**](https://github.com/kiwi0fruit/matplotlibhelper): custom helper to tune Matplotlib experience in Atom/Hydrogen and Pandoctools/Knitty.
* (*optional*) [**Feather Helper**](https://github.com/kiwi0fruit/featherhelper): concise interface to cache numpy arrays and pandas dataframes.

Pandoctools is a tool for converting markdown document. But we also need tools for writing markdown and deploying python/Jupyter code blocks.  
And the best one for it is:

* [**Atom editor with plugins**](https://github.com/kiwi0fruit/pandoctools/blob/master/docs/atom.md). It helps easily type Unicode, interactively run highlighed python/Jupyter code blocks and instantly see results (+ completions from the running Jupyter kernel), can convert basic pandoc markdown to html with live preview.
* Must have plugins: [**SugarTeX Completions**](https://github.com/kiwi0fruit/pandoctools/blob/master/docs/atom.md#sugartex-completions), [**Unix Filter**](https://github.com/kiwi0fruit/pandoctools/blob/master/docs/atom.md#unix-filter), [**Hydrogen**](https://github.com/kiwi0fruit/pandoctools/blob/master/docs/atom.md#hydrogen), [**Markdown Preview Plus**](https://github.com/kiwi0fruit/pandoctools/blob/master/docs/atom.md#markdown-preview-plus)


# Examples

Here are [**examples**](https://github.com/kiwi0fruit/pandoctools/blob/master/examples) that demonstrate converting documents:

* from markdown `.md` with Jupyter python code blocks, SugarTeX math and cross-references to `ipynb` notebook.
* from Hydrogen/python notebook `.py` with Atom/Hydrogen code cells, Knitty markdown incerts (again with SugarTeX math and cross-references) to `.ipynb` notebook.

**Examples are given for to .ipynb conversion but Pandoctools surely capable of conversion to .html, .pdf, .md.md or any Pandoc output format.**

Extras:

* If you need to capture Matplotlib plots please see [matplotlibhelper](https://github.com/kiwi0fruit/matplotlibhelper) (the approach showed in examples there can be used with other plot libraries).
* If you need to autonumber sections see [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref) or [this SE question](https://stackoverflow.com/questions/48434961/how-to-customise-section-headings-to-start-with-letters-in-r-markdown)


# Install

**If you have an antivirus then the first or two runs may fail - there may be errors like "Permission denied" because of the antivirus checking all the components.**

### Via conda

* (*on Windows*) Install 64-bit [Git together with Bash](https://git-scm.com/downloads),
* Install 64-bit [Miniconda3](https://conda.io/miniconda.html) (≥3.6),
* (*on Windows*) Creating "pandoctools" conda environment:
  ```bat
  call activate root
  conda update conda
  conda create -n pandoctools -c defaults -c conda-forge "pandoctools>=1.4.5"
  call activate pandoctools
  pandoctools-ready
  ```
* (*on Unix*) Creating "pandoctools" conda environment:
  ```bash
  source activate root
  conda update conda
  conda create -n pandoctools -c defaults -c conda-forge "pandoctools>=1.4.5"
  source activate pandoctools
  pandoctools-ready
  ```
* The significant commands are the following:
  ```bash
  conda install -c defaults -c conda-forge "pandoctools>=1.4.5"
  pandoctools-ready
  ```
  But it's recommended to create a dedicated conda environment for the Pandoctools.


### Via pip

* (*on Windows*) Install [Git together with Bash](https://git-scm.com/downloads),
* Install [Pandoc](https://pandoc.org/installing.html) (maybe pip would also install it but I'm not sure),
* Install latest stable [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref/releases) (compatible with pandoc version) to the dedicated virtual environment's `.\Scripts` (Windows) or `./bin` (Unix) folder.
* Install Pandoctools:
  ```bash
  pip install pandoctools
  pandoctools-ready
  ```


# Useful tips (reload imported modules in Hydrogen, Python kernel, R kernel, Typescript kernel)

[Useful tips](https://github.com/kiwi0fruit/pandoctools/blob/master/docs/tips.md)


# Alternatives to R Markdown (Markdown-based Literate Programming)

[Alternatives to R Markdown](https://github.com/kiwi0fruit/pandoctools/blob/master/docs/alternatives_to_r_markdown.md)
