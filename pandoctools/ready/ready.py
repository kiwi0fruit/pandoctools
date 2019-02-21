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
    sc.create_menu_shortcut('pandoctools')

    sc.makedirs(pandoctools_user)
    sc.create_desktop_shortcut(pandoctools_user, 'Pandoctools User Data')
    sc.create_shortcut(pandoctools_core, pandoctools_user, 'Pandoctools Core Data')

    # Find Pandoctools exec:
    _bin = sc.find_target('pandoctools')
    if not _bin:
        _bin = sc.find_target(p.join(sc.bin_folder_shcut, 'pandoctools'))
        if not _bin:
            print("'pandoctools' was not found neither in the $PATH nor in the env.", file=sys.stderr)
            _bin = ''

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
    default_sect['pandoctools'] = _bin

    config['Default'] = default_sect
    with io.StringIO() as file:
        config.write(file)
        config_str = file.getvalue()
    try:
        with open(config_file, 'w') as file:
            config.write(file)
    except Exception:
        print(f'{traceback.format_exc()}\n'+
              'WARNING: Failed to create ini file:\n'+
              f'{config_file}\n\n{config_str}',
              file=sys.stderr)

    # Install chromium for pyppeteer:
    install_chromium()
