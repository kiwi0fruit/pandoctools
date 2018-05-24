# Contents

* [Install useful Atom packages](#install-useful-atom-packages)
* [Install R](#install-r)
* [Install LyX](#install-lyx)


# Install useful Atom packages

Optionally install some useful Atom packages:

* [**MagicPython**](https://atom.io/packages/MagicPython) (by *MagicStack*): syntax highlighter for cutting edge Python 3 (default Atom highlighter does not support Python 3).
* [**document-outline**](https://atom.io/packages/document-outline) (by *mangecoeur*): navigation sidebar with table of contents of markdown document when editing.
* [**character-table**](https://atom.io/packages/character-table) (by *klorenz*): insert any Unicode character via name search,
* [**markdown-table-editor**](https://atom.io/packages/markdown-table-editor) (by *susisu*): automatic markdown table editor/formatter,
* [**file-watcher**](https://atom.io/packages/file-watcher) (by *lwblackledge*): helps simultaneously open and edit files in two editors. To use it with PyCharm you should disable PyCharm "safe write" (**Settings → Appearance and Behavior → System Settings → Synchronization → Use "safe write"**).
* [**git-time-machine**](https://atom.io/packages/git-time-machine) (by *littlebee*): see difference with any older Git commit (if you add markdown document to the Git repository). This can be useful for authoring edits (7zip the whole repository and send).
* [**language-batchfile**](https://atom.io/packages/language-batchfile) (by *mmims*): syntax highlighting and snippets for batch files.
* [**highlight-bad-chars**](https://atom.io/packages/highlight-bad-chars) (by *ohanhi*): highlights some Unicode characters that can be confused with standard ANSI (like no-break spaces). The package is buggy so you may need to periodically edit the file to make the package work. Optionally edit theme file: `%USERPROFILE%\.atom\packages\highlight-bad-chars\styles\highlight-bad-chars.atom-text-editor.less`. Fast way to open it is **Setting** → **Open Config Folder**. Then replace:

```less
.highlight-bad-chars .region {
  background-color: fadeout(@text-color-error, 85%);
  border: 1px solid @syntax-background-color;  // @text-color-error;
}
```

To remove/add characters from list edit `%USERPROFILE%\.atom\packages\highlight-bad-chars\lib\highlight-bad-chars.coffee`. For example to remove *diaeresis* and *broken bar* from the list and add `<>` doppelgangers edit this way:

```coffe
  #'\xA6', # Split vertical bar
  ...
  #'\xA8', # modifier - under curve
  '\u02C2',  # modifier letter left arrowhead
  '\u02C3',  # modifier letter right arrowhead
```


## Install R

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
