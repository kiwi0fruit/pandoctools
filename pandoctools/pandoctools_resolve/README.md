# pandoctools-resolve

```
Usage: pandoctools-resolve [FILE_BASENAME] [OPTION]
                             (in this particular order)
      Inside Pandoctools shell scripts use alias: $resolve

      Resolves and echoes absolute path to the file by its basename (given with extension).
      First searches in $HOME/.pandoc/pandoctools (or %APPDATA%\\pandoc\\pandoctools),
      Then in Pandoctools module directory
      (<...>/site-packages/pandoctools/sh).
      
    Options:
      --else TEXT    Fallback file basename that is used if the first one wasn't found,
      --help         Show this message and exit (only works without other args and options).
```

Usage examples:

* `yml="$($resolve profile.yml --else default.yml)"`
* `source "$($resolve profile --else default)"`
