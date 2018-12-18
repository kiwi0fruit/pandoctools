# panfl

**panfl** allows [Panflute](https://github.com/sergiocorreia/panflute) to be run as a command line script so it can be used in Pandoctools shell scripts. It actually actomatically searches for provided Panflute filters in provided directories (python's `sys.path` is the default place to search and I tried to remove current working directory from it). See `panfl --help` for options details and format info.  
Usage: `panfl -t markdown -d "~/dir" -d "./dir" filter1 filter2`

```
Usage: panfl [OPTIONS] [FILTERS]...

  Allows Panflute to be run as a command line executable:

  * to be used in Pandoctools shell scripts as Pandoc filter with multiple
  arguments (should have -t/--to option in this case): `pandoc -t json |
  panfl -t markdown foo.bar | pandoc -f json`

  * to be used as a Pandoc filter (in this case only one positional argument
  is allowed of all options): `pandoc --filter panfl`

  Filters may be set with or without .py extension. It can be relative or
  absolutele paths to files or modules specs like `foo.bar`.

  MIND THAT Panflute temporarily prepends folder of the filter (or relevant
  dir provided if module spec) TO THE `sys.path` before importing the
  filter!

  Search preserves directories order (except for --data-dir and `sys.path`).

Options:
  -w, -t, --write, --to TEXT  Derivative of Pandoc writer option that Pandoc
                              passes to filters.
  -d, --dir TEXT              Search filters in provided directories: `-d dir1
                              -d dir2`.
  --data-dir                  Search filters in default user data directory
                              listed in `pandoc --version` (in it's `filters`
                              subfolder actually). It's appended to the search
                              list.
  --no-sys-path               Disable search filters in python's `sys.path`
                              (without '' and '.') that is appended to the
                              search list.
  --help                      Show this message and exit.
```
