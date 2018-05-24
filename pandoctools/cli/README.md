# Pandoctools CLI application

Pandoctools CLI application is a profile manager of text processing pipelines. It stores short shell (bash or batch) scripts - called profiles - that define chain operations over text. They are mostly Pandoc filters but any CLI text filter is OK. Profiles can be used to convert any document of choise in the specified manner. Simply add metadata section to markdown:

```yaml
---
pandoctools:
  profile: Kiwi
  out: "*.md.md"
...
```

Pandoctools automatically searches for [`Profile-Kiwi.sh`](https://github.com/kiwi0fruit/pandoctools/blob/master/pandoctools/sh/Profile-Kiwi.sh) (or [`Profile-Kiwi.bat`](https://github.com/kiwi0fruit/pandoctools/blob/master/pandoctools/bat/Profile-Kiwi.bat) - depends on OS and installed Git) in special folders: first - folder in user data, then - [folder in python module](https://github.com/kiwi0fruit/pandoctools/tree/master/pandoctools/sh) (actually all files defined in shell scripts are searched in that order, so you can replace a file in a chain simply by putting it to the folder in user data).

Shortcuts to these folders are created on the desktop. Profile can import other shell scripts from that special folders and read files from there. Moreover, profiles can use environment variables defined in Pandoctools CLI application - this shortens shell scripts and makes them more readable.


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
