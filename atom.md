# Atom editor

# Contents

* [Atom editor with full Unicode support](#atom-editor-with-full-unicode-support)
* [SugarTeX Completions for Atom](#sugartex-completions-for-atom)
* [Unix Filter](#unix-filter)
* [Hydrogen](#hydrogen)
* [Markdown Preview Plus](#markdown-preview-plus)
* [Recommended Atom options](#recommended-atom-options)
* [Enable Atom spell checking](#enable-atom-spell-checking)
* [Useful Atom packages](#useful-atom-packages)


# Atom editor with full Unicode support

Highly recommended to install [Atom editor](https://atom.io/) as it's the best for markdown. Atom is perfect for Unicode rich texts. But you need to install some fonts and set font fall-back chains first. See [this instruction](https://github.com/kiwi0fruit/sugartex#atom-editor-with-full-unicode-support) in SugarTeX docs.


# SugarTeX Completions for Atom

[SugarTeX Completions for Atom](https://github.com/kiwi0fruit/sugartex-completions) is an Atom package for easy typing SugarTeX and lots of other Unicode characters. At the moment it can be installed via:

```sh
apm install kiwi0fruit/sugartex-completions --production
```
(it's incompatible with [latex-completions](https://atom.io/packages/latex-completions) package).

In the [SugarTeX documentation](https://github.com/kiwi0fruit/sugartex/blob/master/sugartex.md) appropriate shortcuts for SugarTeX Completions for Atom are given.


# Unix Filter

[**Patched** version of Unix Filter](https://github.com/kiwi0fruit/atom-unix-filter). It runs Pandoctools right from Atom and writes output file (though profile confirmation prompt is not shown). It's convenient to use it with [file-watcher](#useful-atom-packages).

Install:

```sh
apm install kiwi0fruit/atom-unix-filter --production
```

Specify command option to `<...>\pandoctools.exe --stdin` (`<...>/pandoctools --stdin` on Unix) where `<...>` is a path to pandoctools executable that can be learned from desktop shortcut.


# Hydrogen

#### TODO


# Markdown Preview Plus

Then you can convert markdown to markdown via Pandoctools, then convert to html / preview via Markdown Preview Plus.

See [recommended serif font-family fallback chain](https://github.com/kiwi0fruit/open-fonts#best-serif) for **Markdown Preview Plus**.

#### TODO


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
