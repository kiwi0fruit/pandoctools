# Pandoctools CLI application

Pandoctools CLI application is a profile manager of text processing pipelines. It stores short bash scripts - called profiles - that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK. Profiles can be used to convert any document of choise in the specified manner. Simply add metadata section to markdown (all settings are optional - pandoctools would use defaults if needed):

```yaml
---
pandoctools:
  profile: Default
  out: "*.html"
  from: markdown
  to: html
...
```

You can use special shortcuts in `profile` and `out` definitions: `*` mean input file basename without extension, `*.*` mean input file basename with extension.

Pandoctools automatically searches for [`Default`](../sh/Default) profile in special folders: first - folder in user data, then - [folder in python module](../sh) (actually all files defined in shell scripts and `Defaults.ini` are searched in that order, so you can replace a file in a chain simply by putting it to the folder in user data). Folder in user data is `%APPDATA%\pandoc\pandoctools` on Windows, `~/.pandoc/pandoctools` on Unix.

Shortcuts to these folders are created on the desktop. Profile can import other shell scripts from that special folders and read files from there. For example [this one](../sh/Default_args) defines CLI options depending on output format, and [that one](../sh/Default_pipe) defines text convertion pipeline with CLI text filters. Moreover, profiles can use environment variables defined in Pandoctools CLI application - this shortens shell scripts and makes them more readable.

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
  (default INPUT_FILE is "untitled").

  Recommended ways to run Pandoctools are to:
  - add it to 'Open With' applications for desired file format,
  - drag and drop file over pandoctools shortcut,
  - run it from console

  Profiles are searched in user data: "%APPDATA%\pandoc\pandoctools"
  (or $HOME/.pandoc/pandoctools) then in python module:
  "<..>\site-packages\pandoctools\sh". When profile is given by path then
  Pandoctools asks for confirmation (in stdin mode prints confirmation to
  stdout and exits). Profiles read from stdin and write to stdout (usually).

  Some options can be set in document metadata (all are optional):

  ---
  pandoctools:
    prof: Default
    out: *.html
    from: markdown
    to: html
  ...

  May be (?) for security concerns the user data folder should be set to
  write-allowed only as administrator.

Options:
  -i, --in TEXT                Input file path for when INPUT_FILE argument
                               wasn't provided and we read from stdin
                               (INPUT_FILE has a priority).
  -p, --profile TEXT           Pandoctools profile name or file path (default
                               is in INI: "Default").
  -o, --out TEXT               Output file path like "./out/doc.html" or input
                               file path transformation like "./out/*.ipynb"
                               (default is in INI: "*.*.md"). `-o "-"`
                               switches output to stdout but doesn't override
                               `out: x` in metadata.
  -s, --stdout TEXT            Same as --out but write document to stdout (has
                               a priority over --out). `-s "-"` switches
                               output to stdout but doesn't override `out: x`
                               in metadata. If switched to stdout but stdout
                               output was empty then the profile (not
                               Pandoctools itself) always writes output file
                               to disc and doesn't write to stdout with the
                               particular options.
  -f, -r, --from, --read TEXT  Pandoc reader option (can be extended with
                               custom formats handled in profiles).
  -t, -w, --to, --write TEXT   Pandoc writer option (can be extended with
                               custom formats handled in profiles).
  --yes                        Run without confirmation of the profile if it
                               was going to happen.
  --cwd                        Use real CWD everywhere (instead of input file
                               directory as default).
  --detailed-out               With this option when in stdout mode
                               pandoctools stdout consist of yaml metadata
                               section ---... with 'outpath' and 'output' keys
                               that is followed by profile stdout (when not in
                               stdout mode or profile stdout output was empty
                               then key 'output: None').
  --debug                      Debug mode.
  --help                       Show this message and exit.
```

(optional on Windows):
```
ERROR: Bash was not found by the path provided in INI file.
```


## Defaults.ini

Pandoctools stores some settings in [`Defaults.ini`](../sh/Defaults.ini) file. The active `Defaults.ini` is resolved the same way Pandoctools resolves profiles (first in user data then in sh folder in python module).

* you can set `root_env` var there if you installed current environment to special location instead or default `<root_env>/envs/my_env`
* `pandoctools` var stores the path to the pandoctools executable. It is set by pandoctools installer when it writes `Defaults.ini` to the folder in user data. You can specify it yourself too.
* `win_bash` var stores the path to bash on Windows. Default is `%PROGRAMFILES%\Git\bin\bash.exe` but you can set it yourself.


## New CLI apps

Pandoctools comes with convenience CLI apps:

* [**panfl**](../../docs/panfl.md) allows [Panflute](https://github.com/sergiocorreia/panflute) to be run as a command line script so it can be used in Pandoctools shell scripts.
* [**cat-md**](../cat_md) is a simple CLI tool that concatenates input files with stdin input (joins them with double new lines) and prints to stdout.
* [**pandoc-filter-arg**](../pandoc_filter_arg) is a CLI interface that prints argument that is passed by Pandoc to it's filters.


## Environment variables predefined in Pandoctools CLI application:

* `scripts` - `<python_env>\Scripts` folder on Windows, `<python_env>/bin` on Unix
* `source` - `source` bash script from PATH only (without current working dir)
* `resolve` - echoes the resolved fullpath to file given. File is searched in the folder in user data first (`%APPDATA%\pandoc\pandoctools` on Windows, `~/.pandoc/pandoctools` on Unix), then in the [folder in python module](../sh)
* `python_to_PATH` - prepends PATH with all necessary python folders. Argument is the root dir of python installation (root env or created env). Runs only if argument is not empty.
* `env_path` - root dir of python installation where pandoctools was installed
* `input_file` - absolute path to input file (?may be broken when no CWD was specified and python can't resolve relative path)
* `output_file` - absolute path to output file (?may be broken when no CWD)
* `in_ext` - input file extension without dot
* `out_ext` - output file extension without dot
* `root_env` - root dir of main Miniconda/Anaconda installation (empty if wasn't specified in INI and Pandoctools cannot guess it)
* `from` - Pandoc reader format + custom Pandoctools formats
* `to` - Pandoc writer format + custom Pandoctools formats
* `important_from` - bool: whether `from` was set by user
* `important_to` - bool: whether `to` was set by user
* `is_bin_ext_maybe` - Pandoctools nice guess if the `output_file` extension (or `to` if no ext) means that Pandoc needs adding `-o "${output_file}"` option
* `PYTHONIOENCODING` (win) = `utf-8`
* `LANG` (win) = `C.UTF-8`
