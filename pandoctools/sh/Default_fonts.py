import sys
import os
import os.path as p
import io

stdin = sys.stdin.read()
fontscss = sys.argv[1]
if p.isfile(fontscss):
    with io.open(fontscss, 'r', encoding='utf-8') as f:
        css = f.read()
    stdout = stdin.replace('<head>', '<head><style>' + css + '</style>')
else:
    stdout = stdin
sys.stdout.write(stdout)
