from os import path as p
import os
import sys
from typing import Iterable


class PandotoolsError(Exception):
    pass


def where(executable: str, search_dirs_: Iterable[str]=None) -> str:
    """
    :param executable: exec name without .exe
    :param search_dirs_: extra dirs to look for executables
    :return: On Windows: absolute path to the exec that was found
      in the search_dirs or in the $PATH.
      On Unix: absolute path to the exec that was found in the search_dirs
      or executable arg unchanged.
    """
    from subprocess import run, PIPE

    def exe(_exe): return f'{_exe}.exe' if (os.name == 'nt') else _exe
    def is_exe(_exe): return True if (os.name == 'nt') else os.access(_exe, os.X_OK)

    for _dir in (search_dirs_ if search_dirs_ else ()):
        _exec = p.normpath(p.join(_dir, exe(executable)))
        if p.isfile(_exec):
            if is_exe(_exec):
                return p.abspath(_exec)

    if os.name == 'nt':
        exec_abs = run(
            [p.expandvars(r'%WINDIR%\System32\where.exe'), f'$PATH:{executable}.exe'],
            stdout=PIPE, encoding='utf-8',
        ).stdout.split('\n')[0].strip('\r')

        if p.isfile(exec_abs):
            return exec_abs
        else:
            raise PandotoolsError(f"'{executable}' wasn't found in the [{', '.join(search_dirs_)}] and in the $PATH.")
    else:
        return executable


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

    def bash_cygpath(bash_from_conf: str):
        try:
            bash = where('bash', search_dirs)
        except PandotoolsError:
            pass
        if p.isfile(bash_from_conf):
            bash = bash_from_conf
        else:
            git = p.expandvars(r'%PROGRAMFILES%\Git')
            for bash in (rf'{git}\bin\bash.exe', rf'{git}\usr\bin\bash.exe'):
                if p.isfile(bash):
                    break
            else:
                raise PandotoolsError("bash wasn't found in: python environment, $PATH, " +
                                      r"win_bash path in config, %PROGRAMFILES%\Git")
        bash_dir = p.dirname(bash)
        cygpath = where('cygpath',
                        [bash_dir, rf'{p.dirname(bash_dir)}\usr\bin', rf'{bash_dir}\usr\bin'])
        return bash, cygpath
else:
    pandoctools_user_data = "$HOME/.pandoc/pandoctools"
    pandoctools_user = p.join(os.environ["HOME"], ".pandoc", "pandoctools")
    env_path = p.dirname(p.dirname(sys.executable))
    search_dirs = [p.join(env_path, 'bin')]

    def bash_cygpath(bash_from_conf: str):
        bash = where('bash', search_dirs)
        cygpath = ''
        return bash, cygpath
