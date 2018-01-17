# %%
from pandoctools.feather import FeatherHelper

f = FeatherHelper(dir='feather')
# dir=r"%USERPROFILE%\feather\document"
# dir="feather" same as
# dir="./feather" (default)


# %%
f.name('1')
try:
    # raise Exception
    A, B, C = f.pull()
except:
    # calculate stuff
    f.push(A, B, C)
