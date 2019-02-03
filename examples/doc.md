---
pandoctools:
  profile: Default
  out: "*.ipynb"
  # out: "*.pdf"
input: True
eval: False
error: raise
...

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

@{input=False}
```html
<p></p>
```

@{input=False, eval=True}
```py
from IPython.display import Markdown
import pandas as pd
import numpy as np
import tabulatehelper as th

df = pd.DataFrame(np.random.random(16).reshape(4, 4))

Markdown(f'''
{th.md_table(df)}
: Table {{#tbl:table1}}
''')
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
