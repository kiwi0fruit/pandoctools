Pandoctools
===========

Pandoctools is a combination of tools that help write reproducible
markdown reports. They rely on Pandoc and Jupyter kernels.

Glueing part of pandoctools is a profile manager of text processing
pipelines. It stores short shell (bash or batch) scripts that define
chain operations over text. They are mostly Pandoc filters but any CLI
text filter is OK.

`**Introduction article about
Pandoctools** <https://github.com/kiwi0fruit/atom-jupyter-pandoc-markdown>`__.

Contents
========

-  `Notable parts of Pandoctools <#notable-parts-of-pandoctools>`__
-  `Examples markdown to ipynb <#examples-markdown-to-ipynb>`__
-  `Install <#install>`__
-  `Useful tips <#tips.md>`__

Notable parts of Pandoctools
============================

-  `**Pandoc** <https://pandoc.org/>`__,
   `**Jupyter** <http://jupyter.org/>`__,
   `**pandoc-crossref** <https://github.com/lierdakil/pandoc-crossref>`__
   (dependence) - classical tools.
-  `**Pandoctools CLI
   app** <https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/cli>`__:
   profile manager of text processing pipelines. It stores short shell
   (bash or batch) scripts - called profiles - that define chain
   operations over text. They are mostly Pandoc filters but any CLI text
   filter is OK. Profiles can be used to convert any document of choise
   in the specified manner.
-  `**Knitty** <https://github.com/kiwi0fruit/knitty>`__ (dependence):
   Knitty is another CLI for Stitch/Knotr: reproducible report
   generation tool via Jupyter, Pandoc and Markdown. Insert python code
   (or other Jupyter kernel code) to the Markdown document and have
   code’s results in the output document. Can even export to Jupyter
   ipynb notebooks.
-  `**SugarTeX** <https://github.com/kiwi0fruit/sugartex>`__
   (dependence): SugarTeX is a more readable LaTeX language extension
   and transcompiler to LaTeX.
-  `**Feather
   Helper** <https://github.com/kiwi0fruit/pandoctools/blob/master/pandoctools/feather>`__
   helps to cache 2D numpy arrays and pandas dataframes.
-  `**Matplotlib
   Helper** <https://github.com/kiwi0fruit/pandoctools/blob/master/pandoctools/matplotlib>`__
   is my custom helper to tune Matplotlib experience.

| Pandoctools is a tool for converting markdown document. But we also
  need tools for writing markdown and deploying python/Jupyter code
  blocks.
| And the best one for it is:

-  `**Atom editor with
   plugins** <https://github.com/kiwi0fruit/pandoctools/blob/master/atom.md>`__.
   It helps easily type Unicode, interactively run highlighed
   python/Jupyter code blocks and instantly see results (+ completions
   from the running Jupyter kernel), can convert basic pandoc markdown
   to html with live preview.
-  Must have plugins: `**SugarTeX
   Completions** <https://github.com/kiwi0fruit/pandoctools/blob/master/atom.md#sugartex-completions>`__,
   `**Unix
   Filter** <https://github.com/kiwi0fruit/pandoctools/blob/master/atom.md#unix-filter>`__,
   `**Hydrogen** <https://github.com/kiwi0fruit/pandoctools/blob/master/atom.md#hydrogen>`__,
   `**Markdown Preview
   Plus** <https://github.com/kiwi0fruit/pandoctools/blob/master/atom.md#markdown-preview-plus>`__

Examples markdown to ipynb
==========================

Here are
`**examples** <https://github.com/kiwi0fruit/pandoctools/blob/master/examples>`__
that demonstrate converting documents:

-  from markdown ``.md`` with Jupyter python code blocks, SugarTeX math
   and cross-references to ``ipynb`` notebook.
-  from Hydrogen/python notebook ``.py`` with Atom/Hydrogen code cells,
   Knitty markdown incerts (again with SugarTeX math and
   cross-references) to ``.ipynb`` notebook.

Install
=======

Windows:
--------

-  Install `Miniconda <https://conda.io/miniconda.html>`__
-  Install `Git together with Bash <https://git-scm.com/downloads>`__
   Git is needed for writing text conversion profiles in cross-platform
   bash language instead of Windows-only batch language (that is
   supported by Pandoctools anyway).

::

    conda install "conda>=4.5.4"
    conda create -n myenv python=3
    call activale myenv

    conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.0,<2.1" matplotlib feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future shutilwhich cython pywin32 pandas
    pip install panflute knitty sugartex winshell pandoctools

-  Install `pandoc-crossref
   v0.3.0.1 <https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.0.1>`__
   to
   ``<miniconda-path>/envs/myenv/Library/bin``.

Unix:
-----

-  Install `Miniconda <https://conda.io/miniconda.html>`__

::

    conda install "conda>=4.5.4"
    conda create -n myenv python=3
    source activate myenv

    conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.0,<2.1" matplotlib feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future shutilwhich cython pandas
    pip install panflute knitty sugartex pandoctools

-  Install `pandoc-crossref
   v0.3.0.1 <https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.0.1>`__
   to
   ``<miniconda-path>/envs/myenv/bin``.

Useful tips
===========

`Useful
tips <https://github.com/kiwi0fruit/pandoctools/blob/master/tips.md>`__
