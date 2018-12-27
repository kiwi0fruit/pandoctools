import sys


def main(basename: str, fallback_basename: str=None) -> str:
    """
    Returns absolute path to the file by its basename (given with extension).
    First searches in $HOME/.pandoc/pandoctools (or %APPDATA%\\pandoc\\pandoctools),
    Then in Pandoctools module directory
    (<...>/site-packages/pandoctools/sh).

    :param basename:
    :param fallback_basename:
    :return: absolute path (or empty string if it wasn't found)
    """
    return ''


def cli():
    """
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
    """
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == '--help':
            print(str(cli.__doc__).replace('    ', ''))
            return

        file, fallback = sys.argv[1], None
        try:
            if sys.argv[3] and (sys.argv[2].lower() == '--else'):
                fallback = sys.argv[3]
        except IndexError:
            pass
        sys.stdout.write(main(file, fallback))
    else:
        raise ValueError('pandoctools-resolve needs at least one argument.')
