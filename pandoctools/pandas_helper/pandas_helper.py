import pandas as pd
import re
from typing import Iterable, Union
from tabulate import tabulate


class TabulateHelperError(Exception):
    pass


def md_table(tabular_data: Union[pd.DataFrame, object],
             headers: tuple = None,
             format_: Union[dict, str, Iterable[str]] = None,
             **kwargs) -> str:
    """
    Converts tabular data like Pandas dataframe to
    GitHub Flavored Markdown table.

    Markdown table format examples:

    * ``{'0': '-:', '-1': ':-:'}`` - only int keys
    * ``dict(foo='-:', bar=':-:', **{'-1': ':-'})`` -
      any keys that incl. column names (has priority if
      all keys are from column names that are integers)
    * ``'--|-:|--'`` or ``'|--|-:|--|'``
    * ``['--', '-:', '--']`` - iterable

    Parameters
    ----------
    tabular_data :
        tabulate.tabulate(tabular_data[,...]) argument
    headers :
        tabulate.tabulate(..., headers[,...]) argument.
        If tabular_data is pd.DataFrame then default is
        tabular_data.columns converted to Tuple[str]
    format_ :
        GitHub Flavored Markdown table align format
    kwargs :
        Other tabulate.tabulate(...) keyword arguments
    """
    if (headers is None) and isinstance(tabular_data, pd.DataFrame):
        headers = tuple(map(str, tabular_data.columns))

    if headers is not None:
        kwargs['headers'] = headers
    kwargs['tablefmt'] = "pipe"

    md_tbl = tabulate(tabular_data, **kwargs)

    def apply_format(m):
        nonlocal headers, format_
        string = m.group(0)

        default_formats = string.split('|')
        width = len(default_formats)

        # Determine if headers can be used as keys if format_ is a dict:
        # ---------------------------------------------
        good_headers = False
        if headers is None:
            pass
        elif (
            len(default_formats) == len(set(headers)) and
            all(isinstance(hdr, str) for hdr in headers)
        ):
            good_headers = True

        # Process format_ to formats:
        # ---------------------------------------------
        if isinstance(format_, dict):
            _headers = tuple(headers)
            if good_headers and all(key in _headers for key in format_.keys()):
                formats = [format_.get(key, '') for key in headers]
            else:
                try:
                    formats = [''] * width
                    for ikey in format_.keys():
                        i = int(ikey)  # can raise ValueError
                        if (i >= 0) and (i < width):
                            formats[i] = format_[ikey]
                        elif (i < 0) and (-i <= width):
                            formats[width + i] = format_[ikey]
                except ValueError:
                    # there is a non int key in the format_ dict
                    formats = [format_.get(key, '') for key in headers] if good_headers else [''] * width

        elif format_ is None:
            formats = [''] * width
        else:
            if isinstance(format_, str):
                fmts = format_.split('|')
                fmts = fmts[(1 if fmts[0] == '' else 0):(-1 if fmts[-1] == '' else None)]
            else:
                fmts = list(format_)
            formats = (fmts + [''] * width)[:width]

        # Check formats:
        # ---------------------------------------------
        for fmt in formats:
            try:
                if not re.match(r'^:?-+:?$', fmt):
                    raise ValueError("Incorrect Markdown table format: '{}'".format(fmt))
            except TypeError as e:
                raise TypeError("Incorrect Markdown table format: '{}'. {}".format(fmt, e))

        # Apply custom formats to default_formats:
        # ---------------------------------------------
        formats = (fmt[0] + def_fmt[1:-1] + fmt[-1] if fmt else def_fmt
                   for fmt, def_fmt in zip(formats, default_formats))
        return '|'.join(formats)

    # Convert:
    # --------
    return re.sub(r'(?<=\n\|):?-+:?(\|:?-+:?)*(?=\|\r?\n)', apply_format, md_tbl, count=1)


def md_header(tabular_data: Union[pd.DataFrame, object],
              headers: tuple = None,
              **kwargs) -> str:
    """
    Converts tabular data like Pandas dataframe to
    GitHub Flavored Markdown table

    **but** prints only table header + empty row.

    Parameters
    ----------
    tabular_data :
        tabulate.tabulate(tabular_data[,...]) argument
    headers :
        tabulate.tabulate(..., headers[,...]) argument.
        If tabular_data is pd.DataFrame then default is
        tabular_data.columns converted to Tuple[str]
    kwargs :
        Other tabulate.tabulate(...) keyword arguments

    Returns
    -------
    md :
        Markdown table header + empty row
    """
    iter_rows = re.finditer(r'(^|(?<=\n))[^\r\n]*((?=\r?\n)|$)',
                            md_table(tabular_data, headers, **kwargs))
    # noinspection PyUnusedLocal
    rows = [next(iter_rows).group(0) for i in (0, 1)]
    rows.append(re.sub(r'[^ |]', ' ', rows[1]))
    return '\n'.join(rows)
