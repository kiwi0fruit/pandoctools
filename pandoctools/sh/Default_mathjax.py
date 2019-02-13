import sys
import re

MJ_URL = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML"


def sub():
    """ Assumes --mathjax --self-contained --standalone options
        and type="text/javascript" was set. """
    try:
        mathjax_url = sys.argv[2]
    except IndexError:
        mathjax_url = MJ_URL
    rep = '<script type="text/javascript" src="{}" async></script>'.format(mathjax_url)

    sys.stdout.write(re.sub(
        r'<script type="text/javascript"[^<]+?[Mm]ath[Jj]ax.+?</script>',
        rep, sys.stdin.read(), flags=re.DOTALL))


def sub_pdf():
    """ Assumes Default_mathjax.html structure, --mathjax --self-contained --standalone options
        and type="text/javascript" was set. """
    try:
        mathjax_url = sys.argv[2]
    except IndexError:
        mathjax_url = MJ_URL
    i = []

    def rep(m):
        i.append(0)
        if len(i) == 1:
            return ""
        return '<script type="text/javascript" src="{}"></script>'.format(mathjax_url)

    sys.stdout.write(re.sub(
        r'<script type="text/javascript"[^<]+?[Mm]ath[Jj]ax.+?</script>',
        rep, sys.stdin.read(), flags=re.DOTALL, count=2))


if len(sys.argv) < 2:
    pass
elif sys.argv[1] == 'sub_pdf':
    sub_pdf()
elif sys.argv[1] == 'sub':
    sub()
