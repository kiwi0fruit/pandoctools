# pandoctools-resolve

```
Usage: pandoctools-resolve [OPTIONS] FILE_BASENAME

  Inside Pandoctools shell scripts use alias: $resolve

  Resolves and echoes Unix style absolute path to the file by its basename
  (given with extension). First searches in %APPDATA%\pandoc\pandoctools
  (or $HOME/.pandoc/pandoctools), then in Pandoctools module directory:
  <...>/site-packages/pandoctools/sh
  
  On Windows conversion to POSIX paths is done via cygpath that at first is
  read from $cygpath env var then seached in the $PATH

Options:
  --else TEXT  Fallback file basename that is used if the first one wasn't
               found.
  --help       Show this message and exit.
```

Usage examples:

* `yml="$($resolve Profile.yml --else Default.yml)"`
* `source "$($resolve Profile --else Default)"`
