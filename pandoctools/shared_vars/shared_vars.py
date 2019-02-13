import os
import os.path as p
import sys
import yaml
import re
from typing import Tuple, Union, Iterable

yaml_regex = re.compile(r'(?:^|\n)---\n(.+?\n)(?:---|\.\.\.)(?:\n|$)', re.DOTALL)


class PandotoolsError(Exception):
    pass


def load_yaml(string: Union[str, None], del_yaml: bool=False) -> Tuple[str, dict]:
    """
    returns (string_without_first_yaml, first_yaml_dict) if del_yaml
            else (string, first_yaml_dict)
    """
    if isinstance(string, str) and string:
        found = yaml_regex.search(string)
        if found:
            yml = yaml.load(found.group(1))
            if del_yaml:
                string = yaml_regex.sub('\n\n', string, 1)
            if not isinstance(yml, dict):
                yml = {}
            return string, yml
        else:
            return string, {}
    return '', {}


def get(maybe_dict, key: str, default=None):
    """returns ``default`` if ``maybe_dict`` is not a ``dict``"""
    return maybe_dict.get(key, default) if isinstance(maybe_dict, dict) else default


def where(executable: str, search_dirs_: Iterable[str]=None, exe_only: bool=True) -> str:
    """
    :param executable: exec name without .exe, .bat or .cmd
    :param search_dirs_: extra dirs to look for executables
    :param exe_only: on Windows search for executable.exe only.
      If False then search for .exe .bat .cmd (in this order).
    :return: On Windows: absolute path to the exec that was found
      in the search_dirs or in the $PATH.
      On Unix: absolute path to the exec that was found in the search_dirs
      or shutil.which('executable') if it is not None.
      If wasn't found raises PandotoolsError.
    """
    if not (os.name == 'nt'):
        extensions = ('',)
    elif exe_only:
        extensions = ('.exe',)
    else:
        extensions = ('.exe', '.bat', '.cmd')
    if not search_dirs_:
        search_dirs_ = ()

    for _dir in search_dirs_:
        for ext in extensions:
            exe = p.abspath(p.normpath(p.join(_dir, f'{executable}{ext}')))
            if p.isfile(exe):
                if os.name == 'nt':
                    return exe
                elif os.access(exe, os.X_OK):
                    return exe

    if os.name == 'nt':
        from subprocess import run, PIPE
        for ext in extensions:
            exe = f'{executable}{ext}'.lower()
            exe_abs = run([p.expandvars(r'%WINDIR%\System32\where.exe'), f'$PATH:{exe}'],
                          stdout=PIPE, stderr=PIPE)
            if not exe_abs.stderr:
                execs = list(filter(lambda s: s.endswith(exe),
                                    exe_abs.stdout.decode().lower().splitlines()))
                if execs:
                    if p.isfile(execs[0]):
                        return execs[0]
    else:
        from shutil import which
        exe = which(executable)
        if exe:
            return exe
    raise PandotoolsError(
        f"'{executable}' (without extension) wasn't found in the [{', '.join(search_dirs_)}] and in the $PATH.")


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
