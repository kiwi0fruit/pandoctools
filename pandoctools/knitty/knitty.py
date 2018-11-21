import os
import sys
from IPython import get_ipython

ipython = get_ipython()
KNITTY = os.getenv('KNITTY', '').lower()
NOJUPYTER = False if ipython else True

if KNITTY == 'true':
    KNITTY = True
elif KNITTY == 'nojupyter':
    NOJUPYTER = True
    KNITTY = False
else:
    KNITTY = False
