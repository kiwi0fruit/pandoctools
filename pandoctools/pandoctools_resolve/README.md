# pandoctools-resolve

```
Usage: pandoctools-resolve [OPTIONS] FILE_BASENAME

  Inside Pandoctools shell scripts use alias: $resolve

  Resolves and echoes absolute path to the file by its basename (given with
  extension). First searches in %APPDATA%\pandoc\pandoctools
  (or $HOME/.pandoc/pandoctools), then in Pandoctools module directory:
  <...>/site-packages/pandoctools/sh

Options:
  --else TEXT  Fallback file basename that is used if the first one wasn't
               found.
  --help       Show this message and exit.
```

Usage examples:

* `yml="$($resolve Profile.yml --else Default.yml)"`
* `source "$($resolve Profile --else Default)"`
