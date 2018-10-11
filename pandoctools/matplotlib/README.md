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
# %% {md} """ %%% """
"""
---
pandoctools:
  profile: Default
results: pandoc
...
"""

# %% {results=hide} --------------------
from pandoctools import matplotlib as mh
mh.ready(font_size=14)  # should be run before import matplotlib.pyplot
import matplotlib.pyplot as plt


plt.figure(figsize=mh.figsize(w=6))
plt.plot([1, 2, 3, 4])
plt.ylabel(mh.stex('ˎ∇ ⋅ [ ⃗E]ˎ, V/m'))
img = mh.img(plt, qt=True)

# %% -----------------------------------
print('''
![My beautiful figure]({}){{#fig:1}}
'''.format(img))
```

Qt backend gives [interactive plots in Atom/Hydrogen](https://nteract.gitbooks.io/hydrogen/docs/Usage/Examples.html#interactive-plots-using-matplotlib).
