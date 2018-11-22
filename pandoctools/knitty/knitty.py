import os
import sys
from IPython import get_ipython

KNITTY = False
NONE = False
NTERACT = False
LAB = False
NOTEBOOK = False


knitty = os.getenv('KNITTY', '').lower()
if (knitty == 'true') or (knitty == 'knitty'):
    KNITTY = True
elif knitty == 'none':
    NONE = True
elif knitty == 'nteract':
    NTERACT = True
elif knitty == 'lab':
    LAB = True
elif knitty == 'notebook':
    NOTEBOOK = True
elif not get_ipython():
    NONE = True
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
            LAB = True
        except ModuleNotFoundError:
            NOTEBOOK = True


class Front:
    """
    Class for storing automatically determined
    backend. Only one of attributes is ``True``.

    Can be changed by setting ``$KNITTY`` env var:

    1. TRUE (or KNITTY),
    2. NONE (stands for neither IPython nor Jupyter),
    3. NTERACT (stans for Nteract or Atom/Hydrogen),
    4. LAB (stands for Jupyter Lab),
    5. NOTEBOOK (stands for Jupyter Notebook).
    """
    keys = ('knitty', 'none', 'nteract', 'lab', 'notebook')

    def __init__(self,
                 knitty=False,
                 none=False,
                 nteract=False,
                 lab=False,
                 notebook=False):
        self.KNITTY = bool(knitty)
        self.NONE = bool(none)
        self.NTERACT = bool(nteract)
        self.LAB = bool(lab)
        self.NOTEBOOK = bool(notebook)            


front = Front(KNITTY, NONE, NTERACT, LAB, NOTEBOOK)
