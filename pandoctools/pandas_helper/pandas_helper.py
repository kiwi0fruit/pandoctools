import pandas as pd
import re
from typing import Iterable, Union, Tuple
from tabulate import tabulate


class TabulateHelperError(Exception):
    pass


def join_row(row: Iterable[str]) -> str:
    return '|' + '|'.join(row) + '|'


def get_headers_and_formats(string: str) -> Tuple[str, Tuple[str, ...], Tuple[str, ...]]:
    """
    Returns ``(md_headers, headers, formats)``.
    First is a pipe format str, second is a tuple of str keys.
    Or returns ``('', (), formats)`` if header is absent.
    """
    err = 'tabulate returned GFM pipe table with invalid first two lines: {}'
    lines = list(map(lambda s: s.rstrip('\r'), string.split('\n', 2)[:2]))
    md_headers, headers, formats = '', (), None
    for line in reversed(lines):
        if formats:
            match = re.match(r'^\|.*[^\\]\|$', line)
            headers = tuple(map(
                lambda s: s.strip(' '),
                re.split(r'(?<=[^\\])\|', line[1:-1])
            ))
            if match and len(headers) == len(formats):
                md_headers = line
            else:
                raise TabulateHelperError(err.format(lines))
        elif re.match(r'^\|:?-+:?(\|:?-+:?)*\|$', line):
            formats = tuple(line[1:-1].split('|'))
    if formats:
        return md_headers, headers, formats
    else:
        raise TabulateHelperError(err.format(lines))


def md_table(tabular_data: Union[pd.DataFrame, object],
             headers: tuple = None,
             showindex: Union[bool, None] = False,
             formats: Union[dict, str, Iterable[str]] = None,
             **kwargs) -> str:
    """
    Converts tabular data like Pandas dataframe to
    GitHub Flavored Markdown table.

    Markdown table ``formats`` examples:

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
        tabulate.tabulate(..., headers[,...]) optional argument.
        If None and tabular_data is pd.DataFrame then default is
        tabular_data.columns converted to Tuple[str, ...].
        If None then use tabulate.tabulate(...) default
        (but in this particular case if it's absent in the output
        then add blank header).
    showindex :
        tabulate.tabulate(..., showindex[,...]) optional argument.
    formats :
        GitHub Flavored Markdown table align formats
    kwargs :
        Other tabulate.tabulate(...) optional keyword arguments

    Returns
    -------
    md :
        Markdown table
    """
    if (headers is None) and isinstance(tabular_data, pd.DataFrame):
        headers = tuple(map(str, tabular_data.columns))

    if headers is not None:
        kwargs['headers'] = headers
    kwargs['tablefmt'] = "pipe"
    kwargs['showindex'] = showindex

    md_tbl = tabulate(tabular_data, **kwargs)

    def apply_format(m):
        md_headers, _headers, default_formats = get_headers_and_formats(m.group(0))
        width = len(default_formats)
        # Determine if headers can be used as keys if formats is a dict:
        good_headers = len(default_formats) == len(set(_headers))
        # Set headers Markdown code:
        if not _headers and (headers is None):
            md_headers = re.sub(r'[^|]', ' ', join_row(default_formats)) + '\n'

        # Process formats to custom _formats:
        # ---------------------------------------------
        if isinstance(formats, dict):
            if good_headers and all(key in _headers for key in formats.keys()):
                _formats = [formats.get(key, '') for key in _headers]
            else:
                try:
                    _formats = [''] * width
                    for ikey in formats.keys():
                        i = int(ikey)  # can raise ValueError
                        if (i >= 0) and (i < width):
                            _formats[i] = formats[ikey]
                        elif (i < 0) and (-i <= width):
                            _formats[width + i] = formats[ikey]
                except ValueError:
                    # there is a non int key in the formats dict
                    _formats = [formats.get(key, '') for key in _headers] if good_headers else [''] * width

        elif formats is None:
            _formats = [''] * width
        else:
            if isinstance(formats, str):
                fmts = formats.split('|')
                fmts = fmts[(1 if fmts[0] == '' else 0):(-1 if fmts[-1] == '' else None)]
            else:
                fmts = list(formats)
            _formats = ([''] * (width - len(fmts)) + fmts)[:width]

        # Check custom _formats:
        # ---------------------------------------------
        for fmt in _formats:
            try:
                if not re.match(r'^:?-+:?$', fmt) and fmt:
                    raise ValueError("Incorrect Markdown table format: '{}'".format(fmt))
            except TypeError as e:
                raise TypeError("Incorrect Markdown table format: '{}'. {}".format(fmt, e))

        # Apply custom _formats to default_formats:
        # ---------------------------------------------
        _formats = join_row(fmt[0] + def_fmt[1:-1] + fmt[-1] if fmt else def_fmt
                            for fmt, def_fmt in zip(_formats, default_formats))
        # ---------------------------------------------
        nonlocal found
        found = True
        return md_headers + ('\n' if md_headers else '') + _formats

    # Convert:
    # --------
    found = False
    ret = re.sub(r'^([^\r\n]*)\r?\n([^\r\n]*(?=\r?\n)|[^\r\n]+$)',
                 apply_format, md_tbl, count=1)
    if found:
        return ret
    else:
        raise TabulateHelperError('tabulate helper cannot find two lines in tabulate output')


def md_header(tabular_data: Union[pd.DataFrame, object],
              headers: tuple = None,
              showindex: Union[bool, None] = False,
              formats: Union[dict, str, Iterable[str]] = None,
              **kwargs) -> str:
    """
    Converts tabular data like Pandas dataframe to
    GitHub Flavored Markdown table

    **but** prints only table header + empty row.
    If header is absent then returns empty string.

    Markdown table ``formats`` examples:

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
        tabulate.tabulate(..., headers[,...]) optional argument.
        If None and tabular_data is pd.DataFrame then default is
        tabular_data.columns converted to Tuple[str, ...].
        If None then use tabulate.tabulate(...) default
        (but in this particular case if it's absent in the output
        then add blank header).
    showindex :
        tabulate.tabulate(..., showindex[,...]) optional argument.
    formats :
        GitHub Flavored Markdown table align formats
    kwargs :
        Other tabulate.tabulate(...) optional keyword arguments

    Returns
    -------
    md :
        Markdown table header + empty row
    """
    md_tbl = md_table(tabular_data, headers=headers, showindex=showindex,
                      formats=formats, **kwargs)
    md_headers, headers, fmts = get_headers_and_formats(md_tbl)
    if not headers:
        return ''
    else:
        fmts = join_row(fmts)
        return '\n'.join((md_headers, fmts, re.sub(r'[^ |]', ' ', fmts)))
