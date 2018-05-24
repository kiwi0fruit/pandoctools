# Contents

* [Install R](#install-r)
* [Install LyX](#install-lyx)


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
