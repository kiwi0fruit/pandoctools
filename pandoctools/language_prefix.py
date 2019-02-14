import panflute as pf


# noinspection PyUnusedLocal
def action(elem, doc):
    if isinstance(elem, pf.Code) or isinstance(elem, pf.CodeBlock):
        if elem.classes:
            elem.classes[0] = 'language-' + elem.classes[0]


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
