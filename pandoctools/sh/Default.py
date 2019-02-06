import sys


def replace_mathjax():
    import re
    import os
    
    i = []
    def rep(m):
        i.append(0)
        if len(i) == 1:
            return ""
        return '<script type="text/javascript" src="{}"></script>'.format(sys.argv[2])
    sys.stdout.write(re.sub(
        r'<script type="text/javascript"[^<]+?[Mm]ath[Jj]ax.+?</script>',
        rep, sys.stdin.read(), count=2, flags=re.DOTALL))


if len(sys.argv) < 2:
    pass
elif sys.argv[1] == 'replace_mathjax':
    replace_mathjax()
