from IPython.display import display
import pandas as pd
from ..knitty import KNITTY


def md_table(df: pd.DataFrame, hide: bool=False) -> str:
    """
    Displays table and returns it's Markdown string.

    Parameters
    ----------
    df :
        ...
    hide :
        whether to display via IPython or not (KNITTY OS env var sets hide=True)

    Returns
    -------
    md :
        Markdown table
    """
    if KNITTY:
        hide = True
    if not hide:
        # noinspection PyTypeChecker
        display(df)
    # noinspection PyUnusedLocal
    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    return df_formatted.to_csv(sep='|', index=False)


def md_header(df: pd.DataFrame, hide: bool=False) -> str:
    """
    Displays header of the table and returns it's Markdown string.

    Parameters
    ----------
    df :
        ...
    hide :
        whether to display via IPython or not (KNITTY OS env var sets hide=True)

    Returns
    -------
    md :
        Markdown table header + empty row
    """
    md = md_table(df.iloc[[0]], hide=True).split('\n')
    md[2] = md[1].replace('---', ' ')
    md = '\n'.join(md)

    if KNITTY:
        hide = True
    if not hide:
        # noinspection PyTypeChecker
        display(df.iloc[[0]].drop(index=0))

    return md
