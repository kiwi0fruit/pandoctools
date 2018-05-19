import sys


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
