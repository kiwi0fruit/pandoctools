import sys
from typing import Iterable
import io


def main(markdown_files: Iterable[str], input_stream: io.StringIO=sys.stdin) -> str:
    """
    :param markdown_files: list of markdown files paths.
        If path is 'stdin' or '-' then reads it from input_stream
        (can use the same input_stream text several times).
        If markdown_files is empty then default is ['stdin']
    :param input_stream:
    :return: joined Markdown files with "\n\n" separator
    """
    sources_list, _stdin = [], None
    for file in markdown_files:
        if file in ('stdin', '-'):
            if _stdin is None:
                _stdin = input_stream.read()
            sources_list.append(_stdin)
        else:
            with open(file, "r", encoding="utf-8") as f:
                sources_list.append(f.read())
    if not sources_list:
        sources_list.append(input_stream.read())

    return '\n\n'.join(sources_list)


def cli():
    """
    Usage: cat-md [OPTIONS] [INPUT_FILES]

      Joins markdown files with "\\n\\n" separator and writes
      to stdout. If one of the files is "stdin" or "-" then reads
      it from stdin (can use the same stdin text several times).
      If no markdown files provided then default is 'stdin'.

    Options:
      --help   Show this message and exit.
    """
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == '--help':
            print(str(cli.__doc__).replace('    ', ''))
            return
    sys.stdout.write(main(sys.argv[1:]))
