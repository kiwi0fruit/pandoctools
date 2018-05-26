# Pandoctools CLI application

Pandoctools CLI application is a profile manager of text processing pipelines. It stores short shell (bash or batch) scripts - called profiles - that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK. Profiles can be used to convert any document of choise in the specified manner. Simply add metadata section to markdown:

```yaml
---
pandoctools:
  profile: Default
  out: "*.md.md"
...
```

You can use special shortcuts in `profile` and `out` definitions: `*` mean input file basename without extension, `*.*` mean input file basename with extension.

Pandoctools automatically searches for [`Profile-Default.sh`](../sh/Profile-Default.sh) (or [`Profile-Default.bat`](../bat/Profile-Default.bat) - depends on OS and installed Git) in special folders: first - folder in user data, then - [folder in python module](../sh) (actually all files defined in shell scripts are searched in that order, so you can replace a file in a chain simply by putting it to the folder in user data). Folder in user data is `%APPDATA%\pandoc\pandoctools` on Windows, `~/.pandoc/pandoctools` on Unix.

Shortcuts to these folders are created on the desktop. Profile can import other shell scripts from that special folders and read files from there. For example [this one](../sh/Args-Default.sh) defines CLI options depending on output format, and [that one](../sh/Pipe-Default.sh) defines text convertion pipeline with CLI text filters. Moreover, profiles can use environment variables defined in Pandoctools CLI application - this shortens shell scripts and makes them more readable.

I tried to make shell scripts short and transparent so you can easily copy/tune them.

**WARNING**: shell scripts are stored inside user data (both in Pandoc user data and Miniconda installation). I heard some talks about security concerns on this but I'm sure it they are of any importance...


## New CLI apps

Pandoctools comes with convenience CLI apps:

* [**panfl**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/panfl) allows [Panflute](https://github.com/sergiocorreia/panflute) to be run as a command line script so it can be used in Pandoctools shell scripts.
* [**cat-md**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/cat_md) is a simple CLI tool that concatenates input files with stdin input (joins them with double new lines) and prints to stdout.


## Environment variables predefined in Pandoctools CLI application:

* `scripts` - `<python_env>\Scripts` folder on Windows, `<python_env>/bin` on Unix
* `import` - `call`/`source` shell script (provided without extension!) from folder in user data first, then from [folder in python module](../sh)
* `source` - `call`/`source` shell script from PATH only (without current working dir)
* `r` (win) - run app from PATH only (without current working dir)
* `set_resolve` (win) - sets to env var which name given in first arg the resolved fullpath to file given in second arg. File is searched in the folder in user data first, then in the [folder in python module](../sh)
* `resolve` (unix) - echoes the resolved fullpath to file given. File is searched in the folder in user data first, then in the [folder in python module](../sh)
* `pyprepPATH` - prepends PATH with all necessary python folders. Argument is the root dir of python installation (root env or created env). Runs only if argument is not empty.
* `env_path` - root dir of python installation where pandoctools was installed
* `input_file` - absolute path to input file (?may be broken when no CWD was specified and python can't resolve relative path)
* `output_file` - absolute path to output file (?may be broken when no CWD)
* `in_ext` - input file extension
* `in_ext_full` - input file full extension like `tar.gz` or `r.ipynb` or `md.md.html`
* `out_ext` - output file extension
* `out_ext_full` - output file full extension
* `_core_config` - [sh folder in python module](../sh) or [bat folder in python module](../bat) - the one in use (depends on OS and bash on Windows set up)
* `_user_config` - `%APPDATA%\pandoc\pandoctools` on Windows, `~/.pandoc/pandoctools` on Unix
* `root_env` - root dir of main Miniconda/Anaconda installation (empty if wasn't specified in INI and Pandoctools cannot guess it)
* `setUTF8` (win) - set python and console encoding to UTF-8
* `PYTHONIOENCODING` (win) = `utf-8`
* `LANG` (win) = `C.UTF-8`
