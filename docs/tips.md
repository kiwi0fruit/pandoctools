# Contents

* [Reload imported modules in Hydrogen](#reload-imported-modules-in-hydrogen)
* [Install Python kernel](#install-python-kernel)
* [Install R](#install-r)
* [Install LyX](#install-lyx)
* [Install Typescript](#install-typescript)


# Reload imported modules in Hydrogen

It may be useful to have an external module with Hydrogen. Import it to make the code more elegant. But you need to reload it after you change it. More to say: you need to reload every sub-import:

Hydrogen `./document.py`:

```py
from importlib import reload
import the
reload(the)
from the import something
```

Module `./the/__init__.py`:

```py
from importlib import reload
from . import smth
reload(smth); del smth

from .smth import something
```

Module `./the/smth.py`:

```py
def something():
  pass
```


# Install Python kernel

### Crossplatform installation:

(If on Windows first install [Git together with Bash](https://git-scm.com/downloads))

Create conda env (named "python3"):

```bash
conda create -c defaults -c conda-forge -n python3 "python>=3.6" ipykernel exec-wrappers
source activate python3
python -m ipykernel install --user
# kernale name would be the env name

exec=python
kernel=python3
execdir="$(dirname "$(type -p "$exec")")"
 
```

* On Unix (works for `<env>/bin/exec`):
  ```bash
  env="$(dirname "$execdir")"
  wrap="$execdir/wrap/$exec"
   
  ```
* On Windows (`works for <env>/exec`):
  ```bash
  env="$execdir"
  wrap="$execdir/Scripts/wrap/$exec"
   
  ```

```
create-wrappers -t conda -b "$execdir" -f "$exec" -d "$(dirname "$wrap")" --conda-env-dir "$env"

if [[ "$OSTYPE" == "msys" ]]; then
    pref="$(cygpath "$APPDATA")/jupyter"
    wrap="$(cygpath -w "$wrap").bat"
elif [[ "$OSTYPE" =~ ^darwin ]]; then
    pref="$HOME/Library/Jupyter"
else
    pref="$HOME/.local/share/jupyter"; fi
export wrap="$wrap"
export kernelpath="$pref/kernels/$kernel/kernel.json"

cat "$kernelpath" | python -c "import json; import sys; import os; \
f = open(os.environ['kernelpath'], 'w'); dic = json.loads(sys.stdin.read()); \
dic['argv'][0] = os.environ['wrap'].replace(chr(92), '/'); \
json.dump(dic, f); f.close()"
 
```



# Install R

This is an instruction how to install R via conda. It's a not a standard way of having R so if you stray too far from packages provided by conda you might have [**problems**](https://community.rstudio.com/t/using-r-and-conda/10960).

You can also try creating env and installing packages with `--copy` option so that installing R packages natively won't break too much.

Create conda env (named "r"):

### Crossplatform installation:

(If on Windows first install [Git together with Bash](https://git-scm.com/downloads))

```bash
conda create -c defaults -c conda-forge -n r r-essentials exec-wrappers
source activate r
R -e "IRkernel::installspec()" --no-save >/dev/null
 
```

```bash
exec=R
kernel=ir

# works for <env>/bin/exec
execdir="$(dirname "$(type -p "$exec")")"
env="$(dirname "$execdir")"
wrap="$execdir/wrap/$exec"

create-wrappers -t conda -b "$execdir" -f "$exec" -d "$(dirname "$wrap")" --conda-env-dir "$env"

if [[ "$OSTYPE" == "msys" ]]; then
    pref="$(cygpath "$APPDATA")/jupyter"
    wrap="$(cygpath -w "$wrap").bat"
elif [[ "$OSTYPE" =~ ^darwin ]]; then
    pref="$HOME/Library/Jupyter"
else
    pref="$HOME/.local/share/jupyter"; fi
export wrap="$wrap"
export kernelpath="$pref/kernels/$kernel/kernel.json"

cat "$kernelpath" | python -c "import json; import sys; import os; \
f = open(os.environ['kernelpath'], 'w'); dic = json.loads(sys.stdin.read()); \
dic['argv'][0] = os.environ['wrap'].replace(chr(92), '/'); \
json.dump(dic, f); f.close()"
 
```


### Windows only installation

```batch
conda create -c defaults -c conda-forge -n r r-essentials exec-wrappers
call activate r
R -e "IRkernel::installspec()" --no-save > NUL

```

```batch
:: <env>\Scripts\R.exe
where R.exe > __tmp__ && set /p Rexe=<__tmp__ && del __tmp__
set "Rdir=%Rexe:~0,-6%"
set "env=%Rdir:~0,-8%"

create-wrappers -t conda -b "%Rdir%" -f R -d "%Rdir%\wrap" --conda-env-dir "%env%"

set "Rwrap=%Rdir%\wrap\R.bat"
set "ir=%APPDATA%\jupyter\kernels\ir\kernel.json"

type "%ir%" | python -c "import json; import sys; import os; f = open(os.environ['ir'], 'w'); dic = json.loads(sys.stdin.read()); dic['argv'][0] = os.environ['Rwrap'].replace('\\', '/'); json.dump(dic, f); f.close()"
 
```


# Install LyX

If you are not satisfied with [SugarTeX](sugartex.md) and standard LaTeX you may install [**LyX**](http://www.lyx.org/Download) that among other things is a WYSIWYM ("what you see is what you mean") LaTeX editor (which feels pretty much the same as WYSIWYG ("what you see is what you get")). LyX helps you write LaTeX formulas like in MS Word and then clipboard copy LaTeX code to your markdown text.

* In order to edit inline code again you need to copy the code together with two `$...$` and paste it into LyX inline formula object (**Insert** → **Inline Formula**).
* In order to edit formulas between `$$...$$` again you need to copy the code with only two `$...$` and paste it into LyX display formula object (**Insert** → **Display Formula**).
* **LyX** needs [**MiKTeX**](https://miktex.org/download). So you should install it as well (MiKTeX is bundled with one of the LyX installers).
* Tip: `Ctrl+Enter` creates a new line in LyX.


# Install Typescript

* First install [zeromq](https://github.com/zeromq/zeromq.js/). On Windows I used from source installation: 1) [Microsoft Visual C++ Build Tools 2015](http://go.microsoft.com/fwlink/?LinkId=691126) or [Build Tools for Visual Studio 2017](https://www.visualstudio.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15) (I don't remember which was installed) - check Windows 8.1 SDK and Windows 10 SDK options, 2) with `npm config set msvs_version 2015` and 3) creating conda environment for python 2: `conda create -n python2 python=2.7`,
* Then install [itypescript](https://www.npmjs.com/package/itypescript).

