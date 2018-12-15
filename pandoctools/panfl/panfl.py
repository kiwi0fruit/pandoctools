"""
Allow Panflute to be run as a command line script
(so it can be used in Pandoctools shell scripts)

Code taken from Panflute:
BSD 3-clause "New" or "Revised" License
https://github.com/sergiocorreia/panflute

Copyright (c) 2016, Sergio Correia

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of Sergio Correia nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import sys
from collections import OrderedDict

from panflute import load, dump, debug
import click
import re


@click.command(help="Filters should have basename only (may be with or without .py extension). " +
               "Search preserves directories order (except for --data-dir and `sys.path`).")
@click.argument('filters', nargs=-1)
@click.option('-w', '-t', '--write', '--to', 'to', type=str, default='html',
              help='Pandoc writer option.')
@click.option('--dir', '-d', 'dirs', multiple=True,
              help="Search filters in provided directories: `-d dir1 -d dir2`.")
@click.option('--data-dir', is_flag=True, default=False,
              help="Search filters in default user data directory listed in `pandoc --version` " +
                   "(in it's `filters` subfolder actually). It's appended to the search list.")
@click.option('--no-sys-path', is_flag=True, default=False,
              help="Disable search filters in python's `sys.path` (I tried to remove current working directory either way) " +
              "that is appended to the search list.")
def main(filters, to, dirs, data_dir, no_sys_path):
    if len(sys.argv) > 1:
        sys.argv[1] = to
    doc = load()
    filters = list(filters)
    dirs = list(dirs)

    verbose = doc.get_metadata('panflute-verbose', False)

    # Display message (tests that everything is working ok)
    msg = doc.get_metadata('panflute-echo', False)
    if msg:
        debug(msg)

    if filters:
        if verbose:
            msg = "panflute: will run the following filters:"
            debug(msg, ' '.join(filters))
        doc = autorun_filters(filters, doc, dirs, data_dir, not no_sys_path, verbose)
    elif verbose:
        debug("panflute: no filters found in metadata")

    dump(doc)


def autorun_filters(filters: list, doc, search_path: list, data_dir: bool, sys_path: bool, verbose):
    if data_dir:
        if os.name == 'nt':
            search_path.append(os.path.join(os.environ["APPDATA"], "pandoc", "filters"))
        else:
            search_path.append(os.path.join(os.environ["HOME"], ".pandoc", "filters"))
    if sys_path:
        search_path += [dir_ for dir_ in sys.path if (dir_ != '') and (dir_ != '.') and os.path.isdir(dir_)]

    filenames = OrderedDict()

    for fil in filters:
        for path in search_path:
            # Allow with and without .py ending
            filter_path = os.path.join(path, fil + ('' if fil.endswith('.py') else '.py'))

            if os.path.isfile(filter_path):
                if verbose:
                    debug("panflute: filter <{}> found in {}".format(fil, filter_path))
                filenames[fil] = filter_path
                break
            elif verbose:
                debug("          filter <{}> NOT found in {}".format(fil, filter_path))
        else:
            raise Exception("filter not found: " + fil)

    for fil, filter_path in filenames.items():
        globals_dict = dict()
        if verbose:
            debug("panflute: running filter <{}>".format(fil))
        with open(filter_path) as fp:
            code = fp.read()
        exec(code, globals_dict)
        try:
            doc = globals_dict['main'](doc)
        except:
            debug("Failed to run filter: " + fil)
            if 'main' not in globals_dict:
                debug(' - Possible cause: filter lacks a main() function')
            debug('Filter code:')
            debug('-' * 64)
            debug(code)
            debug('-' * 64)
            raise
        if verbose:
            debug("panflute: filter <{}> completed".format(fil))

    return doc
