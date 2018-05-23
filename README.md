# Pandoctools

Pandoc profile manager (stores any CLI filter pipelines), CLI wrapper for Panflute, other helpers.

**Pandoctools is not finished yet!**

## Install

### Prepare:

```
conda create -n myenv python=3
source activate myenv
call activale myenv
```

### Install:

Windows:

Install [Miniconda](https://conda.io/miniconda.html).
```
conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.0,<2.1" matplotlib feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future shutilwhich pywin32 pyperclip
pip install panflute knitty sugartex winshell
pip install git+https://github.com/kiwi0fruit/pandoctools.git
```
Then install [pandoc-crossref v0.3.0.1](https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.0.1) to  
`<miniconda-path>/envs/myenv/Library/bin`.

### Unix:

Install [Miniconda](https://conda.io/miniconda.html).
```
conda install -c defaults -c conda-forge "pip>=10.0.1" "pandoc>=2.0,<2.1" matplotlib feather-format jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters pypandoc click psutil nbformat pandoc-attributes six pyyaml notebook jupyter future shutilwhich
pip install panflute knitty sugartex
pip install git+https://github.com/kiwi0fruit/pandoctools.git
```
Then install [pandoc-crossref v0.3.0.1](https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.0.1) to  
`<miniconda-path>/envs/myenv/bin`.
