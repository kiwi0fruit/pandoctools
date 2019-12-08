from typing import Tuple, List
import sys
import os.path as p
import re
import click


def regex_replace(text: str, pattern: str, repl_template: str, strings: Tuple[str]=(), filepaths: Tuple[str]=()):
    """
    returns ``re.sub(pattern, repl_template.format(*repls), text, flags=re.DOTALL)``
    where ``repls`` is a List[str] either got from ``strings`` directly or read from ``filepaths``.
    """
    if not strings and filepaths:
        repls: List[str] = []
        for filepath in filepaths:
            with open(filepath, 'r', encoding='utf-8') as f:
                repls.append(f.read())
    elif not filepaths and strings:
        repls = list(strings)
    else:
        raise ValueError('Exactly and only one of `string` and `filepath` should be provided.')
    return re.sub(pattern, repl_template.format(*repls), text, flags=re.DOTALL)


@click.command(help="""Reads from stdin. Writes to stdout:

re.sub(pattern, repl_template.format(*repls), stdin, flags=re.DOTALL)

Where repls is a List[str] got from multiple options: either --string directly or read from --filepath.""")
@click.option('-p', '--pattern', type=str, required=True)
@click.option('-t', '--repl-template', 'repl_template', type=str, default='')
@click.option('-s', '--string', 'strings', multiple=True)
@click.option('-f', '--filepath', 'filepaths', multiple=True)
def cli(pattern: str, repl_template: str, strings: Tuple[str], filepaths: Tuple[str]):
    sys.stdout.write(regex_replace(sys.stdin.read(), pattern=pattern, repl_template=repl_template, strings=strings, filepaths=filepaths))
