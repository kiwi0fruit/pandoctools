# Feather Helper

Feather Helper helps to cache 2D numpy arrays and pandas dataframes. Usage example in Atom/Hydrogen:

```py
from pandoctools import feather as fh
# fh.setdir(r"%USERPROFILE%\feather\mydoc")
# %%
fh.name('id1')
try:
    # raise Exception  # <- this is a switch
    A, B, C = fh.pull()
except Exception as e:
    # calculate stuff
    fh.push(A, B, C, e=e)
```
