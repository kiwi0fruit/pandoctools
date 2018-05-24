# Matplotlib Helper

Matplotlib Helper is my custom helper to tune Matplotlib experience. I tuned fonts, made some tweaks to use it with SugarTeX, some tweaks to use mpl interactive plots in Atom/Hydrogen. Added export to raw markdown so it nicely works with [`results=pandoc` from Knitty](https://github.com/kiwi0fruit/knitty/blob/master/knitty.md#22-results-pandoc-chunk-option). Usage example in Atom/Hydrogen:

```py
from pandoctools import matplotlib as mh
mh.ready()
# mh.ready(KNITTY, font_size=14, finalize_=False)
# ... do additional tuning
# mh.finalize()

import matplotlib.pyplot as plt

# ... prepare plot
plt.figure(figsize=(w, w/mh.GR))
plt.ylabel(mh.stex('ˎ∇ ⋅ [ ⃗E]ˎ, V/m'))
# ...

print('''
![My beautiful figure]({}){{#fig:1}}
'''.format(mh.img(plt, qt=True)))
```
Qt backend gives [interactive plots in Atom/Hydrogen](https://nteract.gitbooks.io/hydrogen/docs/Usage/Examples.html#interactive-plots-using-matplotlib).
