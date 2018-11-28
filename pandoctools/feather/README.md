# Feather Helper

Feather Helper helps to cache 2D numpy arrays and pandas dataframes. Usage example in Atom/Hydrogen:

```py
from pandoctools import feather as fh
# fh.setdir("~/feather/mydoc")
# %%
fh.name('id1')
try:
    # raise Exception  # <- this is a switch
    A, B, C = fh.pull()
    # lst = fh.pull(len(lst))  # control len can be set
except Exception as e:
    # calculate stuff
    fh.push(A, B, C, e=e)
```
