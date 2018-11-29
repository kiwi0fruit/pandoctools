# Matplotlib Helper

Matplotlib Helper is my custom helper to tune Matplotlib experience. I tuned fonts, made some tweaks to use it with SugarTeX, some tweaks to use mpl interactive plots in Atom/Hydrogen. Added export to raw markdown so it nicely works with [`results=pandoc` from Knitty](https://github.com/kiwi0fruit/knitty/blob/master/knitty.md#22-results-pandoc-chunk-option).

Can export plots with unicode to SVG or PNG. See default fonts in default keyword arguments of `ready()`.

Hints:

1. [MJ fonts](https://github.com/kiwi0fruit/open-fonts/tree/master/Fonts/MJ/oft).
2. Delete `fontList.cache`, `fontList.py3k.cache` or `fontList.json` from `%USERPROFILE%\.matplotlib` folder after installing a new font.
3. If font becomes bold without a reason try ([source](https://github.com/matplotlib/matplotlib/issues/5574)):

```py
from matplotlib import font_manager
if 'roman' in font_manager.weight_dict:
    del font_manager.weight_dict['roman']
    # noinspection PyProtectedMember
    font_manager._rebuild()
```

4. Install [Computer Modern Unicode](https://sourceforge.net/projects/cm-unicode/) for bold-italic unicode support: `"mathtext.sf": "CMU Serif:bold:italic"`. Sans-serif command `\mathsf{}` is reassigned because sans-serif font is rarely used in serif docs.


Usage example that works both in Atom+Hydrogen and in Pandoctools+Knitty:

```py
"""
---
pandoctools:
  profile: Default
...
"""

# %% --------------------
from IPython.display import Markdown
from pandoctools import matplotlib as mh
mh.ready(font_size=14)  # should be run before import matplotlib.pyplot
import matplotlib.pyplot as plt


plt.figure(figsize=mh.figsize(w=6))
plt.plot([1, 2, 3, 4])
plt.ylabel(mh.stex('ˎ∇ ⋅ [ ⃗E]ˎ, V/m'))

# this code in knitty would be parsed by pandoc:
Markdown(f'![My beautiful figure]({mh.img(plt)}){{#fig:1}}')
```

Qt backend gives [interactive plots in Atom/Hydrogen](https://nteract.gitbooks.io/hydrogen/docs/Usage/Examples.html#interactive-plots-using-matplotlib).

You may need to install to use in Jupyter Lab:

```
conda install jupyterlab jupyterlab_server tk nodejs
pip install ipympl
jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-matplotlib
```
Instead of `pip install ipympl` you can also try:
```
conda update --all
conda install -c defaults -c conda-forge ipympl
conda update --all
```
