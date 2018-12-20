# import sys
import os
import os.path as p
import subprocess
from subprocess import PIPE
import re
import sys
import click


class PandocFilterArgError(Exception):
    pass


def run_err(*args: str, stdin: str) -> str:
    """
    Run subprocess that would definitely give error
    and get stderr.

    :param args: CLI args
    :param stdin:
    :return: stderr
    """
    return subprocess.run(args, stderr=PIPE, input=stdin, encoding='utf-8').stderr


def win_where(executable: str) -> str:
    """
    :param executable: exec name without .exe
    :return:
        1. on Windows: absolute path to the exec that was found in the $PATH
        2. on Unix: executable arg untouched
    """
    if os.name == 'nt':
        executable = subprocess.run(
            [p.expandvars(r'%WINDIR%\System32\where.exe'), f'$PATH:{executable}.exe'],
            stdout=PIPE, encoding='utf-8'
        ).stdout.split('\n')[0].strip('\r')
        if not p.isfile(executable):
            raise PandocFilterArgError(f"'{executable}' wasn't found in the $PATH")
    return executable


doc = '''---
panflute-filters: {}
...
x
'''.format(p.join(p.dirname(p.abspath(__file__)), 'pandoc_filter_arg', 'pandoc_filter_arg.py'))


def pandoc_filter_arg(output: str=None, to: str=None) -> str:
    """
    :param output: Pandoc writer option
    :param to: Pandoc writer option
    :return: argument that is passed by Pandoc to it's filters
        Uses Pandoc's defaults.
    """
    pandoc, panfl = win_where('pandoc'), win_where('panfl')
    args = [pandoc, '-f', 'markdown', '--filter', panfl, '-o', (output if output else '-')]
    if to:
        args += ['-t', to]

    match = None
    err = run_err(*args, stdin=doc)
    for match in re.findall(r'(?<=\$\$\$).+?(?=\$\$\$)', err):
        pass
    if match is None:
        raise PandocFilterArgError(f'stderr output to parse: {err}')
    else:
        return match


# noinspection PyUnusedLocal
@click.command(
    context_settings=dict(ignore_unknown_options=True,
                          allow_extra_args=True),
    help="CLI interface that prints argument that is passed by Pandoc to it's filters. " +
         "Uses Pandoc's defaults. Ignores extra arguments."
)
@click.pass_context
@click.option('-o', '--output', type=str, default=None,
              help='Pandoc writer option.')
@click.option('-w', '-t', '--write', '--to', 'to', type=str, default=None,
              help="Pandoc writer option.")
def cli(ctx, output, to):
    sys.stdout.write(pandoc_filter_arg(output, to))
