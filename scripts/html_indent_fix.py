#!/usr/bin/env python
import panflute as pf
import re

regex = re.compile(r'(^|(?<=\n))( {4}| {0,3}\t)[ \t]*')


def action(elem, doc):
    if isinstance(elem, pf.RawBlock):
        if elem.format == 'html':
            elem.text = regex.sub('   ', elem.text)


def main(doc=None):
    return pf.run_filter(action, doc=doc)

if __name__ == '__main__':
    main()
