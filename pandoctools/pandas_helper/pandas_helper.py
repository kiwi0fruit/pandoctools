import pandas as pd
import re
from typing import Iterable, Union


def md_table(df: pd.DataFrame, format_: Union[dict, str, Iterable[str]]=None) -> str:
    """
    Converts Pandas dataframe to Markdown table.

    Markdown table format examples:

    * ``{'0': '-:', '-1': ':-:'}`` - only int keys
    * ``dict(foo='-:', bar=':-:')`` - non int keys that are column names
    * ``'--|-:|--'`` or ``'|--|-:|--|'``
    * ``['--', '-:', '--']`` - list
    """
    # Process format_:
    # ----------------
    L = len(df.columns)
    DEFAULT = '---'

    if format_ is None:
        format_ = [DEFAULT for i in range(L)]
    elif isinstance(format_, dict):
        try:
            tmp_format = {}
            for key in format_.keys():
                ikey = int(key)  # can raise ValueError exception
                if ikey >= 0:
                    tmp_format[key] = format_[key]
                elif -ikey <= L:
                    tmp_format[str(L + ikey)] = format_[key]
            # can no longer raise ValueError exception
            format_ = [tmp_format.get(str(i), DEFAULT) for i in range(L)]
        except ValueError:
            # there is a non int key in the format_ dict
            format_ = [format_.get(key, DEFAULT) for key in list(df.columns)]
    else:
        if isinstance(format_, str):
            format_ = filter(None, format_.split('|'))
        format_ = list(format_)
        format_ = [(format_[i] if i < len(format_) else DEFAULT) for i in range(L)]

    # Check format_:
    # --------------
    regex = re.compile(r'^:?-+:?$')
    for fmt in format_:
        try:
            if not regex.match(fmt):
                raise ValueError("Incorrect Markdown table format: '{}'".format(fmt))
        except TypeError as e:
            raise TypeError("Incorrect Markdown table format: '{}'. {}".format(fmt, e))

    # Convert:
    # --------
    df_format = pd.DataFrame([format_], columns=df.columns)
    df_formatted = pd.concat([df_format, df])
    return df_formatted.to_csv(sep='|', index=False, na_rep='NaN')


def md_header(df: pd.DataFrame) -> str:
    """
    Returns
    -------
    md :
        Markdown table header + empty row
    """
    md = md_table(df.iloc[[0]]).split('\n')
    md[2] = re.sub(r'[^\s|]', '   ', md[2])
    return '\n'.join(md)
