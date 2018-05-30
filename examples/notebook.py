# %% {md} """ %%% """
"""
---
pandoctools:
  profile: Kiwi
  out: "%USERPROFILE%\\*.ipynb"
  # out: "*.py.md"
input: False
eval: True
echo: False
...
"""
# %% {echo=False, eval=True}
KNITTY = True
# %% {echo=False, eval=False}
KNITTY = False


# %% {md} Markdown cell that doesn't affect PyCharm code inspection and Atom+Hydrogen 'Run All':
"""
# Markdown to Jupyter notebook example

Here is a SugarTeX example with @eq:max and @fig:img.

See [PDF of this source](https://github.com/kiwi0fruit/sugartex/raw/master/sugartex.pdf) if you do not have [excellent Unicode support](https://github.com/kiwi0fruit/sugartex#atom-editor-with-full-unicode-support).


ˎˎ
˱∇ × [ ⃗B] - 1∕c ∂[ ⃗E]∕∂t ˳= 4π∕c [ ⃗j] ¦#
               ∇ ⋅ [ ⃗E]\ ˳= 4πρ       ¦
 ∇ × [ ⃗E] + 1∕c ∂[ ⃗B]∕∂t ˳= [ ⃗0]      ¦
               ∇ ⋅ [ ⃗B]\ ˳= 0         ˲
,ˎˎ{#eq:max}

where ˎ[ ⃗B], [ ⃗E], [ ⃗j]: ℝ⁴ → ℝ³ˎ – vector functions of the form
ˎ(t,x,y,z) ↦ [ ⃗f](t,x,y,z), [ ⃗f] = (f_˹x˺, f_˹y˺, f_˹z˺)ˎ.


![Sample image with cross-references.](https://avatars3.githubusercontent.com/u/19735117?s=460&v=4){#fig:img}

Image caption does not work but it can be fixed via simple Panflute filter. Or it can be considered Pandoc bug.
"""


# %% {echo=True, results=pandoc}
import pandas as pd
import numpy as np
from pandoctools import pandas as th

df = pd.DataFrame(np.random.random(16).reshape(4, 4))

print(th.md_table(df, KNITTY))
print(': Table {#tbl:table1}')


# %% {md}
"""
Text and @tbl:table1
"""


# %% {input=True, eval=False, echo=True}
import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.random(16).reshape(4, 4))
df


# %% {r, echo=True} R cell:
"""
# R cell:
x <- c(10, 20)
x[1]
"""


# %% {results=pandoc, echo=True}
import math
print('''

Markdown text with SugarTeX formula: ˎα^˱{pi:1.3f}˲ˎ.
It works because of the results=pandoc option and SugarTeX Pandoc filter.

'''.replace('ˎ', '$').format(pi=math.pi))


# %% {input=True, eval=False, echo=True}
print('Hello!')
