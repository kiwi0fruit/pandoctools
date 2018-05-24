# Pandoctools CLI application

**Filters pipes shell scripts** (bash/batch) as interface to Panflute Pandoc filters and python text filters. Users write a shell script that specifies filters and Pandoc options. Then they use it to convert the particular document or to convert any document of choise in the same manner.

Actually it's some pre-written scripts, some standards of writing shell scripts and one new command line application that makes these scripts shorter.

Predefined in python app:

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
