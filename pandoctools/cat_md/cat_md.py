import sys
import os


def cat_md():
    r"""
    cat-md CLI joins markdown files with "\n\n" separator and writes
    to stdout. If one of the files is "stdin" then reads it from stdin
    (can use the same stdin text several times).
    Also replaces all "\r\n" with "\n" on Unix.

    OPTIONS:

    --keep-cr    doesn't replace "\r" (carriage return)
    --help       shows this message and exits
    """
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == '--help':
            print(cat_md.__doc__)
            return

    args = sys.argv[1:]
    n = len(args)
    args = [arg for arg in args if arg.lower() != '--keep-cr']
    keep_CR = (len(args) != n) or (os.name == 'nt')

    def del_CR(text): return text if keep_CR else text.replace('\r\n', '\n')

    sources_list, stdin = [], None
    for file in args:
        if file == 'stdin':
            if stdin is None:
                stdin = del_CR(sys.stdin.read())
            sources_list.append(stdin)
        else:
            with open(file, "r", encoding="utf-8") as f:
                sources_list.append(del_CR(f.read()))
    out = '\n\n'.join(sources_list)
    sys.stdout.write(out)
