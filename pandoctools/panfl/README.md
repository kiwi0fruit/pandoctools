# panfl

**panfl** allows [Panflute](https://github.com/sergiocorreia/panflute) to be run as a command line script so it can be used in Pandoctools shell scripts. It actually actomatically searches for provided Panflute filters in provided directories (python's `sys.path` is the default place to search). See `panfl --help` for options details and format info.  
Usage: `panfl -t makdown filter1 filter2 filter3`
