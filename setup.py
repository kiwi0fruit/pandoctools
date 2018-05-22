from setuptools import setup, find_packages
from setuptools.command.install import install
from os import path as p
import os
import versioneer


here = p.abspath(p.dirname(__file__))

with open(p.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def folder_shortcut(shortcut_name, target_path, sc):
    if os.name == 'nt':
        from win32com.client import Dispatch
        import winshell
    
        shell = Dispatch('WScript.Shell')
        shortcut_file = p.join(winshell.desktop(), shortcut_name + '.lnk')
        shortcut = shell.CreateShortCut(shortcut_file)
        shortcut.Targetpath = target_path
        shortcut.WorkingDirectory = target_path
        shortcut.save()
    else:
        # sc.create_desktop_shortcut(target_path)
        import subprocess
        desktop = subprocess.check_output(['xdg-user-dir', 'DESKTOP'])
        dir_ = p.join(desktop, shortcut_name)
        if not p.exists(dir_):
            os.makedirs(dir_)
        os.symlink(dir_, target_path)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        from shortcut import ShortCutter
        from pandoctools import pandoctools_user, pandoctools_bin
        
        if os.name == 'nt':
            import sys
            pandoctools_core = p.join(p.dirname(sys.executable), 'Lib', 'site-packages', 'pandoctools', 'bat')
            if not p.exists(pandoctools_bin):
                open(pandoctools_bin, 'a').close()
        else:
            import site
            pandoctools_core = p.join(site.getsitepackages()[0], 'pandoctools', 'sh')

        if not p.isdir(pandoctools_user):
            os.makedirs(pandoctools_user)
        if not p.isdir(pandoctools_core):
            os.makedirs(pandoctools_core)

        sc = ShortCutter()
        sc.create_desktop_shortcut(pandoctools_bin)
        folder_shortcut('Pandoctools User Data', pandoctools_user, sc)
        folder_shortcut('Pandoctools Core Data', pandoctools_core, sc)
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
                      'notebook', 'jupyter', 'winshell', 'pywin32'],

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
