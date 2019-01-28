import os.path as p
from subprocess import run, PIPE
import re
import sys
import click
from typing import Iterable
from ..shared_vars import where, PandotoolsError


def run_err(*args: str, stdin: str) -> str:
    """
    Run subprocess that would definitely give error
    and get stderr.

    :param args: CLI args
    :param stdin:
    :return: stderr
    """
    return run(args, stderr=PIPE, input=stdin, encoding='utf-8').stderr


doc = '''---
panflute-filters: {}
...
x
'''.format(p.join(p.dirname(p.abspath(__file__)), 'pandoc_filter_arg', 'pandoc_filter_arg.py'))


def pandoc_filter_arg(output: str=None, to: str=None, search_dirs: Iterable[str]=None) -> str:
    """
    :param output: Pandoc writer option
    :param to: Pandoc writer option
    :param search_dirs: extra dirs to look for executables
    :return: argument that is passed by Pandoc to it's filters
        Uses Pandoc's defaults.
    """
    pandoc, panfl = where('pandoc', search_dirs), where('panfl', search_dirs)
    args = [pandoc, '-f', 'markdown', '--filter', panfl, '-o', (output if output else '-')]
    if to:
        args += ['-t', to]

    match = None
    err = run_err(*args, stdin=doc)
    for match in re.findall(r'(?<=\$\$\$).+?(?=\$\$\$)', err):
        pass
    if match is None:
        raise PandotoolsError(f'stderr output to parse: {err}')
    else:
        return match


def is_bin_ext_maybe(output: str, to: str=None, search_dirs: Iterable[str]=None,
                     force_pandoc: bool=False) -> bool:
    """
    :param output: Pandoc writer option
    :param to: Pandoc writer option.
        Used only if output doesn't have an extension
    :param search_dirs: extra dirs to look for executables
    :param force_pandoc: ignore hardcoded logic and always "ask" Pandoc.
        Useful for testing hardcoded logic.
    :return: argument that is passed by Pandoc to it's filters
        Uses Pandoc's defaults.
    """
    ext = p.splitext(p.basename(output))[1][1:]
    if not ext:
        ext = to

    if not ext:
        return False
    elif ext in ('pdf', 'docx', 'epub', 'odt') and (not force_pandoc):  # TODO add more
        return True
    else:
        pandoc, panfl = where('pandoc', search_dirs), where('panfl', search_dirs)
        err = run([pandoc, '-f', 'markdown', '--filter', panfl, '-t', ext],
                  stderr=PIPE, stdout=PIPE, input=doc.encode()).stderr
        err = err.decode() if err else ''
        if re.search(r"(Cannot write \w+ output to terminal|specify an output file)", err):
            return True
        else:
            return False


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
