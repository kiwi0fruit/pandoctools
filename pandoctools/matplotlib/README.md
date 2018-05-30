# Matplotlib Helper

Matplotlib Helper is my custom helper to tune Matplotlib experience. I tuned fonts, made some tweaks to use it with SugarTeX, some tweaks to use mpl interactive plots in Atom/Hydrogen. Added export to raw markdown so it nicely works with [`results=pandoc` from Knitty](https://github.com/kiwi0fruit/knitty/blob/master/knitty.md#22-results-pandoc-chunk-option). Usage example that works both in Atom+Hydrogen and in Pandoctools+Knitty:

```py
# %% {md} """ %%% """
"""
---
pandoctools:
  profile: Default
  out: "*.*.md"
results: pandoc
...
"""
# %% {echo=False, eval=True}
KNITTY = True
# %% {echo=False, eval=False}
# noinspection PyRedeclaration
KNITTY = False


# %% {results=hide} ----------------------------
from pandoctools import matplotlib as mh
mh.ready(KNITTY)
# mh.ready(KNITTY, font_size=14, finalize=False)
# ... do additional tuning
# mh.finalize()

import matplotlib.pyplot as plt
w = 6
plt.figure(figsize=(w, w/mh.GR))
plt.plot([1,2,3,4])
plt.ylabel(mh.stex('ˎ∇ ⋅ [ ⃗E]ˎ, V/m'))
img = mh.img(plt, qt=True)
# %%
print('''
![My beautiful figure]({}){{#fig:1}}
'''.format(img))
```
Qt backend gives [interactive plots in Atom/Hydrogen](https://nteract.gitbooks.io/hydrogen/docs/Usage/Examples.html#interactive-plots-using-matplotlib).
