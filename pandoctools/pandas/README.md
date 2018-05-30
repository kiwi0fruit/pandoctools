# Pandas Helper

Pandas Helper displays Data Frame and returns it's Markdown string. Usage example that works both in Atom+Hydrogen and in Pandoctools+Knitty:

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


# %% ----------------------------
import pandas as pd
import numpy as np
from pandoctools import pandas as th

df = pd.DataFrame(np.random.random(16).reshape(4, 4))

print("""

{tbl}

: Table {{#tbl:table1}}

""".format(tbl=th.md_table(df, KNITTY)))
```
