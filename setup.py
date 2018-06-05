from setuptools import setup, find_packages
from setuptools.command.install import install
from os import path as p
import os
import configparser
import traceback
from pandoctools.shortcut import ShortCutter
from pandoctools.cli import pandoctools_user
import versioneer
import io
import sys

DEFAULTS_INI = {'profile': 'Default',
                'out': '*.*.md',
                'root_env': '',
                'win_bash': r'%PROGRAMFILES%\Git\bin\bash.exe'}

here = p.abspath(p.dirname(__file__))
with open(p.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


class PostInstallCommand(install):
    """
    Post-installation for installation mode.
    """
    def run(self):
        error_log = io.StringIO()
        sc = ShortCutter(raise_errors=False, error_log=error_log)

        # Set pandoctools_core:
        if os.name == 'nt':
            pandoctools_core = p.join(sc.site_packages, 'pandoctools', 'bat')
            _pandoctools_core = p.join(sc.site_packages, 'pandoctools', 'sh')
            bash_append = ' (Bash)'
        else:
            pandoctools_core = p.join(sc.site_packages, 'pandoctools', 'sh')
            _pandoctools_core = pandoctools_core
            bash_append = ''

        # Create shortcuts:
        sc.create_desktop_shortcut('pandoctools', entry_point=True)
        ret = sc.create_menu_shortcut('pandoctools', entry_point=True)
        pandoctools_bin = ret[1]
        
        sc.create_desktop_shortcut('python')  # TODO remove after testing

        sc.makedirs(pandoctools_user, pandoctools_core, _pandoctools_core)
        sc.create_desktop_shortcut(pandoctools_user, 'Pandoctools User Data')
        sc.create_shortcut(pandoctools_core, pandoctools_user, 'Pandoctools Core Data')
        sc.create_shortcut(_pandoctools_core, pandoctools_user, 'Pandoctools Core Data' + bash_append)

        # Write INI:
        config_file = p.join(pandoctools_user, 'Defaults.ini')
        config = configparser.ConfigParser(interpolation=None)
        default_sect = DEFAULTS_INI.copy()
        if p.exists(config_file):
            config.read(config_file)
            try:
                d = config.items('Default')
                default_sect.update(dict(d))
            except configparser.NoSectionError:
                pass
        default_sect['pandoctools'] = pandoctools_bin
        if p.exists(p.expandvars(default_sect['win_bash'])):
            pandoctools_core = _pandoctools_core

        config['Default'] = default_sect
        with io.StringIO() as file:
            config.write(file)
            config_str = file.getvalue()
        try:
            with open(config_file, 'w') as file:
                config.write(file)
        except:
            print('WARNING: Failed to create ini file.\n\n' + ''.join(traceback.format_exc()), file=error_log)
            print('File:\n{}\n\n{}'.format(config_file, config_str), file=error_log)

        # Dump error log:
        print(error_log.getvalue(), file=open(p.join(p.join(p.expanduser('~')), 'pandoctools_install_error_log.txt'), 'w', encoding="utf-8"))
        error_log.close()

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

    install_requires=['click', 'pyyaml', 'panflute', 'knitty>=0.3.10', 'pandas',
                      'sugartex>=0.1.9', 'matplotlib', 'feather-format',  # 'shortcut',
                      'notebook', 'jupyter', 'winshell;platform_system=="Windows"',
                      'pywin32;platform_system=="Windows"'],

    include_package_data=True,
    package_data={
        'pandoctools': ['bat/*', 'sh/*'],
    },
    entry_points={
        'console_scripts': [
            'cat-md=pandoctools.cat_md.cat_md:cat_md',
            'pandoctools=pandoctools.cli.cli:pandoctools',
            'panfl=pandoctools.panfl.panfl:main',
        ],
    },
    scripts=[
        'scripts/pandoc19_fix_html_indent.py',
        'scripts/pandoctools-import',
        'scripts/pandoctools-import.bat',
        'scripts/pandoctools-resolve',
        'scripts/pandoctools-resolve.bat',
        'scripts/path-run.bat',
        'scripts/path-source',
        'scripts/path-source.bat',
        'scripts/path-pyprep',
        'scripts/path-pyprep-win',
        'scripts/path-pyprep.bat',
        'scripts/setvar.bat',
        'scripts/pandoctools-cygpath',
    ],
)
