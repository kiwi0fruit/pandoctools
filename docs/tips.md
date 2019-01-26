# Contents

* [Reload imported modules in Hydrogen](#reload-imported-modules-in-hydrogen)
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


# Install R

Create conda env (named "r"):

### on Unix:

```bash
conda create -c defaults -c conda-forge -n r r-essentials exec-wrappers
source activate r
R
```
```r
IRkernel::installspec()
quit()
```
Do the same as in Windows algorithm below.

### on Windows

```batch
conda create -n r r-essentials exec-wrappers
call activate r
R
```
```r
IRkernel::installspec()
quit()
```
```batch
where python.exe > __tmp__ && set /p pyexe=<__tmp__ && del __tmp__
set "env=%pyexe:~0,-11%"

where R.exe > __tmp__ && set /p Rexe=<__tmp__ && del __tmp__
set "Rdir=%Rexe:~0,-6%"

create-wrappers -t conda -b "%Rdir%" -f R -d "%env%\Scripts\wrap" --conda-env-dir "%env%"

set "ir=%APPDATA%\jupyter\kernels\ir"
python -c "print(r'%env%\Scripts\wrap\R.bat'.replace('\\', '/'))" >> "%ir%\kernel.json"
explorer "%ir%"
```
Edit `%APPDATA%\jupyter\kernels\ir\kernel.json`: cut the path at the last line and paste intead of the path.


# Install LyX

If you are not satisfied with [SugarTeX](sugartex.md) and standard LaTeX you may install [**LyX**](http://www.lyx.org/Download) that among other things is a WYSIWYM ("what you see is what you mean") LaTeX editor (which feels pretty much the same as WYSIWYG ("what you see is what you get")). LyX helps you write LaTeX formulas like in MS Word and then clipboard copy LaTeX code to your markdown text.

* In order to edit inline code again you need to copy the code together with two `$...$` and paste it into LyX inline formula object (**Insert** → **Inline Formula**).
* In order to edit formulas between `$$...$$` again you need to copy the code with only two `$...$` and paste it into LyX display formula object (**Insert** → **Display Formula**).
* **LyX** needs [**MiKTeX**](https://miktex.org/download). So you should install it as well (MiKTeX is bundled with one of the LyX installers).
* Tip: `Ctrl+Enter` creates a new line in LyX.


# Install Typescript

* First install [zeromq](https://github.com/zeromq/zeromq.js/). On Windows I used from source installation: 1) [Microsoft Visual C++ Build Tools 2015](http://go.microsoft.com/fwlink/?LinkId=691126) or [Build Tools for Visual Studio 2017](https://www.visualstudio.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15) (I don't remember which was installed) - check Windows 8.1 SDK and Windows 10 SDK options, 2) with `npm config set msvs_version 2015` and 3) creating conda environment for python 2: `conda create -n python2 python=2.7`,
* Then install [itypescript](https://www.npmjs.com/package/itypescript).

