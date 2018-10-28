# Pandoctools CLI application

Pandoctools CLI application is a profile manager of text processing pipelines. It stores short bash scripts - called profiles - that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK. Profiles can be used to convert any document of choise in the specified manner. Simply add metadata section to markdown:

```yaml
---
pandoctools:
  profile: Default
  out: "*.md.md"
...
```

You can use special shortcuts in `profile` and `out` definitions: `*` mean input file basename without extension, `*.*` mean input file basename with extension.

Pandoctools automatically searches for [`Profile-Default.sh`](../sh/Profile-Default.sh) in special folders: first - folder in user data, then - [folder in python module](../sh) (actually all files defined in shell scripts and `Defaults.ini` are searched in that order, so you can replace a file in a chain simply by putting it to the folder in user data). Folder in user data is `%APPDATA%\pandoc\pandoctools` on Windows, `~/.pandoc/pandoctools` on Unix.

Shortcuts to these folders are created on the desktop. Profile can import other shell scripts from that special folders and read files from there. For example [this one](../sh/Args-Default.sh) defines CLI options depending on output format, and [that one](../sh/Pipe-Default.sh) defines text convertion pipeline with CLI text filters. Moreover, profiles can use environment variables defined in Pandoctools CLI application - this shortens shell scripts and makes them more readable.

I tried to make shell scripts short and transparent so you can easily copy/tune them.

**WARNING**: shell scripts are stored inside user data (both in Pandoc user data and Miniconda installation). I heard some talks about security concerns on this but I'm not sure it they are of any importance...


## How to use

After installation you would have a shortcut on the desktop. Recommended ways to run Pandoctools are to:

- add it to 'Open With' applications for desired file format,
- drag and drop file over pandoctools shortcut,
- run it from console, see: `pandoctools --help`

```
Usage: pandoctools [OPTIONS] [INPUT_FILE]

  Pandoctools is a Pandoc profile manager that stores CLI filter pipelines.
  (default INPUT_FILE is "Untitled").

  Profiles are searched in user data: "%APPDATA%\pandoc\pandoctools" then in
  python module: "d:\user\python\miniconda3_x64\envs\research\lib\site-
  packages\pandoctools\bat". Profiles read from stdin and write to stdout
  (usually).

  Some options can be set in document metadata:

  ---
  pandoctools:
    prof: Default
    out: *.html
  ...

  May be (?) for security concerns the user data folder should be set to
  write-allowed only as administrator.

Options:
  -p, --profile TEXT  Pandoctools profile name or file path (default is
                      "Default").
  -o, --out TEXT      Output file path like "./out/doc.html" or input file
                      path transformation like "*.html", "./out/*.r.ipynb"
                      (default is "*.html").
                      In --stdio mode only full
                      extension is considered: "doc.r.ipynb" > "r.ipynb".
  --stdio             Read document form stdin and write to stdout in a silent
                      mode. INPUT_FILE only gives a file path. If --stdio was
                      set but stdout output was empty then the profile (not
                      Pandoctools itself) always writes output file to disc
                      and doesn't write to stdout with these options.
  --stdin             Same as --stdio but always writes output file to disc
                      (suppresses --stdio).
  --cwd               Use real CWD everywhere (instead of input file directory
                      as default).
  --detailed-out      With this option when in --stdio and --stdin modes
                      pandoctools stdout consist of yaml metadata section
                      ---... with 'outpath' and 'output' keys that is followed
                      by profile stdout (when --stdin or profile stdout output
                      was empty then key 'output: None').
  --debug             Debug mode.
  --help              Show this message and exit.

```


## Defaults.ini

Pandoctools stores some settings in [`Defaults.ini`](../sh/Defaults.ini) file. The active `Defaults.ini` is resolved the same way Pandoctools resolves profiles (first in user data then in sh folder in python module).

* you can set `root_env` var there if you installed current environment to special location instead or default `<root_env>/envs/my_env`
* `pandoctools` var stores the path to the pandoctools executable. It is set by pandoctools installer when it writes `Defaults.ini` to the folder in user data. You can specify it yourself too.
* `win_bash` var stores the path to bash on Windows. Default is `%PROGRAMFILES%\Git\bin\bash.exe` but you can set it yourself.


## New CLI apps

Pandoctools comes with convenience CLI apps:

* [**panfl**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/panfl) allows [Panflute](https://github.com/sergiocorreia/panflute) to be run as a command line script so it can be used in Pandoctools shell scripts.
* [**cat-md**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/cat_md) is a simple CLI tool that concatenates input files with stdin input (joins them with double new lines) and prints to stdout.


## Environment variables predefined in Pandoctools CLI application:

* `scripts` - `<python_env>\Scripts` folder on Windows, `<python_env>/bin` on Unix
* `import` - `source` bash script (provided without extension!) from folder in user data first, then from [folder in python module](../sh)
* `source` - `source` bash script from PATH only (without current working dir)
* `resolve` - echoes the resolved fullpath to file given. File is searched in the folder in user data first, then in the [folder in python module](../sh)
* `pyprepPATH` - prepends PATH with all necessary python folders. Argument is the root dir of python installation (root env or created env). Runs only if argument is not empty.
* `env_path` - root dir of python installation where pandoctools was installed
* `input_file` - absolute path to input file (?may be broken when no CWD was specified and python can't resolve relative path)
* `output_file` - absolute path to output file (?may be broken when no CWD)
* `in_ext` - input file extension
* `in_ext_full` - input file full extension like `tar.gz` or `r.ipynb` or `md.md.html`
* `out_ext` - output file extension
* `out_ext_full` - output file full extension
* `_core_config` - [sh folder in python module](../sh)
* `_user_config` - `%APPDATA%\pandoc\pandoctools` on Windows, `~/.pandoc/pandoctools` on Unix
* `root_env` - root dir of main Miniconda/Anaconda installation (empty if wasn't specified in INI and Pandoctools cannot guess it)
* `PYTHONIOENCODING` (win) = `utf-8`
* `LANG` (win) = `C.UTF-8`
