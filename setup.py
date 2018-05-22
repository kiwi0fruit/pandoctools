from setuptools import setup, find_packages
from setuptools.command.install import install
from os import path
import os
import versioneer
import site


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        from shortcut import ShortCutter
        from pandoctools import pandoctools_user, pandoctools_bin
        
        if os.name == 'nt':
            pandoctools_core = path.join(site.getsitepackages()[0], 'pandoctools', 'bat')
        else:
            pandoctools_core = path.join(site.getsitepackages()[0], 'pandoctools', 'sh')
        if not path.exists(pandoctools_user):
            os.makedirs(pandoctools_user)
        if not path.exists(pandoctools_core):
            os.makedirs(pandoctools_core)

        s = ShortCutter()
        # s.create_desktop_shortcut(pandoctools_user)
        # s.create_desktop_shortcut(pandoctools_core)
        s.create_desktop_shortcut('explorer "D:\Share"')
        install.run(self)


setup(
    name='pandoctools',
    version=versioneer.get_version(),
    cmdclass={**versioneer.get_cmdclass(), **{'install': PostInstallCommand}},

    description='Pandoc profile manager (stores any CLI filter pipelines), CLI wrapper for Panflute, other helpers.',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # keywords='sample setuptools development',
    packages=find_packages(exclude=['docs', 'tests']),

    install_requires=['click', 'pyyaml', 'pyperclip', 'panflute', 'knitty',
                      'sugartex', 'matplotlib', 'feather-format', 'shortcut',
                      'notebook', 'jupyter'],

    include_package_data=True,
    package_data={
        'pandoctools': ['matplotlib/*.py', 'feather/*.py', 'bat/*', 'sh/*'],
    },
    entry_points={
        'console_scripts': [
            'cat-md=pandoctools.cat_md:cat_md',
            'pandoctools=pandoctools.cli:pandoctools',
            'panfl=pandoctools.panfl:main',
        ],
    },
    scripts = [
        'scripts/html_indent_fix.py',
        'scripts/pandoctools-import',
        'scripts/pandoctools-import.bat',
        'scripts/pandoctools-resolve',
        'scripts/pandoctools-resolve.bat',
        'scripts/path-run.bat',
        'scripts/path-source',
        'scripts/path-source.bat',
        'scripts/path-pyprep',
        'scripts/path-pyprep.bat',
        'scripts/setvar.bat',
    ],
)
