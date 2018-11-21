import os
import sys

KNITTY = os.getenv('KNITTY', '').lower()
HYDROGEN = False

if KNITTY == 'true':
    KNITTY = True
if KNITTY == 'hydrogen':
    HYDROGEN = True
    KNITTY = False
else:
    KNITTY = False
