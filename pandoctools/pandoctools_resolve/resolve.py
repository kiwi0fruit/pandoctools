import sys
import os.path as p
import click
from ..shared_vars import pandoctools_user, pandoctools_user_data, pandoctools_core


def main(basename: str, fallback_basename: str=None) -> str:
    """
    Returns absolute path to the file by its basename (given with extension).
    First searches in $HOME/.pandoc/pandoctools (or %APPDATA%\\pandoc\\pandoctools),
    Then in Pandoctools module directory  (<...>/site-packages/pandoctools/sh).
    Fallback basename is used if the first one wasn't found.

    :param basename:
    :param fallback_basename:
    :return: absolute path (or empty string if it wasn't found)
    """
    for abs_path in (p.join(dir_, name)
                     for name in (basename, fallback_basename)
                     for dir_ in (pandoctools_user, pandoctools_core)
                     if name):
        if p.isfile(abs_path):
            return abs_path
    return ''


@click.command(help=f"""
Inside Pandoctools shell scripts use alias: $resolve

Resolves and echoes absolute path to the file by its basename (given with extension).
First searches in {pandoctools_user_data}, then in Pandoctools module directory:
{pandoctools_core}
""")
@click.argument('file_basename', type=str)
@click.option('--else', 'fallback', type=str, default=None,
              help="Fallback file basename that is used if the first one wasn't found.")
def cli(file_basename, fallback):
    sys.stdout.write(main(file_basename, fallback))
