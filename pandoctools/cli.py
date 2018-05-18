import sys
import os
from os.path import join, dirname, abspath
import click
import re

if os.name == 'nt':
    pandoctools_user_data = r"%APPDATA%\pandoc\pandoctools"
    pandoctools_user = join(os.environ["APPDATA"], "pandoc", "pandoctools")
    pandoctools_core = join(dirname(abspath(__file__)), "bat")
else:
    pandoctools_user_data = "$HOME/.pandoc/pandoctools"
    pandoctools_user = join(os.environ["HOME"], ".pandoc", "pandoctools")
    pandoctools_core = join(dirname(abspath(__file__)), "sh")


def cat_md():
    """
    Joins markdown files with "\n\n" separator and writes to stdout.
    If file is 'stdin' then reads it from stdin.
    """
    sources_list, stdin = [], None
    for file in sys.argv[1:]:
        if file == 'stdin':
            if stdin is None:
                stdin = sys.stdin.read()
            sources_list.append(stdin)
        else:
            with open(file, "r", encoding="utf-8") as f:
                sources_list.append(f.read())
    sys.stdout.write('\n\n'.join(sources_list))


@click.command(
    help="Pandoctools is a Pandoc profile manager that stores CLI filter pipelines.\n" +
         "Profiles first are read from user data: {} then from python module: {}\n".format(pandoctools_user_data,
                                                                                           pandoctools_core) +
         "Profiles read from stdin and write to stdout (at least something). " +
         "May be (?) for security concerns the user data folder should be set to write-allowed only as administrator."
)
@click.argument('input_file', type=str, default=None, required=False)
@click.option('-p', '--profile', type=str, default="Default",
              help='Pandoctools profile name or file path.')
@click.option('-o', '--out', type=str, default=None,
              help='Output file path like "./out/doc.html"\n' +
                   'or input file path transformation like "./out/*.html", "*.r.ipynb"\n' +
                   'If not provided the output document is written to stdout. ' +
                   'Same is when additional extension postfix provided but input file name is not provided.')
@click.option('-t', '--to', type=str, default=None,
              help='Extension like "html" or "r.ipynb" that governs output format.')
@click.option('--stdin', is_flag=True, default=False,
              help='Read document form stdin. INPUT_FILE only gives a file path.')
def pandoctools(input_file, profile, out, to, stdin):
    """
    if stdout == 'no stdout <path>' then the profile wrote output file to disc
    and told us about it.
    """
    os.environ['_user_config'] = pandoctools_user
    os.environ['_core_config'] = pandoctools_core
