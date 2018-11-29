# Feather Helper

Feather Helper helps to cache 2D numpy arrays and pandas dataframes. Usage example in Atom/Hydrogen:

```py
import pandas as pd
import numpy as np
from pandoctools import feather as fh
fh.setdir("~/feather/mydoc")  # optional

# %%
fh.name('id1')
try:
    # raise Exception  # <- this is a switch
    df, A = fh.pull()  # control length can be set: fh.pull(N)
except Exception as e:
    print('push')  # calculate stuff:
    df = pd.DataFrame(np.random.random(16).reshape(4, 4))
    A = df.values
    fh.push(df, A, e=e)

print(df, '\n', A)
```
