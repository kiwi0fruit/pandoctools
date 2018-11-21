import os
import sys
from IPython import get_ipython
from typing import NamedTuple

NOIPYTHON = False
NTERACT = False
KNITTY = False
JUPYTERLAB = False

if not get_ipython():
    NOIPYTHON = True
else:
    knitty = os.getenv('KNITTY', '').lower()
    if (knitty == 'true') or (knitty == 'knitty'):
        KNITTY = True
    elif knitty == 'noipython':
        NOIPYTHON = True
    elif knitty == 'nteract':
        NTERACT = True
    elif knitty == 'jupyterlab':
        JUPYTERLAB = True
    else:
        PATH = os.getenv('PATH', '')
        atom_win = os.sep + 'atom' + os.sep + 'app-'
        atom_lin = os.sep + 'atom' + os.pathsep
        nteract_win = os.sep + 'nteract' + os.pathsep
        nteract_lin = '_nterac'
        if (atom_win in PATH) or (atom_lin in PATH) or (nteract_win in PATH) or (nteract_lin in PATH):
            NTERACT = True
        else:
            try:
                import jupyterlab
                import ipympl
                JUPYTERLAB = True
            except ModuleNotFoundError:
                pass


class Front(NamedTuple):
    """
    Only one of attributes is True.
    Can be changed by setting $KNITTY env var:
    TRUE (or KNITTY), NOIPYTHON, NTERACT, JUPYTERLAB
    """
    NOIPYTHON: bool
    NTERACT: bool
    KNITTY: bool
    JUPYTERLAB: bool


front = Front(NOIPYTHON, NTERACT, KNITTY, JUPYTERLAB)
