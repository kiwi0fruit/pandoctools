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


help_str = """Pandoctools is a Pandoc profile manager that stores CLI filter pipelines.

Not providing INPUT_FILE is the same as setting --std flag (default name is "Untitled").

Profiles are searched in user data: "{}" then in python module: "{}".
Profiles read from stdin and write to stdout (usually).

Some options can be set in document metadata:\n
---\n
pandoctools:\n
  prof: Default\n
  out: *.html\n
...

May be (?) for security concerns the user data folder should be set to write-allowed only as administrator.
""".format(pandoctools_user_data, pandoctools_core)


@click.command(help=help_str)
@click.argument('input_file', type=str, default=None, required=False)
@click.option('-p', '--prof', type=str, default=None,
              help='Pandoctools profile name or file path (default is "Default").')
@click.option('-o', '--out', type=str, default=None,
              help='Output file path like "./out/doc.html" ' +
                   'or input file path transformation like "*.html", "./out/*.r.ipynb" (default is "*.html").\n' +
                   'In --std mode only full extension is considered: "doc.r.ipynb" > "r.ipynb".')
@click.option('-s', '--std', is_flag=True, default=False,
              help="Read document form stdin and write to stdout. INPUT_FILE only gives a file path. If --std was " +
                   "set but stdout = '' then the profile always writes output file to disc with that options.")
def pandoctools(input_file, profile, out, std):
    """
    """
    os.environ['_user_config'] = pandoctools_user
    os.environ['_core_config'] = pandoctools_core

    if not std:
        input("Press Enter to continue...")
