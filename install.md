# Install

# Contents

* [Contents](#contents)
* [1. Install Pandoc](#1-install-pandoc)
* [2. Install Pandoctools python module](#2-install-pandoctools-python-module)
  * [2.1 Installation in details](#21-installation-in-details)
* [3. Install Pandoctools shell scripts](#3-install-pandoctools-shell-scripts)
* [4. Recommended install](#4-recommended-install)
  * [4.1 Atom editor with full Unicode support](#41-atom-editor-with-full-unicode-support)
  * [4.2 Recommended Atom options](#42-recommended-atom-options)
  * [4.3 Enable Atom spell checking](#43-enable-atom-spell-checking)
  * [4.4 SugarTeX Completions for Atom](#44-sugartex-completions-for-atom)
  * [4.6 Pandoctools Atom Package](#46-pandoctools-atom-package)


## 1. Install Pandoc

Pandoctools needs installed [**Pandoc**](https://github.com/jgm/pandoc/releases). It needs Pandoc to be available from command prompt. Check: `pandoc --help`. It should work if you installed it with default settings.

Tip: Pandoc ≥ 2.0 is needed for proper Knotr output re-processing (for toolchain: `f.md` → `f.md.md` → `f.md.md.html`).

Highly recommended installation of [**pandoc-crossref**](https://github.com/lierdakil/pandoc-crossref/releases) (copy it to the `%PROGRAMFILES(x86)%\Pandoc` or `%PROGRAMFILES%\Pandoc`).

See [Using Pandoc](tips.md#using-pandoc).


## 2. Install Pandoctools python module


### 2.1 Install via pip

```sh
pip install pandoctools
```

or from GitHub:
```sh
pip install git+https://github.com/kiwi0fruit/pandoctools.git
```
In this case you need to have installed [**Git**](https://git-scm.com/downloads) available from command prompt.


### 2.2 Install via conda for Anaconda

If you use pip for all python packages management then previous commands would work without problems.

But if you use conda (in Anaconda or Miniconda) for python packages management then some additional actions should be made.

I prefer conda because of the fast and easy binaries support on Windows. So the instructions from the beginning:

Install [**Anaconda**](https://www.continuum.io/downloads) or [**Miniconda**](https://conda.io/miniconda.html). I assume that you have `conda` and `activate` scripts available from the command line. This is the case when you install Anaconda or Miniconda with default settings or you know what you are doing.

Run:

```sh
conda install -c defaults -c conda-forge -c kiwi0fruit pandoctools-pip
pip install pandoctools
```

pip will install `shutilwhich` and `panflute` as well.

Or create environment from scratch:

```sh
conda create -n pandoctools -c defaults -c conda-forge -c kiwi0fruit python=3 pandoctools-pip
activate pandoctools
pip install pandoctools
```

Another way to create environment with `the_env.yml`:

```sh
conda env create -f "the_env.yml"
```

```yaml
name: the_env
channels:
  - defaults
  - conda-forge
  - kiwi0fruit
dependencies:
  - python=3
  - pandoctools-pip
  - pip:
    - pandoctools
```

Then you would need to activate `the_env` environment in order to use Pandoctools: `activate the_env`.

**Note** that if you call `conda` or `activate` from a shell script you need to add `call activate the_env` on Windows / `source activate the_env` on Linux/Unix.

**Tip**: If on Windows and you didn't add python to `PATH` during installation you can modify `PATH` each time in console. For example:
```bat
set PYTHONPATH=<some path>\Miniconda
set PATH=%PYTHONPATH%;%PYTHONPATH%\Scripts;%PYTHONPATH%\Library\bin;%PATH%
```


## 3. Install Pandoctools shell scripts

Download the latest zip from [Pandoctools releases](https://github.com/kiwi0fruit/pandoctools/releases).

Copy `pandoctools-0.*/bash/pandoc/pandoctools` folder to the `%APPDATA%\pandoc` (on Windows) or `$HOME/.pandoc` (on Unix).


## 4. Recommended install:

### 4.1 Atom editor with full Unicode support

Highly recommended to install [Atom editor](https://atom.io/) as it's the best for markdown.

Atom is perfect for Unicode rich texts. But you need to install some fonts first. Recommended font fallback chain for Windows (I guess I would use it on Linux too):

`Consolas, 'TeX Gyre Schola Math monospacified for Consolas', 'Symbola monospacified for Consolas', 'STIX Two Text', 'Segoe UI Symbol', 'Noto Sans Symbols', 'Noto Sans Symbols2', 'Microsoft JhengHei', 'Noto Sans CJK TC Thin', monospace`

Main part is choosing your favorite monospace font (`Consolas` in my case), then installing monospacified `TeX Gyre Schola Math` and `Symbola` from [monospacifier.py](https://github.com/cpitclaudel/monospacifier). Pick versions for your favorite monospace font. [STIX Two](http://www.stixfonts.org/) and [Noto](https://www.google.com/get/noto/) fonts can also be freely downloaded.

Consolas font can be installed with [PowerPoint Viewer](https://www.microsoft.com/en-us/download/details.aspx?id=13) (available for download till April 2018).


### 4.2 Recommended Atom options

1. In **Settings** → **Editor**:
    * turn on **Soft Wrap** and **Soft Wrap At Preffered Line Length**. This setting is convenient for inspection of markdown code that was obtained from untrusted source,
    * **Font Size**: `15`,
    * **Line Height**: `1.7`.
2. Enable opening markdown files right from the Windows shell (from Explorer): in **Settings** → **System** turn on three checkboxes.
3. Sometimes some Atom packages break spell check and the clear install may be the easiest option. As stated [here](https://discuss.atom.io/t/how-to-completely-uninstall-atom-from-windows/17338) if on Windows in order to delete Atom completely you should uninstall it and then delete it's files from `%USERPROFILE%\.atom`, `%LOCALAPPDATA%\atom` and `%APPDATA%\Atom`.


### 4.3 Enable Atom spell checking

As far as I know it works only with **language-gfm** (GitHub flavored Markdown package). May be I'm wrong though.

English spell checking works on Atom and I was able to make russian and english spell checking work simultaneously. In order to make it work you should specify something like `en-US, ru-RU` in **Locales** setting and `C:\Dictionaries` in **Locale Paths** setting of **spell-check** module (by _atom_). Then put `en_US.aff`, `en_US.dic`, `ru_RU.aff`, `ru_RU.dic` to that folder (you can download the [Hunspell dictionary](https://sourceforge.net/projects/hunspell/files/Spelling%20dictionaries/en_US/)). Or you can use dictionaries from LibreOffice like [Russian spellcheck dictionary](https://extensions.libreoffice.org/extensions/russian-spellcheck-dictionary.-based-on-works-of-aot-group). They can be found in `%PROGRAMFILES%\LibreOffice 5\share\extensions` or `%APPDATA%\LibreOffice\4\user` folders (you can search for `*.dic` files). I renamed `russian-aot.aff`, `russian-aot.dic` files to `ru_RU.aff`, `ru_RU.dic` and changed their encoding to UTF-8.


### 4.6 Pandoctools Atom Package

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
