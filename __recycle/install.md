# Recommended install

* Atom
* [SugarTeX Completions for Atom](https://github.com/kiwi0fruit/sugartex-completions)
* [Other useful Atom packages](https://github.com/kiwi0fruit/pandoctools/blob/master/tips.md#install-useful-atom-packages)

# Contents

* [Recommended install](#recommended-install)
  * [1 Atom editor with full Unicode support](#1-atom-editor-with-full-unicode-support)
  * [2 Recommended Atom options](#2-recommended-atom-options)
  * [3 Enable Atom spell checking](#3-enable-atom-spell-checking)
  * [4 Useful Atom packages](#4-useful-atom-packages)
  * [5 Pandoctools Atom Package](#5-pandoctools-atom-package)


## Recommended install

### 1 Atom editor with full Unicode support

Highly recommended to install [Atom editor](https://atom.io/) as it's the best for markdown.

Atom is perfect for Unicode rich texts. But you need to install some fonts first. Recommended font fallback chain for Windows (I guess I would use it on Linux too):

`Consolas, 'TeX Gyre Schola Math monospacified for Consolas', 'Symbola monospacified for Consolas', 'STIX Two Text', 'Segoe UI Symbol', 'Noto Sans Symbols', 'Noto Sans Symbols2', 'Microsoft JhengHei', 'Noto Sans CJK TC Thin', monospace`

Main part is choosing your favorite monospace font (`Consolas` in my case), then installing monospacified `TeX Gyre Schola Math` and `Symbola` from [monospacifier.py](https://github.com/cpitclaudel/monospacifier). Pick versions for your favorite monospace font. [STIX Two](http://www.stixfonts.org/) and [Noto](https://www.google.com/get/noto/) fonts can also be freely downloaded.

Consolas font can be installed with [PowerPoint Viewer](https://www.microsoft.com/en-us/download/details.aspx?id=13) (available for download till April 2018).


### 2 Recommended Atom options

1. In **Settings** → **Editor** turn on **Soft Wrap** and **Soft Wrap At Preffered Line Length**. This setting is convenient for inspection of markdown code that was obtained from untrusted source,
2. Enable opening markdown files right from the Windows shell (from Explorer). In **Settings** → **System** turn on three checkboxes.
3. Sometimes some Atom packages break spell check and the clear install may be the easiest option. As stated [here](https://discuss.atom.io/t/how-to-completely-uninstall-atom-from-windows/17338) if on Windows in order to delete Atom completely you should uninstall it and then delete it's files from `%USERPROFILE%\.atom`, `%LOCALAPPDATA%\atom` and `%APPDATA%\Atom`.


### 3 Enable Atom spell checking

As far as I know it works only with **language-gfm** (GitHub flavored Markdown package). May be I'm wrong though.

English spell checking works on Atom and I was able to make russian and english spell checking work simultaneously. In order to make it work you should specify something like `en-US, ru-RU` in **Locales** setting and `C:\Dictionaries` in **Locale Paths** setting of **spell-check** module (by _atom_). Then put `en_US.aff`, `en_US.dic`, `ru_RU.aff`, `ru_RU.dic` to that folder (you can download the [Hunspell dictionary](https://sourceforge.net/projects/hunspell/files/Spelling%20dictionaries/en_US/)). Or you can use dictionaries from LibreOffice like [Russian spellcheck dictionary](https://extensions.libreoffice.org/extensions/russian-spellcheck-dictionary.-based-on-works-of-aot-group). They can be found in `%PROGRAMFILES%\LibreOffice 5\share\extensions` or `%APPDATA%\LibreOffice\4\user` folders (you can search for `*.dic` files). I renamed `russian-aot.aff`, `russian-aot.dic` files to `ru_RU.aff`, `ru_RU.dic` and changed their encoding to UTF-8.


### 4 Useful Atom packages

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


### 5 Pandoctools Atom Package

Pandoctools Atom Package is still under development. As a temporal solution you can use [patched Markdown Preview Plus](https://github.com/kiwi0fruit/markdown-preview-plus) Atom Package. You can install it via:
```sh
apm install kiwi0fruit/markdown-preview-plus
```
(it's incompatible with original [markdown-preview-plus](https://atom.io/packages/markdown-preview-plus) and with default **markdown-preview** packages).

Then you can convert markdown to markdown via Pandoctools, then convert to html / preview via Markdown Preview Plus.

See [this](https://github.com/atom-community/markdown-preview-plus/issues/255) for details about possible bugs when using it with **pandoc-crossref** (that's the default setting).

Recommended serif font-family fallback chain for **Markdown Preview Plus**:

`'Times New Roman', 'STIX Two Text', 'Segoe UI Symbol', 'Noto Sans Symbols', 'Noto Sans Symbols2', 'Noto Serif CJK TC ExtraLight', serif`

[STIX Two](http://www.stixfonts.org/) and [Noto](https://www.google.com/get/noto/) fonts can be freely downloaded.

#### TODO
