import os
from IPython import get_ipython
from typing import NamedTuple

class Fronts(NamedTuple):
    """
    Named tuple with names for automatically determined
    backend stored in ``front`` var that can be changed by
    setting ``$KNITTY`` env var:

    * ``TRUE`` (or ``KNITTY``),
    * ``NONE`` (stands for neither IPython nor Jupyter),
    * ``NTERACT`` (stans for Nteract),
    * ``HYDROGEN`` (stans for Atom / Hydrogen),
    * ``LAB`` (stands for Jupyter Lab),
    * ``NOTEBOOK`` (stands for Jupyter Notebook).
    """
    KNITTY: str
    NONE: str
    NTERACT: str
    HYDROGEN: str
    LAB: str
    NOTEBOOK: str

fronts = Fronts('knitty', 'none', 'nteract', 'hydrogen', 'lab', 'notebook')


knitty = os.getenv('KNITTY', '').lower()
if knitty in fronts:
    front = knitty
elif knitty == 'true':
    front = fronts.KNITTY
elif not get_ipython():
    front = fronts.NONE
else:
    PATH = os.getenv('PATH', '')
    atom_win = os.sep + 'atom' + os.sep + 'app-'
    atom_lin = os.sep + 'atom' + os.pathsep
    nteract_win = os.sep + 'nteract' + os.pathsep
    nteract_lin = '_nterac'
    if (nteract_win in PATH) or (nteract_lin in PATH):
        front = fronts.NTERACT
    elif (atom_win in PATH) or (atom_lin in PATH):
        front = fronts.HYDROGEN
    else:
        try:
            import jupyterlab
            import ipympl
            front = fronts.LAB
        except ModuleNotFoundError:
            front = fronts.NOTEBOOK
