import os
import sys

KNITTY = os.environ['KNITTY'].lower()

if KNITTY == 'true':
    KNITTY = True
elif KNITTY == 'false':
    KNITTY = False
elif 'knitty' in sys.modules:
    KNITTY = True
else:
    KNITTY = False
