# Pandas Helper

Pandas Helper displays Data Frame and returns it's Markdown string. Usage example that works both in Atom+Hydrogen and in Pandoctools+Knitty:

```py
"""
---
pandoctools:
  profile: Default
results: pandoc
...
"""


# %% ----------------------------
import pandas as pd
import numpy as np
from pandoctools import pandas as th

df = pd.DataFrame(np.random.random(16).reshape(4, 4))

print(f"""

{th.md_table(df)}

: Table {{#tbl:table1}}

""")
```
