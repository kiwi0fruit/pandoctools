from typing import Tuple, List
import sys
import os.path as p
import re
import click


def regex_replace(text: str, pattern: str, repl_template: str, filepaths: Tuple[str]=()):
    """
    returns ``re.sub(pattern, repl_template.format(*strings), text, flags=re.DOTALL)``
    where ``strings`` is a List[str] read from ``filepaths``
    (if ``strings`` is empty no formatting is attemtpted).
    """
    strings: List[str] = []
    for filepath in filepaths:
        with open(filepath, 'r', encoding='utf-8') as f:
            strings.append(f.read())
    return re.sub(pattern, repl_template.format(*strings) if strings else repl_template, text, flags=re.DOTALL)


@click.command(help="""Reads from stdin. Writes to stdout:

re.sub(pattern, repl_template.format(*strings), stdin, flags=re.DOTALL)

Where strings is a List[str] got from multiple --filepath options.
Like: -f xx -f yy (if no filepaths were provided then no formatting is attemtpted).""")
@click.option('-p', '--pattern', type=str, required=True)
@click.option('-t', '--repl-template', 'repl_template', type=str, default='')
@click.option('-f', '--filepath', 'filepaths', multiple=True)
def cli(pattern: str, repl_template: str, filepaths: Tuple[str]):
    sys.stdout.write(regex_replace(sys.stdin.read(), pattern=pattern, repl_template=repl_template, filepaths=filepaths))
