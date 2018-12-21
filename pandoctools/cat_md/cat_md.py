import sys
import os

_help = r"""Usage: cat-md [OPTIONS] [INPUT_FILES]

  cat-md CLI joins markdown files with "\n\n" separator and writes
  to stdout. If one of the files is "stdin" then reads it from stdin
  (can use the same stdin text several times).

Options:
  --help    Show this message and exit.
"""

def cat_md():
    
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == '--help':
            print(_help)
            return

    sources_list, stdin = [], None
    for file in sys.argv[1:]:
        if file == 'stdin':
            if stdin is None:
                stdin = sys.stdin.read()
            sources_list.append(stdin)
        else:
            with open(file, "r", encoding="utf-8") as f:
                sources_list.append(f.read())
    out = '\n\n'.join(sources_list)
    sys.stdout.write(out)
