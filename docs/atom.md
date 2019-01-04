# Atom editor

# Contents

* [Atom editor with full Unicode support](#atom-editor-with-full-unicode-support)
* [Atom packages for right Pandoctools experience](#atom-packages-for-right-pandoctools-experience)
    * [SugarTeX Completions](#sugartex-completions)
    * [Unix Filter](#unix-filter)
    * [Hydrogen](#hydrogen)
      * [Reload imported modules in Hydrogen](#reload-imported-modules-in-hydrogen)
    * [Markdown Preview Plus](#markdown-preview-plus)
* [Recommended Atom options](#recommended-atom-options)
* [Enable Atom spell checking](#enable-atom-spell-checking)
* [Useful Atom packages](#useful-atom-packages)


# Atom editor with full Unicode support

Highly recommended to install [Atom editor](https://atom.io/) as it's the best for markdown. Atom is perfect for Unicode rich texts. But you need to install some fonts and set font fall-back chains first. See [this instruction](https://github.com/kiwi0fruit/sugartex#atom-editor-with-full-unicode-support) in SugarTeX docs.


# Atom packages for right Pandoctools experience 

## SugarTeX Completions

Install [SugarTeX Completions](https://atom.io/packages/sugartex-completions) package for easy typing SugarTeX and lots of other Unicode characters. (it's incompatible with [latex-completions](https://atom.io/packages/latex-completions) package).

In the [SugarTeX documentation](https://github.com/kiwi0fruit/sugartex/blob/master/sugartex.md) appropriate shortcuts for SugarTeX Completions for Atom are given.


## Unix Filter

Install [Unix Filter](https://atom.io/packages/unix-filter) (>=0.0.2). It nicely runs on Windows too. It runs Pandoctools right from Atom and writes output file (though profile confirmation prompt is not shown). It's convenient to use it with [file-watcher](#useful-atom-packages).

Specify command option to `<...>\pandoctools.exe --stdin "%FILE%"` (`<...>/pandoctools --stdin "$FILE"` on Unix) where `<...>` is a path to pandoctools executable that can be learned from desktop shortcut. And **uncheck** "Replace Text" option.


## Hydrogen

Install [Hydrogen](https://atom.io/packages/hydrogen) (by nteract) Atom package that allows interactive python code execution. With it you can run and see instantly see results of code blocks that are later would be processed by Pandoctools/Knitty and be included to the output document.

See the [short instruction](https://github.com/kiwi0fruit/knitty/blob/master/docs/hydrogen.md) how to use and set up Hydrogen.


### Reload imported modules in Hydrogen

[Reload imported modules in Hydrogen](https://github.com/kiwi0fruit/pandoctools/blob/master/tips.md#reload-imported-modules-in-hydrogen)


## Markdown Preview Plus

Running Pandoctools can be slow since it uses Knitty (and hence starts and stops Jupyter every time) so the best approach when writing document with Pandoctools is to convert from enchanced Markdown to standard Pandoc Markdown (Knitty and all Pandoc filters run here). Then preview html/print pdf it with standard tool and plain Pandoc without filters.

And in my opinion the best tool for this is Markdown Peview Plus Atom package.

### Installation

* First install [Markdown Peview Plus](https://atom.io/packages/markdown-preview-plus) (>=3.3.1)
* Then patch MPP by copying files from [MPP patch](https://github.com/kiwi0fruit/misc/tree/master/src/mpp) to `%USERPROFILE%\.atom\packages\markdown-preview-plus\styles` folder (`%USERPROFILE%\.atom` is `~/.atom` on Linux). The patch overrides default css theme. It has `custom-fonts.less` file - tune it to change fonts of the theme.
* Make sure MPP settings are set to:
    * **Settings** (root) > **Renderer backend** is pandoc
    * **Math Options** > **Enable Math Rendering By Default** is checked
    * **Math Options** > **Math Renderer** is `HTML-CSS`
    * **Math Options** > **MathJax TeX Extensions** are `AMSmath.js, AMSsymbols.js, noErrors.js, noUndefined.js, HTML.js`
    * **Math Options** > **MathJax 'undefinedFamily' (font family)** is `'Libertinus Serif', 'PT Astra Serif', 'Libertinus Math', Tinos, 'STIX Two Math', 'Noto Serif', Symbola, 'Noto Serif CJK TC', serif`
    * **Pandoc settings** > **Path to Pandoc executable** set to pandoc exec that wasinstalled by conda/Miniconda: take path to pandoctools executable (from desktop shortcut for example) and replace `pandoctools` with `pandoc`
    * **Pandoc settings** > **Filters** set to empty string
    * **Pandoc settings** > **Commandline Arguments** set to empty string
    * **Pandoc settings** > **Markdown Flavor** set to simply `markdown`
    * **Pandoc settings** > **Citations** is unchecked (if you need it you can add it in Pandoctools more explicit CLI)
    * **Save to PDF options** > **Render background** turned ON

The MPP patch needs installed [serif](https://github.com/kiwi0fruit/open-fonts#best-serif) and [monospace](https://github.com/kiwi0fruit/open-fonts#best-monospace) fallback fonts chains from [Open fonts](https://github.com/kiwi0fruit/open-fonts). You can switch from serif to [sans serif](https://github.com/kiwi0fruit/open-fonts#best-sans-serif) if you want.

The patched CSS (less actually) theme is not ideal and still buggy but a lot better that default MMP theme. Suggestions and pull requests are welcomed.

PS: If you are interested in beautiful fonts and on Windows take a look at [MacType](https://github.com/kiwi0fruit/open-fonts#mactype) font rendering engine.


# Recommended Atom options

1. In **Settings** → **Editor** turn on **Soft Wrap** and **Soft Wrap At Preffered Line Length**. This setting is convenient for inspection of markdown code that was obtained from untrusted source,
2. Enable opening markdown files right from the Windows shell (from Explorer). In **Settings** → **System** turn on three checkboxes.
3. Sometimes some Atom packages break spell check and the clear install may be the easiest option. As stated [here](https://discuss.atom.io/t/how-to-completely-uninstall-atom-from-windows/17338) if on Windows in order to delete Atom completely you should uninstall it and then delete it's files from `%USERPROFILE%\.atom`, `%LOCALAPPDATA%\atom` and `%APPDATA%\Atom`.


# Enable Atom spell checking

As far as I know it works only with **language-gfm** (GitHub flavored Markdown package). May be I'm wrong though.

English spell checking works on Atom and I was able to make russian and english spell checking work simultaneously. In order to make it work you should specify something like `en-US, ru-RU` in **Locales** setting and `C:\Dictionaries` in **Locale Paths** setting of **spell-check** module (by _atom_). Then put `en_US.aff`, `en_US.dic`, `ru_RU.aff`, `ru_RU.dic` to that folder (you can download the [Hunspell dictionary](https://sourceforge.net/projects/hunspell/files/Spelling%20dictionaries/en_US/)). Or you can use dictionaries from LibreOffice like [Russian spellcheck dictionary](https://extensions.libreoffice.org/extensions/russian-spellcheck-dictionary.-based-on-works-of-aot-group). They can be found in `%PROGRAMFILES%\LibreOffice 5\share\extensions` or `%APPDATA%\LibreOffice\4\user` folders (you can search for `*.dic` files). I renamed `russian-aot.aff`, `russian-aot.dic` files to `ru_RU.aff`, `ru_RU.dic` and changed their encoding to UTF-8.


# Useful Atom packages

Optionally install some useful Atom packages:

* [**MagicPython**](https://atom.io/packages/MagicPython) (by *MagicStack*): syntax highlighter for cutting edge Python 3 (default Atom highlighter does not support Python 3).
* [**document-outline**](https://atom.io/packages/document-outline) (by *mangecoeur*): navigation sidebar with table of contents of markdown document when editing.
* [**character-table**](https://atom.io/packages/character-table) (by *klorenz*): insert any Unicode character via name search,
* [**charcode-display**](https://atom.io/packages/charcode-display) (by *yonchu*): display the code of the character under the current cursor position in the status bar.,
* [**markdown-table-editor**](https://atom.io/packages/markdown-table-editor) (by *susisu*): automatic markdown table editor/formatter,
* [**file-watcher**](https://atom.io/packages/file-watcher) (by *lwblackledge*): helps simultaneously open and edit files in two editors. To use it with PyCharm you should disable PyCharm "safe write" (**Settings → Appearance and Behavior → System Settings → Synchronization → Use "safe write"**).
* [**git-time-machine**](https://atom.io/packages/git-time-machine) (by *littlebee*): see difference with any older Git commit (if you add markdown document to the Git repository). This can be useful for authoring edits (7zip the whole repository and send).
* [**language-batchfile**](https://atom.io/packages/language-batchfile) (by *mmims*): syntax highlighting and snippets for batch files.
* [**highlight-bad-chars**](https://atom.io/packages/highlight-bad-chars) (by *ohanhi*): highlights some Unicode characters that can be confused with standard ANSI (like no-break spaces). The package might be buggy so you may need to periodically edit the file to make the package work.
