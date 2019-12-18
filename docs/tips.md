# Contents

* [Reload imported modules in Hydrogen](#reload-imported-modules-in-hydrogen)
* [Install Python kernel](#install-python-kernel)
* [Install R kernel](#install-r-kernel)
* [Install Typescript kernel](#install-typescript-kernel)


# Reload imported modules in Hydrogen

It may be useful to have an external module with Hydrogen. Import it to make the code more elegant. But you need to reload it after you change it. More to say: you need to reload every sub-import:

Hydrogen `./document.py`:

```py
from importlib import reload
import the
reload(the)
from the import something  # noqa E402
```

Module `./the/__init__.py`:

```py
from importlib import reload
from . import smth
reload(smth); del smth

from .smth import something  # noqa E402
```

Module `./the/smth.py`:

```py
def something():
  pass
```


# Install Python kernel

### Crossplatform installation:

(If on Windows first install [Git together with Bash](https://git-scm.com/downloads))

Create conda env (for example named "python3". Set another value to the `$kernel` environment variable if you need to):

```bash
kernel=python3

conda create -c defaults -c conda-forge -n "$kernel" "python>=3.6" ipykernel exec-wrappers
source activate "$kernel"
python -m ipykernel install --user --name "$kernel"

exec=python
execdir="$(dirname "$(type -p "$exec")")"
if [[ "$OSTYPE" == "msys" ]]; then
    # works for <env>/exec
    env="$execdir"
    wrap="$execdir/Scripts/wrap/$exec"
else
    # works for <env>/bin/exec
    env="$(dirname "$execdir")"
    wrap="$execdir/wrap/$exec"; fi

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



# Install R kernel

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


# Install Typescript kernel

* First install [zeromq](https://github.com/zeromq/zeromq.js/). On Windows I used from source installation: 1) [Microsoft Visual C++ Build Tools 2015](http://go.microsoft.com/fwlink/?LinkId=691126) or [Build Tools for Visual Studio 2017](https://www.visualstudio.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15) (I don't remember which was installed) - check Windows 8.1 SDK and Windows 10 SDK options, 2) with `npm config set msvs_version 2015` and 3) creating conda environment for python 2: `conda create -n python2 python=2.7`,
* Then install [itypescript](https://www.npmjs.com/package/itypescript).

