# panfl

**panfl** allows [Panflute](https://github.com/sergiocorreia/panflute) to be run as a command line script so it can be used in Pandoctools shell scripts. It actually actomatically searches for provided Panflute filters in provided directories (python's `sys.path` is the default place to search). See `panfl --help` for options details and format info.  
Usage: `panfl -t markdown filter1 filter2 filter3`

```
Usage: panfl [OPTIONS] [FILTERS]...

  Filters should have basename only (may be with or without .py extension).
  Search preserves directories order (except for --data-dir and `sys.path`).

Options:
  -w, -t, --write, --to TEXT  Pandoc writer option.
  -d, --dir TEXT              Search filters in provided directories: `-d dir1
                              -d dir2`.
  --data-dir                  Search filters in default user data directory
                              listed in `pandoc --version` (in it's `filters`
                              subfolder actually). It's appended to the search
                              list.
  --no-sys-path               Disable search filters in python's `sys.path`
                              (current working directory removed) that is
                              appended to the search list.
  --help                      Show this message and exit.
```
