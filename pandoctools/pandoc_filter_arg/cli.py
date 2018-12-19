# import sys
import os
import os.path as p
import subprocess
from subprocess import PIPE
import re
import sys


class PandocFilterArgError(Exception):
    pass


def run_err(*args: str, stdin: str) -> str:
    return subprocess.run(args, stderr=PIPE, input=stdin, encoding='utf-8').stderr


def where(executable: str) -> str:
    executable = subprocess.run(
        [p.expandvars(r'%WINDIR%\System32\where.exe'), f'$PATH:{executable}.exe'],
        stdout=PIPE, encoding='utf-8').stdout.split('\n')[0].strip('\r')
    if not p.isfile(executable):
        raise PandocFilterArgError(f"'{executable}' wasn't found in the $PATH")
    return executable


doc = '''---
panflute-filters: {}
...
x
'''.format(p.join(p.dirname(p.abspath(__file__)), 'pandoc_filter_arg', 'pandoc_filter_arg.py'))

_help = """CLI interface that prints argument that is passed by Pandoc to it's filters.
The first argument is Pandoc's --to / -t / --write / -w argument.
Uses Pandoc's default if the first argument is absent or empty. 
"""


def cli():
    """
    * CLI interface that prints argument that is passed by Pandoc to it's filters.
    * The first argument is Pandoc's ``--to`` / ``-t`` / ``--write`` / ``-w`` argument.
    * Uses Pandoc's default if the first argument is absent or empty.
    """
    to = sys.argv[1] if (len(sys.argv) > 1) else None
    if to == '--help':
        print(_help)
        return
    to = to if to else None
    pandoc, panfl = (where('pandoc'), where('panfl')) if (os.name == 'nt') else ('pandoc', 'panfl')
    args = [pandoc, '-f', 'markdown', '--filter', panfl, '-o', 'dummy_file']
    if to is not None:
        args += ['-t', to]

    match = None
    err = run_err(*args, stdin=doc)
    for match in re.findall(r'(?<=\$\$\$).+?(?=\$\$\$)', err):
        pass
    if match is None:
        raise PandocFilterArgError(f'stderr output to parse: {err}')
    else:
        sys.stdout.write(match)
