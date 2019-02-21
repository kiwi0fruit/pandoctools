import os
import os.path as p
import sys
from typing import Tuple, Iterable
from knitty.tools import where, KnittyError
from subprocess import run, PIPE


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
        bash = where('bash', search_dirs, exe_only=False)
    except KnittyError:
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

    ret = run([bash, '-c', 'cygpath -w $(which cygpath)'], stderr=PIPE, stdout=PIPE)
    cygpath = None
    if ret.stdout and not ret.stderr:
        cygpath = ret.stdout.decode().strip().splitlines()[0]
        if not p.isfile(cygpath):
            cygpath = None
    if not cygpath:
        bash_dir = p.dirname(bash)
        cygpath = where('cygpath', [bash_dir, rf'{p.dirname(bash_dir)}\usr\bin',
                        rf'{bash_dir}\usr\bin'])
    return bash, cygpath


def is_bin_ext_maybe(output: str, to: str=None, search_dirs: Iterable[str]=None,
                     force_pandoc: bool=False) -> bool:
    """
    Nice guess if the ``output`` extension (or ``to`` if no ext) means
    that Pandoc needs adding ``-o "${output_file}"`` option.

    :param output: Pandoc writer option
    :param to: Pandoc writer option.
        Used only if output doesn't have an extension
    :param search_dirs: extra dirs to look for executables
    :param force_pandoc: ignore hardcoded logic and always "ask" Pandoc.
        Useful for testing hardcoded logic.
    """
    ext = p.splitext(p.basename(output))[1][1:]
    if not ext:
        ext = to

    if not ext:
        return False
    elif ext in ('pdf', 'docx', 'epub', 'odt') and (not force_pandoc):  # TODO add more
        return True
    else:
        import re
        from knitty.pandoc_filter_arg import doc

        pandoc, panfl = where('pandoc', search_dirs), where('panfl', search_dirs)
        err = run([pandoc, '-f', 'markdown', '--filter', panfl, '-t', ext],
                  stderr=PIPE, stdout=PIPE, input=doc.encode()).stderr
        err = err.decode() if err else ''
        if re.search(r"(Cannot write \w+ output to terminal|specify an output file)", err):
            return True
        else:
            return False
