import os
import sys
from IPython import get_ipython

NOIPYTHON = False
NTERACT = False
KNITTY = False

if not get_ipython():
    NOIPYTHON = True

PATH = os.getenv('PATH', '')
atom = os.sep + 'atom' + os.sep + 'app'
nteract = os.sep + 'nteract' + os.pathsep
if (atom in PATH) or (nteract in PATH):
    NTERACT = True

knitty = os.getenv('KNITTY', '').lower()
if knitty == 'true':
    KNITTY = True
elif knitty == 'noipython':
    NOIPYTHON = True
elif knitty == 'nteract':
    NTERACT = True
