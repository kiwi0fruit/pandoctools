import pandas as pd
import re
from typing import Iterable, Union
from tabulate import tabulate


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
    DEFAULT = '---'
    columns = list(df.columns)
    if format_ is None:
        format_ = {}
    elif isinstance(format_, dict):
        try:
            tmp_format = {}
            L = len(df.columns)
            for int_key in format_.keys():
                i = int(int_key)  # can raise ValueError exception
                if i >= 0:
                    tmp_format[columns[i]] = format_[int_key]
                elif -i <= L:
                    tmp_format[columns[L + i]] = format_[int_key]
            # can no longer raise ValueError exception
            format_ = tmp_format
        except ValueError:
            # there is a non int key in the format_ dict
            format_ = {key: format_.get(key) for key in columns if format_.get(key)}
    else:
        if isinstance(format_, str):
            format_ = filter(None, format_.split('|'))
        format_ = list(format_)
        format_ = {key: format_[i] for i, key in enumerate(columns) if i < len(format_)}

    # [DEFAULT for i in range(L)]
    # format_ = [tmp_format.get(str(i), DEFAULT) for i in range(L)]
    # format_ = [format_.get(key, DEFAULT) for key in list(df.columns)]
    # format_ = [(format_[i] if i < len(format_) else DEFAULT) for i in range(L)]
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
    tabulate(df, headers=df.columns, tablefmt="pipe")
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
