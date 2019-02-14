import os
import os.path as p
import sys
from typing import Tuple
from knitty.tools import where


class PandotoolsError(Exception):
    pass


pandoctools_core = p.join(p.dirname(p.dirname(p.abspath(__file__))), 'sh')
if os.name == 'nt':
    pandoctools_user_data = r"%APPDATA%\pandoc\pandoctools"
    pandoctools_user = p.join(os.environ["APPDATA"], "pandoc", "pandoctools")
    env_path = p.dirname(sys.executable)
    search_dirs = [env_path,
                   p.join(env_path, r'Library\mingw-w64\bin'),
                   p.join(env_path, r'Library\usr\bin'),
                   p.join(env_path, r'Library\bin'),
                   p.join(env_path, 'Scripts'),
                   p.join(env_path, 'bin')]
else:
    pandoctools_user_data = "$HOME/.pandoc/pandoctools"
    pandoctools_user = p.join(os.environ["HOME"], ".pandoc", "pandoctools")
    env_path = p.dirname(p.dirname(sys.executable))
    search_dirs = [p.join(env_path, 'bin')]


def bash_cygpath(bash_from_conf: str='') -> Tuple[str, str]:
    """ Returns (bash, cygpath) """
    if os.name != 'nt':
        return where('bash', search_dirs), ''
    try:
        bash = where('bash', search_dirs)
    except PandotoolsError:
        if p.isfile(bash_from_conf):
            bash = bash_from_conf
        else:
            git = p.expandvars(r'%PROGRAMFILES%\Git')
            for bash in (rf'{git}\bin\bash.exe', rf'{git}\usr\bin\bash.exe'):
                if p.isfile(bash):
                    break
            else:
                raise PandotoolsError(
                    "bash wasn't found in: python environment, $PATH, " +
                    r"win_bash path in config, %PROGRAMFILES%\Git"
                )
    bash_dir = p.dirname(bash)
    return bash, where('cygpath', [bash_dir, rf'{p.dirname(bash_dir)}\usr\bin',
                                   rf'{bash_dir}\usr\bin'])
