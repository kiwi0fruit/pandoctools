import sys
import os
from os import path as p
import click
import re
import yaml
import subprocess
from subprocess import PIPE
import configparser
import io
from ..pandoc_filter_arg import pandoc_filter_arg, is_bin_ext_maybe
from ..shared_vars import pandoctools_user, pandoctools_user_data, pandoctools_core


PROFILE = 'Default'
OUT = '*.html'


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


def get_ext_and_from(file_path: str, read: str=None):
    """
    Returns extension and pandoc reader format like ('md', 'markdown', 'true')
    """
    ext = p.splitext(file_path)[1][1:]
    important_from = 'true' if read else 'false'
    read = read.lower() if read else {'md': 'markdown', '': 'markdown'}.get(ext.lower(), ext.lower())
    return ext, read, important_from


def get_ext_and_to(file_path: str, to: str=None):
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
                     cwd: bool) -> str:
    """
    Find profile path by profile name/profile path.
    In profile name is given (not profile path) then search in folder1, then in folder2.
    """
    if p.splitext(p.basename(profile))[0] == profile:
        for dir_ in (user_dir, core_dir):
            profile_path = p.join(dir_, profile)
            if p.isfile(profile_path):
                return profile_path
        else:
            raise ValueError(f"Profile '{profile}' was not found in\n{user_dir}\nand\n{core_dir}")
    else:
        return expand_pattern(profile, input_file, cwd)


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
def guess_root_env(env_path: str):
    """
    Checks if python root env in default location:
    env_path =? "<...>/root_python/envs/env_name"
    """
    up1 = p.dirname(env_path)
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
            print("Please respond with 'y' or 'n'.")


# Set some vars and env vars:
if os.name == 'nt':
    env_path = p.dirname(sys.executable)
    scripts_bin = p.join(env_path, "Scripts")
    pandoctools_bin = p.join(scripts_bin, "pandoctools.exe")
    search_dirs = [env_path, scripts_bin, p.join(env_path, 'Library', 'bin')]
else:
    scripts_bin = p.dirname(sys.executable)
    env_path = p.dirname(scripts_bin)
    pandoctools_bin = p.join(scripts_bin, "pandoctools")
    search_dirs = [env_path, scripts_bin]
    win_bash = None

# Read from INI config:
config = read_ini('Defaults', pandoctools_user, pandoctools_core)
if os.name == 'nt':
    # Find bash on Windows:
    win_bash = expandvars(config.get('Default', 'win_bash', fallback=''))
    if not p.isfile(win_bash):
        # here we implicitly use the fact that ini from core sh folder
        # (pandoctools_core) has path to git's bash
        win_bash = None

# Find python root env:
root_env = config.get('Default', 'root_env', fallback='')
#   Expand environment vars and get abs path:
root_env = expandvars(root_env)
root_env = root_env if p.isabs(root_env) and p.isdir(root_env) else guess_root_env(env_path)


help_str = f"""Pandoctools is a Pandoc profile manager that stores CLI filter pipelines.
(default INPUT_FILE is "Untitled").

Profiles are searched in user data: "{pandoctools_user_data}" then in python module: "{pandoctools_core}".
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
"""


@click.command(help=help_str)
@click.argument('input_file', type=str, default=None, required=False)
@click.option('-p', '--profile', type=str, default=None,
              help='Pandoctools profile name or file path (default is "Default").')
@click.option('-o', '--out', type=str, default=None,
              help='Output file path like "./out/doc.html" ' +
                   'or input file path transformation like "*.html", "./out/*.ipynb" (default is "*.html").\n' +
                   'In --stdio mode only extension is considered: "doc.ipynb" > ".ipynb".')
@click.option('-f', '-r', '--from', '--read', 'read', type=str, default=None,
              help="Pandoc reader option (extended with custom formats).")
@click.option('-t', '-w', '--to', '--write', 'to', type=str, default=None,
              help="Pandoc writer option (extended with custom formats).")
@click.option('--stdio', is_flag=True, default=False,
              help="Read document form stdin and write to stdout in a silent mode. " +
                   "INPUT_FILE only gives a file path. If --stdio was set but stdout output was empty " +
                   "then the profile (not Pandoctools itself) always writes output file to disc and doesn't write " + 
                   "to stdout with these options.")
@click.option('--stdin', is_flag=True, default=False,
              help="Same as --stdio but always writes output file to disc (suppresses --stdio).")
@click.option('--cwd', is_flag=True, default=False,
              help="Use real CWD everywhere (instead of input file directory as default).")
@click.option('--detailed-out', is_flag=True, default=False,
              help="With this option when in --stdio and --stdin modes pandoctools stdout consist of yaml " +
              "metadata section ---... with 'outpath' and 'output' keys that is followed by profile stdout " +
              "(when --stdin or profile stdout output was empty then key 'output: None').")
@click.option('--debug', is_flag=True, default=False, help="Debug mode.")
def pandoctools(input_file, profile, out, read, to, stdio, stdin, cwd, detailed_out, debug):
    """
    Sets environment variables:
    * scripts, import, source
    * r (win), set_resolve (win), resolve (unix)
    * env_path, _core_config, _user_config
    * input_file, output_file
    * in_ext, in_ext_full
    * out_ext, out_ext_full
    """
    # Read document and mod input_file if needed:
    if stdio or stdin:
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        doc = input_stream.read()  # doc = sys.stdin.read()
    else:
        if not input_file:
            print("Input file was not provided.\n" + 
                  "Recommended ways to run Pandoctools are to:\n" +
                  "- add it to 'Open With' applications for desired file format,\n" +
                  "- drag and drop file over pandoctools shortcut,\n" +
                  "- run it from console, see: pandoctools --help\n" +
                  ("\nERROR: Bash was not found by the path provided in INI file.\n"
                   if (win_bash is None) and (os.name == 'nt')
                   else ""))
            input("Press Enter to exit.")
            return None
        with open(expandvars(input_file), 'r', encoding="utf-8") as file:
            doc = file.read()
    input_file = input_file if input_file else "untitled"

    if not (profile and out and read and to):
        # Read metadata:
        m = re.search(r'(?:^|\n)---\n(.+?\n)(?:---|\.\.\.)(?:\n|$)', doc, re.DOTALL)
        metadata = yaml.load(m.group(1)) if m else None
        pandoctools_meta = metadata.get('pandoctools', None) if isinstance(metadata, dict) else None
        if not isinstance(pandoctools_meta, dict):
            pandoctools_meta = {}
        # Mod options if needed:
        profile = profile if profile else pandoctools_meta.get('profile')
        out = out if out else pandoctools_meta.get('out')
        read = read if read else pandoctools_meta.get('from')
        to = to if to else pandoctools_meta.get('to')

    # #
    if (win_bash is None) and (os.name == 'nt'):
        raise ValueError('Bash was not found by the path provided in INI file.')

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
    profile_path = get_profile_path(profile, pandoctools_user, pandoctools_core, input_file, cwd)

    # Run profile confirmation:
    if not stdio and not stdin:
        with open(profile_path, 'r') as file:
            print(f'Profile code:\n\n{file.read().strip()}\n')
        message = ("Type y/yes to continue with the profile or type n/no to exit. Then press Enter.\n"
                   f"    Profile: {profile} | Path: {profile_path}\n"
                   f"    Out: {out} | Path: {output_file}\n")
        if not user_yes_no_query(message):
            return None

    # Set environment vars to dict:
    env_vars = {}
    if os.name == 'nt':
        env_vars['PYTHONIOENCODING'] = 'utf-8'
        env_vars['LANG'] = 'C.UTF-8'

    env_vars['source'] = p.join(scripts_bin, 'pandoctools-source')
    env_vars['python_to_PATH'] = p.join(scripts_bin, 'pandoctools-python-to-path')
    env_vars['resolve'] = p.join(scripts_bin, 'pandoctools-resolve')
    env_vars['scripts'] = scripts_bin
    env_vars['env_path'] = env_path
    env_vars['input_file'] = input_file
    env_vars['output_file'] = output_file
    env_vars['in_ext'], env_vars['from'], env_vars['important_from'] = get_ext_and_from(input_file, read)
    env_vars['out_ext'], env_vars['to'], env_vars['important_to'] = get_ext_and_to(output_file, to)
    env_vars['is_bin_ext_maybe'] = str(is_bin_ext_maybe(output_file, to, search_dirs=search_dirs)).lower()
    env_vars['root_env'] = root_env

    # convert win-paths to unix-paths if needed:
    if os.name == 'nt':
        vars_ = ["source", "scripts", "resolve", "python_to_PATH",
                 "env_path", "input_file", "output_file", "root_env"]
        vars_ = [var for var in vars_ if env_vars[var] != '']
        args = [win_bash, p.join(scripts_bin, 'pandoctools-cygpath')] + [env_vars[var] for var in vars_]

        cygpath = subprocess.run(args, stdout=PIPE, input=doc, encoding='utf-8')
        cygpaths = re.split(r'\r?\n', cygpath.stdout.strip())
        for i, var in enumerate(vars_):
            env_vars[var] = cygpaths[i]

        if cygpath.stderr is not None:
            # error_stream = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
            # error_stream.write(cygpath.stderr)
            print(cygpath.stderr, file=sys.stderr)

    # debug env vars:
    if debug:
        vars_ = ['scripts', 'source', 'python_to_PATH', 'resolve', 'env_path',
                 'input_file', 'output_file', 'root_env', 'in_ext', 'from', 'out_ext',
                 'to', 'is_bin_ext_maybe', 'important_from', 'important_to',
                 'PYTHONIOENCODING', 'LANG']
        for var in vars_:
            print(f'{var}: {env_vars.get(var)}')
        print('win_bash: ', win_bash, '\n')
        print(os.environ["PATH"], '\n')
        print(dict(os.environ))

    # run pandoctools:
    bash = win_bash if (os.name == 'nt') else 'bash'
    bash_cwd = None if cwd else p.dirname(input_file)
    proc = subprocess.run([bash, profile_path], stdout=PIPE, input=doc,
                          encoding='utf-8', cwd=bash_cwd,
                          env={**dict(os.environ), **env_vars})

    if proc.stderr is not None:
        # error_stream = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        # error_stream.write(proc.stderr)
        print(proc.stderr, file=sys.stderr)

    # forward output:
    stdout = proc.stdout if (proc.stdout is not None) else ''
    if detailed_out:
        with io.StringIO() as f:
            dic = {'outpath': output_file}
            if stdin or (stdout == ''):
                dic['output'] = 'None'
            yaml.dump(dic, f, default_flow_style=False)
            meta = '---\n' + f.getvalue() + '...\n'
    else:
        meta = ''

    output_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if not stdio or stdin:
        def _print(s):
            if not stdin:
                try:
                    print(s)
                except UnicodeEncodeError:
                    print(str(s).encode('utf-8'))

        if detailed_out:
            output_stream.write(meta)

        if stdout != '':
            print(stdout, end='', file=open(output_file, 'w', encoding='utf-8'))
            _print("Pandoctools wrote profile's stdout to:\n    " + output_file)
        else:
            _print("Profile's stdout is empty. Presumably profile wrote to:\n    " + output_file)
        if not stdin:
            input('Press Enter to continue...')
    else:
        output_stream.write(meta + stdout)  # sys.stdout.write(proc.stdout)
