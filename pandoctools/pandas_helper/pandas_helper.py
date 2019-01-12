import pandas as pd
import re
from typing import Iterable, Union, Tuple
from tabulate import tabulate

first_two_lines = re.compile(r'^(?P<first_line>[^\r\n]*)\r?\n([^\r\n]*(?=\r?\n)|[^\r\n]+$)')


class TabulateHelperError(Exception):
    pass


def join_row(row: Iterable[str]) -> str:
    return '|' + '|'.join(row) + '|'


def get_headers_and_formats(string: str) -> Tuple[Tuple[str, ...], ...]:
    """
    Returns (headers, formats).
    Or (formats,) if header is absent.
    """
    err = 'tabulate returned GFM pipe table with invalid first two lines: {}'
    lines = list(map(lambda s: s.rstrip('\r'), string.split('\n', 2)[:2]))
    ret, formats = [], None
    for line in reversed(lines):
        if formats:
            match = re.match(r'^\|.*[^\\]\|$', line)
            headers = tuple(map(
                lambda s: s.strip(' '),
                re.split(r'(?<=[^\\])\|', line[1:-1])
            ))
            if match and len(headers) == len(formats):
                ret = [headers] + ret
            else:
                raise TabulateHelperError(err.format(lines))
        elif re.match(r'^\|:?-+:?(\|:?-+:?)*\|$', line):
            formats = tuple(line[1:-1].split('|'))
            ret.append(formats)
    if ret:
        return tuple(ret)
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
        tabulate.tabulate(..., headers[,...]) optional argument.
        If None and tabular_data is pd.DataFrame then default is
        tabular_data.columns converted to Tuple[str].
        If None then use tabulate.tabulate(...) default
        (but in this particular case if it's absent in the output
        then add blank header).
    showindex :
        tabulate.tabulate(..., showindex[,...]) optional argument.
    formats :
        GitHub Flavored Markdown table align format
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
        headers_fmts = get_headers_and_formats(m.group(0))
        _headers = '' if (len(headers_fmts) == 1) else headers_fmts[0]
        default_formats = headers_fmts[-1]
        width = len(default_formats)
        # Determine if headers can be used as keys if formats is a dict:
        good_headers = len(default_formats) == len(set(_headers))
        # Set headers Markdown code:
        if _headers:
            md_headers = m.group('first_line') + '\n'
        elif headers is None:
            md_headers = re.sub(r'[^|]', ' ', join_row(default_formats)) + '\n'
        else:
            md_headers = ''

        # Process formats to custom formats:
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

        # Check custom formats:
        # ---------------------------------------------
        for fmt in _formats:
            try:
                if not re.match(r'^:?-+:?$', fmt) and fmt:
                    raise ValueError("Incorrect Markdown table format: '{}'".format(fmt))
            except TypeError as e:
                raise TypeError("Incorrect Markdown table format: '{}'. {}".format(fmt, e))

        # Apply custom formats to default_formats:
        # ---------------------------------------------
        _formats = join_row(fmt[0] + def_fmt[1:-1] + fmt[-1] if fmt else def_fmt
                            for fmt, def_fmt in zip(_formats, default_formats))
        # ---------------------------------------------
        return md_headers + _formats

    # Convert:
    # --------
    if first_two_lines.match(md_tbl):
        return first_two_lines.sub(apply_format, md_tbl, count=1)
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
        tabulate.tabulate(..., headers[,...]) optional argument.
        If None and tabular_data is pd.DataFrame then default is
        tabular_data.columns converted to Tuple[str].
        If None then use tabulate.tabulate(...) default
        (but in this particular case if it's absent in the output
        then add blank header).
    showindex :
        tabulate.tabulate(..., showindex[,...]) optional argument.
    formats :
        GitHub Flavored Markdown table align format
    kwargs :
        Other tabulate.tabulate(...) optional keyword arguments

    Returns
    -------
    md :
        Markdown table header + empty row
    """
    md_tbl = md_table(tabular_data, headers=headers, showindex=showindex,
                      formats=formats, **kwargs)
    match = first_two_lines.match(md_tbl)
    headers_fmts = get_headers_and_formats(match.group(0))
    if len(headers_fmts) == 1:
        return ''
    else:
        # noinspection PyListCreation
        rows = [match.group('first_line'), join_row(headers_fmts[-1])]
        rows.append(re.sub(r'[^ |]', ' ', rows[1]))
        return '\n'.join(rows)
