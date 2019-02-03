"""
---
pandoctools:
  profile: Kiwi
  out: "*.ipynb"
  # out: "*.pdf"
input: False
eval: True
echo: False
error: raise
...
"""

# %% Markdown cell that doesn't affect PyCharm code inspection and Atom+Hydrogen 'Run All':
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

In this version of Pandoc image caption @fig:img works but for some reason this text is not inside:

@{eval=False, echo=True}
```html
<p></p>
```
"""


# %% {echo=True}
from IPython.display import Markdown
import pandas as pd
import numpy as np
import tabulatehelper as th

df = pd.DataFrame(np.random.random(16).reshape(4, 4))

Markdown(f'''
{th.md_table(df)}
: Table {{#tbl:table1}}
''')


# %%
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

# %%
"""
# Header

@{echo=True}
```r
x <- c(10, 20)
x[1]
```
"""


# %% {echo=True}
import math
Markdown(f'''
Markdown text with SugarTeX formula: ˎα^˱{math.pi:1.3f}˲ˎ.
It works because of the Markdown display option and SugarTeX Pandoc filter.
''')


# %% {input=True, eval=False, echo=True}
print('Hello!')
