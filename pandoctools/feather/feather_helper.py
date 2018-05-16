# %%
from pandoctools.feather import FeatherHelper

fh = FeatherHelper(dir='feather')
# dir=r"%USERPROFILE%\feather\document"
# dir="feather" same as
# dir="./feather" (default)


# %%
fh.name('1')
try:
    # raise Exception
    A, B, C = fh.pull()
except:
    # calculate stuff
    fh.push(A, B, C)
