from os import path as p
import configparser
import traceback
import io
import sys
from shortcutter import ShortCutter
from pyppdf.patch_pyppeteer import patch_pyppeteer
from pyppeteer.command import install as install_chromium
from ..shared_vars import pandoctools_user, pandoctools_core

DEFAULTS_INI = {'profile': 'Default',
                'out': '*.*.md',
                'root_env': '',
                'win_bash': r'%PROGRAMFILES%\Git\bin\bash.exe'}


def ready():
    sc = ShortCutter(raise_errors=False, error_log=sys.stderr, activate=False)

    # Create shortcuts:
    sc.create_desktop_shortcut('pandoctools')
    pandoctools_bin = sc.create_menu_shortcut('pandoctools')[1]

    sc.makedirs(pandoctools_user)
    sc.create_desktop_shortcut(pandoctools_user, 'Pandoctools User Data')
    sc.create_shortcut(pandoctools_core, pandoctools_user, 'Pandoctools Core Data')

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

    config['Default'] = default_sect
    with io.StringIO() as file:
        config.write(file)
        config_str = file.getvalue()
    try:
        with open(config_file, 'w') as file:
            config.write(file)
    except:
        print(f'{traceback.format_exc()}\n'+
              'WARNING: Failed to create ini file:\n'+
              f'{config_file}\n\n{config_str}',
              file=sys.stderr)

    # Install chromium for pyppeteer:
    install_chromium()
