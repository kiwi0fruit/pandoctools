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

In order to get R language support you may need to install [**language-r**](https://atom.io/packages/language-r) package for Atom. And actually install R. This is what I did:

1. Installed [**R**](https://cran.r-project.org/). For example to `%APPDATA%\R`,
2. Installed [**RStudio**](https://www.rstudio.com/products/rstudio/download/),
3. Run `setx -m R_HOME %APPDATA%\R` in command prompt with administrator privileges (I don't remember if it's necessary).
4. Installed [**IRkernel**](https://irkernel.github.io/installation/) from RStudio that was started in the context of `the_env` python environment. To do so run `call activate the_env` (`. activate the_env` on Unix) and then start `"%PROGRAMFILES%\RStudio\bin\rstudio.exe"` (I assume it's x64 version of RStudio on x64 Windows so `%PROGRAMFILES%` instead of `%PROGRAMFILES(x86)%`).

**Tip**: If on Windows and you didn't add python to `PATH` during installation you can modify `PATH` in console. For example:
```bat
set PYTHONPATH=<some path>\Miniconda
set PATH=%PYTHONPATH%;%PYTHONPATH%\Scripts;%PYTHONPATH%\Library\bin;%PATH%
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

