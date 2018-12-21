import sys

_help = """cat-md joins markdown files with "\n\n" separator and writes to stdout.
If one of the files is "stdin" then reads it from stdin
(can use the same stdin text several times).
"""


def cat_md():
    """
    Joins markdown files with "\n\n" separator and writes to stdout.
    If one of the files is "stdin" then reads it from stdin
    (can use the same stdin text several times).
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print(_help)
            return

    sources_list, stdin = [], None
    for file in sys.argv[1:]:
        if file == 'stdin':
            if stdin is None:
                stdin = sys.stdin.read().replace('\r\n', '\n')
            sources_list.append(stdin)
        else:
            with open(file, "r", encoding="utf-8") as f:
                sources_list.append(f.read().replace('\r\n', '\n'))
    sys.stdout.write('\n\n'.join(sources_list))
