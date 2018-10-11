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
        whether to display table via IPython or not

    Returns
    -------
    md :
        Markdown table if KNITTY is True (OS env var)
        else ""
    """
    # noinspection PyUnusedLocal
    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    md = df_formatted.to_csv(sep="|", index=False)

    if KNITTY:
        hide = True
    if not hide:
        # noinspection PyTypeChecker
        display(df)
    return md if KNITTY else ""
