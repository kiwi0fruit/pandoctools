# Pandoctools CLI application

Pandoctools CLI application is a profile manager of text processing pipelines. It stores short shell (bash or batch) scripts - called profiles - that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK. Profiles can be used to convert any document of choise in the specified manner. Simply add metadata section to markdown:

```yaml
---
pandoctools:
  profile: Default
  out: "*.md.md"
...
```

Pandoctools automatically searches for [`Profile-Default.sh`](../sh/Profile-Default.sh) (or [`Profile-Default.bat`](../bat/Profile-Default.bat) - depends on OS and installed Git) in special folders: first - folder in user data, then - [folder in python module](../sh) (actually all files defined in shell scripts are searched in that order, so you can replace a file in a chain simply by putting it to the folder in user data).

Shortcuts to these folders are created on the desktop. Profile can import other shell scripts from that special folders and read files from there. For example [this one](../sh/Args-Default.sh) defines CLI options depending on output format, and [that one](../sh/Pipe-Default.sh) defines text convertion pipeline with CLI text filters. Moreover, profiles can use environment variables defined in Pandoctools CLI application - this shortens shell scripts and makes them more readable.

I tried to make shell scripts short and transparent so you can easily copy/tune them.

**WARNING**: shell scripts are stored inside user data (both in Pandoc user data and Miniconda installation). I heard some talks about security concerns on this but I'm sure it they are of any importance...


## New CLI apps

Pandoctools comes with convenience CLI apps:

* [**panfl**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/panfl) allows [Panflute](https://github.com/sergiocorreia/panflute) to be run as a command line script so it can be used in Pandoctools shell scripts.
* [**cat-md**](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/cat_md) is a simple CLI tool that concatenates input files with stdin input (joins them with double new lines) and prints to stdout.


## Environment variables predefined in Pandoctools CLI application:

* scripts
* import
* source
* r (win)
* set_resolve (win)
* resolve (unix)
* pyprepPATH
* env_path
* input_file
* output_file
* in_ext
* in_ext_full
* out_ext
* out_ext_full
* _core_config
* _user_config
* root_env
* setUTF8 (win)
* PYTHONIOENCODING (win)
* LANG (win)
