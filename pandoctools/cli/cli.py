import sys
import os
from os import path as p
import click
import yaml
from subprocess import run, PIPE
import configparser
import io
from typing import Tuple
from ..pandoc_filter_arg import pandoc_filter_arg, is_bin_ext_maybe
from ..shared_vars import (pandoctools_user, pandoctools_user_data, bash_cygpath,
                           pandoctools_core, env_path, search_dirs)
from knitty.tools import get, load_yaml


PROFILE = 'Default'
OUT = '*.*.md'


def expandvars(file_path):
    return p.expanduser(p.expandvars(file_path))


def expand_pattern(pattern: str,  target_file: str,  cwd: bool) -> str:
    """
    Make file path from pattern and target file path:
      - If (target = c/d/doc.md) then (* = doc.md) and (<*> = doc)
      - If (target = c/d/doc.md.html) then (* = doc.md.html) and (<*> = doc.md)
    Pattern can be a simple relative path - it would be relative to input file dir
    (or relative to CWD if cwd=True).
      - ./doc2.md      + dir/doc.md      -> dir/doc2.md
      - doc2.md        + dir/doc.md      -> dir/doc2.md
      - doc2.md        + dir/doc.md      -> doc2.md (cwd=True)
      - C:/*.*.md      + dir/doc.md      -> C:/doc.md.md
      - ./*.pdf        + dir/doc.md      -> dir/doc.pdf
      - *.*.md         + dir/doc.md      -> dir/doc.md.md
      - ./out/*.pdf    + dir/doc.md      -> dir/out/doc.pdf
      - out/*.*.md     + dir/doc.md      -> dir/out/doc.md.md
      - ../*.*.md      + dir2/dir/doc.md -> dir2/doc.md.md
      - ../out/*.md.md + dir2/dir/doc.md -> dir2/out/doc.md.md
      - ../doc2.md     + dir2/dir/doc.md -> dir2/doc2.md
      - ../*.*.md      + dir2/dir/doc.md -> ../doc.md.md (cwd=True)
    """
    target_name = p.basename(target_file)
    file_path = pattern.replace('*.*', target_name).replace('*', p.splitext(target_name)[0])
    if not p.isabs(file_path) and not cwd:
        file_path = p.normpath(p.join(p.dirname(target_file), file_path))
    return p.abspath(file_path)


def get_ext_and_from(file_path: str, read: str = None):
    """
    Returns extension and pandoc reader format like ('md', 'markdown', 'true')
    """
    ext = p.splitext(file_path)[1][1:]
    important_from = 'true' if read else 'false'
    read = read.lower() if read else {'md': 'markdown', '': 'markdown'}.get(ext.lower(), ext.lower())
    return ext, read, important_from


def get_ext_and_to(file_path: str, to: str = None):
    """
    Returns extension and pandoc writer format like ('html', 'html5', 'true')
    """
    ext = p.splitext(file_path)[1][1:]
    important_to = 'true' if to else 'false'
    to = to.lower() if to else pandoc_filter_arg(output=f'file.{ext}' if ext else 'file',
                                                 search_dirs=search_dirs)
    return ext, to, important_to


def get_profile_path(profile: str,
                     user_dir: str,
                     core_dir: str,
                     input_file: str,
                     cwd: bool) -> Tuple[str, bool]:
    """
    Find profile path by profile name/profile path.
    In profile name is given (not profile path) then search in user_dir, then in core_dir.

    returns tuple(profile_path, safe_location)
    """
    if p.splitext(p.basename(profile))[0] == profile:
        for dir_ in (user_dir, core_dir):
            profile_path = p.join(dir_, profile)
            if p.isfile(profile_path):
                return profile_path, True
        else:
            raise ValueError(f"Profile '{profile}' was not found in\n{user_dir}\nand\n{core_dir}")

    profile_path = expand_pattern(profile, input_file, cwd)
    if not p.isfile(profile_path):
        raise ValueError(f"Profile '{profile}' was not found in\n{profile_path}")

    return profile_path, False


def read_ini(ini: str,  dir1: str,  dir2: str):
    """
    Read ini file by ini name/ini path.
    If ini name is given (not ini path) then search in dir1, then in dir2.
    """
    if p.splitext(p.basename(ini))[0] == ini:
        for dir_ in (dir1, dir2):
            ini_path = p.join(dir_, f'{ini}.ini')
            if p.isfile(ini_path):
                break
        else:
            raise ValueError(f"INI '{ini}' was not found.")
    else:
        ini_path = ini

    _config = configparser.ConfigParser(interpolation=None)
    _config.read(ini_path)
    return _config


# noinspection PyShadowingNames
def guess_root_env(env_path_: str):
    """
    Checks if python root env in default location:
    env_path_ =? "<...>/root_python/envs/env_name"
    """
    up1 = p.dirname(env_path_)
    up2 = p.dirname(up1)
    python_bin = p.join(up2, 'python.exe' if (os.name == 'nt') else 'bin/python')
    if (p.basename(up1) == 'envs') and p.isfile(python_bin):
        return up2
    else:
        return ""


def user_yes_no_query(message: str):
    yes = {'yes', 'y'}
    no = {'no', 'n'}
    print(message)
    while True:
        answer = input().lower()
        if answer in yes:
            return True
        elif answer in no:
            return False
        else:
            print("Please respond with one of: 'y', 'yes', 'n', 'no'.")


# Set some vars and env vars. Read from INI config:
config = read_ini('Defaults', pandoctools_user, pandoctools_core)
if os.name == 'nt':
    scripts_bin = 'Scripts'
    pandoctools_bin = p.join(env_path, r'Scripts\pandoctools.exe')
    bash, cygpath = bash_cygpath(expandvars(config.get('Default', 'win_bash', fallback='')))
else:
    scripts_bin = 'bin'
    pandoctools_bin = p.join(env_path, 'bin', 'pandoctools')
    bash, cygpath = bash_cygpath()

# Find python root env:
root_env = config.get('Default', 'root_env', fallback='')
#   Expand environment vars and get abs path:
root_env = expandvars(root_env)
root_env = root_env if p.isabs(root_env) and p.isdir(root_env) else guess_root_env(env_path)


@click.command(help=f"""
Pandoctools is a Pandoc profile manager that stores CLI filter pipelines.
(default INPUT_FILE is "untitled").

Recommended ways to run Pandoctools are to:\n
- add it to 'Open With' applications for desired file format,\n
- drag and drop file over pandoctools shortcut,\n
- run it from console

Profiles are searched in user data: "{pandoctools_user_data}" then in python module: "{pandoctools_core}".
When profile is given by path then Pandoctools asks for confirmation
(in stdin mode prints confirmation to stdout and exits).
Profiles read from stdin and write to stdout (usually).

Some options can be set in document metadata (all are optional):\n
---\n
pandoctools:\n
  prof: Default\n
  out: *.html\n
  from: markdown\n
  to: html\n
...\n
May be (?) for security concerns the user data folder should be set to write-allowed only as administrator.
""")
@click.argument('input_file', type=str, default=None, required=False)
@click.option('-i', '--in', 'input_file_stdin', type=str, default=None,
              help="Input file path for when INPUT_FILE argument wasn't provided and we read from stdin " +
                   '(INPUT_FILE has a priority).')
@click.option('-p', '--profile', type=str, default=None,
              help='Pandoctools profile name or file path (default is in INI: "Default").')
@click.option('-o', '--out', type=str, default=None,
              help='Output file path like "./out/doc.html" ' +
                   'or input file path transformation like "./out/*.ipynb" (default is in INI: "*.*.md"). ' +
                   '`-o "-"` switches output to stdout but doesn\'t override `out: x` in metadata.')
@click.option('-s', '--stdout', type=str, default=None,
              help="Same as --out but write document to stdout (has a priority over --out). " +
                   '`-s "-"` switches output to stdout but doesn\'t override `out: x` in metadata. ' +
                   "If switched to stdout but stdout output was empty then the profile (not Pandoctools itself) " +
                   "always writes output file to disc and doesn't write " + 
                   "to stdout with the particular options.")
@click.option('-f', '-r', '--from', '--read', 'read', type=str, default=None,
              help="Pandoc reader option (can be extended with custom formats handled in profiles).")
@click.option('-t', '-w', '--to', '--write', 'to', type=str, default=None,
              help="Pandoc writer option (can be extended with custom formats handled in profiles).")
@click.option('--yes', is_flag=True, default=False,
              help="Run without confirmation of the profile if it was going to happen.")
@click.option('--cwd', is_flag=True, default=False,
              help="Use real CWD everywhere (instead of input file directory as default).")
@click.option('--detailed-out', is_flag=True, default=False,
              help="With this option when in stdout mode pandoctools stdout consist of yaml " +
              "metadata section ---... with 'outpath' and 'output' keys that is followed by profile stdout " +
              "(when not in stdout mode or profile stdout output was empty then key 'output: None').")
@click.option('--debug', is_flag=True, default=False, help="Debug mode.")
def pandoctools(input_file, input_file_stdin, profile, out, read, to, stdout, yes, cwd, detailed_out, debug):
    """
    Sets environment variables:
      * scripts, source, resolve
      * env_path, root_env, cygpath
      * input_file, output_file, from, to
      * important_from, important_to
      * in_ext, out_ext, is_bin_ext_maybe
      * Windows only: PYTHONIOENCODING, LANG
    """
    # Read document and mod input_file if needed:
    if input_file:
        stdin = False
        with open(expandvars(input_file), 'r', encoding="utf-8") as file:
            doc = file.read()
    else:
        stdin = True
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        doc = input_stream.read()  # sys.stdin.read()

        if input_file_stdin:
            input_file = input_file_stdin
        else:
            input_file = 'untitled'

    if stdout == '-':
        stdout = True
        out = None
    elif stdout:
        stdout = True
        out = stdout
    elif out == '-':
        stdout = True
        out = None
    else:
        stdout = False

    # now both stdin and stdout are bools

    # #
    if not (profile and out and read and to):
        # Read metadata:
        pandoctools_meta = get(load_yaml(doc)[1], 'pandoctools')
        if not isinstance(pandoctools_meta, dict):
            pandoctools_meta = {}
        # Mod options if needed:
        profile = profile if profile else pandoctools_meta.get('profile')
        out = out if out else pandoctools_meta.get('out')
        read = read if read else pandoctools_meta.get('from')
        to = to if to else pandoctools_meta.get('to')

    # Read from INI config (Read profile, 'out'):
    profile = profile if profile else config.get('Default', 'profile', fallback=PROFILE)
    out = out if out else config.get('Default', 'out', fallback=OUT)
    profile = profile if profile else PROFILE
    out = out if out else OUT

    # Expand environment vars and get abs path:
    input_file = p.abspath(expandvars(input_file))
    profile = expandvars(profile)
    out = expandvars(out)

    # Expand custom patterns:
    output_file = expand_pattern(out, input_file, cwd)
    profile_path, safe_location = get_profile_path(profile, pandoctools_user, pandoctools_core, input_file, cwd)

    # Run profile confirmation:
    if not (yes or safe_location):
        with open(profile_path, 'r') as file:
            print('Profile code:\n' +
                  '--------------------------\n' +
                  file.read().strip())
        print("--------------------------\n" +
              f"Profile: {profile} | Path: {profile_path}\n" +
              f"Out: {out} | Path: {output_file}\n" +
              "--------------------------")

        if not stdin:
            if not user_yes_no_query(
                "Type y/yes to continue with the profile or type n/no to exit. Then press Enter.\n"
            ):
                return
        else:
            print('Run pandoctools with the same parameters and --yes option to confirm the profile.')
            return

    # Set environment vars to dict:
    dic = dict()
    dic['in_ext'], dic['from'], dic['important_from'] = get_ext_and_from(input_file, read)
    dic['out_ext'], dic['to'], dic['important_to'] = get_ext_and_to(output_file, to)
    if os.name == 'nt':
        dic['PYTHONIOENCODING'] = 'utf-8'
        dic['LANG'] = 'C.UTF-8'
    env_vars = dict(
        source=p.join(p.dirname(pandoctools_core), 'source-from-path'),
        resolve=p.join(env_path, scripts_bin, 'pandoctools-resolve'),
        scripts=scripts_bin,
        env_path=env_path,
        input_file=input_file,
        output_file=output_file,
        is_bin_ext_maybe=str(is_bin_ext_maybe(output_file, to, search_dirs=search_dirs)).lower(),
        root_env=root_env,
        cygpath=cygpath,
        **dic
    )

    # convert win-paths to unix-paths if needed:
    if os.name == 'nt':
        vars_ = [var for var in ("source", "scripts", "resolve", "env_path",
                                 "input_file", "output_file", "root_env")
                 if env_vars.get(var)]
        posix_paths = run([cygpath] + [env_vars[var] for var in vars_],
                          stdout=PIPE, input=doc, encoding='utf-8').stdout.strip().splitlines()
        for var, pth in zip(vars_, posix_paths):
            env_vars[var] = pth

    # debug env vars:
    if debug:
        vars_ = ['scripts', 'source', 'resolve', 'env_path', 'cygpath',
                 'input_file', 'output_file', 'root_env', 'in_ext', 'from', 'out_ext',
                 'to', 'is_bin_ext_maybe', 'important_from', 'important_to',
                 'PYTHONIOENCODING', 'LANG']
        for var in vars_:
            print(f'{var}: {env_vars.get(var)}')
        print('bash: ', bash, '\n')
        print(os.environ["PATH"], '\n')
        print(dict(os.environ))

    # run pandoctools:
    bash_cwd = None if cwd else p.dirname(input_file)
    proc = run([bash, profile_path], stdout=PIPE, input=doc,
               encoding='utf-8', cwd=bash_cwd,
               env={**dict(os.environ), **env_vars})

    # forward output:
    prof_stdout = proc.stdout if proc.stdout else ''
    if detailed_out:
        with io.StringIO() as f:
            dic = {'outpath': output_file}
            if not (stdout and prof_stdout):
                dic['output'] = 'None'
            yaml.dump(dic, f, default_flow_style=False)
            meta = '---\n' + f.getvalue() + '...\n'
    else:
        meta = ''

    if not stdout:
        if prof_stdout:
            print(prof_stdout, end='', file=open(output_file, 'w', encoding='utf-8'))

        if not (stdin or yes):
            def safe_print(s):
                try:
                    print(s)
                except UnicodeEncodeError:
                    print(str(s).encode('utf-8'))

            if prof_stdout:
                safe_print("Pandoctools wrote profile's stdout to:\n    " + output_file)
            else:
                safe_print("Profile's stdout is empty. Presumably profile wrote to:\n    " + output_file)
            input('Press Enter to continue...')
    else:
        output_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        output_stream.write(meta + prof_stdout)  # sys.stdout.write()
