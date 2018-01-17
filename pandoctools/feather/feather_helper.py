# %%
from pandoctools.feather import FeatherHelp

f = FeatherHelp('feather')


# %%
f.name('1')
try:
    # raise Exception
    A, B, C = f.pull()
except:
    # calculate stuff
    f.push(A, B, C)
