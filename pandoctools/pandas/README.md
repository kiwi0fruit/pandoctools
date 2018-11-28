# Pandas Helper

Pandas Helper displays Data Frame and returns it's Markdown string. Usage example that works both in Atom+Hydrogen and in Pandoctools+Knitty:

```py
"""
---
pandoctools:
  profile: Default
...
"""


# %% ----------------------------
from IPython.display import Markdown
import pandas as pd
import numpy as np
from pandoctools import pandas as th

df = pd.DataFrame(np.random.random(16).reshape(4, 4))

# appended header is useful when very long table
# (can display `df.iloc[[0]]` in hydrogen)
Markdown(f"""

{th.md_table(df)}

: Table {{#tbl:table1}}

{th.md_header(df)}

""")
```
