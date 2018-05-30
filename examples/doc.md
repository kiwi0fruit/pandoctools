---
pandoctools:
  profile: Default
  out: "%USERPROFILE%\\*.ipynb"
  # out: "*.md.md"
input: True
eval: False
...
@{py, input=False, echo=False, eval=True}
```
KNITTY = True
```
@{input=False, echo=False}
```py
try:
    KNITTY
except:
    KNITTY = False
```

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

@{input=False, eval=True, results=pandoc}
```py
import pandas as pd
import numpy as np
from pandoctools import pandas as th

df = pd.DataFrame(np.random.random(16).reshape(4, 4))

print(th.md_table(df, KNITTY))
print(': Table {#tbl:table1}')
```

Text and @tbl:table1


```py
import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.random(16).reshape(4, 4))
df
```

# Title

Text and @tbl:table2

| a | b | c | d |
|---|---|---|---|
| 1 | 2 | 3 | 4 |

: Table {#tbl:table2}

```py
print('Hello!')
```
