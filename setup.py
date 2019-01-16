from setuptools import setup, find_packages

import os
import versioneer

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pandoctools',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description='Profile manager of text processing pipelines: Pandoc filters, any text CLI filters. Atom+Markdown+Pandoc+Jupyter workflow, export to ipynb.',
    long_description=long_description,

    url='https://github.com/kiwi0fruit/pandoctools',

    author='Peter Zagubisalo',
    author_email='peter.zagubisalo@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    # keywords='sample setuptools development',
    packages=find_packages(exclude=['docs', 'tests']),

    install_requires=['click', 'pyyaml', 'notebook', 'jupyter', 'certifi', 
                      'panflute>=1.11.1', 'knitty>=0.4.14', 'pyppeteer>=0.0.25',
                      'sugartex>=0.1.13', 'shortcutter>=0.1.8'],
    # pandoctools: "pip>=10.0.1" "pandoc>=2.3.1" click pyyaml notebook jupyter certifi
    # shortcutter: pywin32 {win}
    # panflute: future shutilwhich [click pyyaml]
    # knitty: jupyter_core traitlets ipython jupyter_client nbconvert pandocfilters
    #         pypandoc psutil nbformat pandoc-attributes [click pyyaml panflute]
    # pyppeteer: websockets appdirs urllib3 tqdm [pyee]
    # pyee: --  # sugartex: [panflute]

    include_package_data=True,
    package_data={
        'pandoctools': ['sh/*'],
    },
    entry_points={
        'console_scripts': [
            'cat-md=pandoctools.cat_md.cat_md:cli',
            'pandoctools=pandoctools.cli.cli:pandoctools',
            'pandoc-filter-arg=pandoctools.pandoc_filter_arg.cli:cli',
            'pandoctools-pyppeteer-pdf=pandoctools.pyppeteer_pdf.pyppeteer_pdf:cli',
            'pandoctools-resolve{}=pandoctools.pandoctools_resolve.resolve:cli'.format(
                '-win' if os.name == 'nt' else ''
            ),
        ],
    },
    scripts=[
        'scripts/pandoctools-source',
        'scripts/pandoctools-python-to-path',
        'scripts/pandoctools-cygpath',
    ] + ([
        'scripts/pandoctools-resolve',
    ] if os.name == 'nt' else []),
)
