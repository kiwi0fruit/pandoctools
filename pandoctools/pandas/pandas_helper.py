from IPython.display import display
import pandas as pd
_knitty = False


def ready(knitty: bool=False):
    """
    Set current knitty option that later can be used by ``md_table``. Initial is False.
    """
    global _knitty
    _knitty = knitty


def md_table(df: pd.DataFrame, knitty: bool or None=None, hide: bool=False) -> str:
    """
    Displays table and returns it's Markdown string.
    If knitty - do not display.
    
    Parameters
    ----------
    knitty : whether we run Knitty or Hydrogen
        None means use previous value. Initial is False
    hide : whether to display table via IPython

    Returns
    -------
    Markdown table if knitty is True
    else ""
    """
    global _knitty

    # noinspection PyUnusedLocal
    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    _md_table = df_formatted.to_csv(sep="|", index=False)

    if knitty is not None:
        _knitty = knitty

    if _knitty:
        hide = True

    if not hide:
        # noinspection PyTypeChecker
        display(df)
    return _md_table if _knitty else ""
