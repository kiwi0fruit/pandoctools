from setuptools import setup, find_packages
from setuptools.command.install import install
from os import path as p
import os
import configparser
import traceback
from pandoctools.shortcut import ShortCutter
from pandoctools.cli import pandoctools_user, pandoctools_bin
import versioneer
import io


here = p.abspath(p.dirname(__file__))

with open(p.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def desktop_dir_shortcut(shortcut_name, target_path):
    if not p.isdir(target_path):
        os.makedirs(target_path)
    if os.name == 'nt':
        from win32com.client import Dispatch
        import winshell
        shell = Dispatch('WScript.Shell')
        shortcut_file = p.join(winshell.desktop(), shortcut_name + '.lnk')
        shortcut = shell.CreateShortCut(shortcut_file)
        shortcut.Targetpath = target_path
        shortcut.WorkingDirectory = target_path
        shortcut.save()
        return ""
    elif os.name != 'darwin':
        import subprocess
        desktop = subprocess.check_output([
            'xdg-user-dir',
            'DESKTOP'
        ]).decode('utf-8').strip()
        shortcut_path = p.join(desktop, shortcut_name)
        if p.exists(shortcut_path):
            os.remove(shortcut_path)
        os.symlink(target_path, shortcut_path)
        return ""
    else:
        return 'WARNING: "{}" folder shortcut was not implemented for macOS.'


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        error_log = ""

        # Set pandoctools_core:
        if os.name == 'nt':
            import sys
            _pdt = p.join(p.dirname(sys.executable), 'Lib', 'site-packages', 'pandoctools')
            pandoctools_core = p.join(_pdt, 'bat')
            _pandoctools_core = p.join(_pdt, 'sh')
            bash_append = ' (Bash)'
        else:
            import site
            pandoctools_core = p.join(site.getsitepackages()[0], 'pandoctools', 'sh')
            _pandoctools_core = pandoctools_core
            bash_append = ''

        # Create shortcuts:
        if not p.exists(pandoctools_bin):
            open(pandoctools_bin, 'a').close()
        try:
            sc = ShortCutter()
            sc.create_desktop_shortcut(pandoctools_bin)
            error_log += desktop_dir_shortcut('Pandoctools User Data', pandoctools_user)
            error_log += desktop_dir_shortcut('Pandoctools Core Data', pandoctools_core)
            error_log += desktop_dir_shortcut('Pandoctools Core Data' + bash_append, _pandoctools_core)
        except:
            error_log += 'WARNING: Failed to create desktop shortcuts.\n\n' + ''.join(traceback.format_exc())

        # Write INI:
        config_file = p.join(pandoctools_user, 'Defaults.ini')
        config = configparser.ConfigParser(interpolation=None)
        if p.exists(config_file):
            config.read(config_file)
            try:
                default_sect = dict(config.items('Default'))
            except configparser.NoSectionError:
                default_sect = {}
        else:
            default_sect = {}

        default_sect['pandoctools'] = pandoctools_bin
        if 'root_env' not in default_sect:
            default_sect['root_env'] = ''
        if 'win_bash' not in default_sect:
            git_bash = r'%PROGRAMFILES%\Git\bin\bash.exe'
            if p.exists(p.expandvars(git_bash)):
                default_sect['win_bash'] = git_bash
                pandoctools_core = _pandoctools_core
            else:
                default_sect['win_bash'] = ''

        config['Default'] = default_sect
        with io.StringIO() as f:
            config.write(f)
            config_str = f.getvalue()
        try:
            with open(config_file, 'w') as f:
                config.write(f)
        except:
            error_log += 'WARNING: Failed to create ini file.\n\n' + ''.join(traceback.format_exc())
            error_log += '\nFile:\n{}\n\n{}'.format(config_file, config_str)
        
        # Dump error log:
        if error_log != "":
            print(error_log, file=open(p.join(pandoctools_core, 'install_error_log.txt'), 'w', encoding="utf-8"))

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

    install_requires=['click', 'pyyaml', 'panflute', 'knitty',
                      'sugartex', 'matplotlib', 'feather-format',  # 'shortcut',
                      'notebook', 'jupyter', 'pyperclip;platform_system=="Windows"', 
                      'winshell;platform_system=="Windows"',
                      'pywin32;platform_system=="Windows"'],

    include_package_data=True,
    package_data={
        'pandoctools': ['matplotlib/*.py', 'feather/*.py', 'bat/*', 'sh/*'],
    },
    entry_points={
        'console_scripts': [
            'cat-md=pandoctools.cat_md.cat_md:cat_md',
            'pandoctools=pandoctools.cli.cli:pandoctools',
            'panfl=pandoctools.panfl.panfl:main',
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
        'scripts/path-pyprep-win',
        'scripts/path-pyprep.bat',
        'scripts/setvar.bat',
        'scripts/pandoctools-cygpath',
    ],
)
