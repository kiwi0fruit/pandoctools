# Pandas Helper

Pandas Helper displays Data Frame and returns it's Markdown string. Usage example in Atom/Hydrogen:

`````py
# %% {md} """ %%% """ --------
"""
---
echo: False
...
```py
KNITTY = True
```
"""

# %% --------
import pandas as pd
import numpy as np
from pandoctools import pandas as dfh

df = pd.DataFrame(np.random.random(16).reshape(4, 4))

print(dfh.md_table(df, KNITTY))
print('')
print(': Table {#tbl:table1}')
`````
