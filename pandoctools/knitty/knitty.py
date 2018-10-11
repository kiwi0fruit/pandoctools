import os
import sys

KNITTY = os.getenv('KNITTY', '').lower()

if KNITTY == 'true':
    KNITTY = True
else:
    KNITTY = False
