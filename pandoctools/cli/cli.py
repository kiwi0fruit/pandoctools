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


def get_extensions(file_path: str):
    """Get extension and full extension like 'tag.gz'."""
    ext = p.splitext(file_path)[1][1:]
    match = re.search(r'[.]([.0-9a-zA-Z]*)$', p.basename(file_path))
    ext_full = match.group(1) if match else ""
    return ext, ext_full


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
        ext = p.basename(core_dir)[-3:]
        profile1 = p.join(user_dir, 'Profile-{}.{}'.format(profile, ext))
        profile2 = p.join(core_dir, 'Profile-{}.{}'.format(profile, ext))
        if p.isfile(profile1):
            return profile1
        elif p.isfile(profile2):
            return profile2
        else:
            raise ValueError("Profile '{}' was not found in\n{}\nand\n{}".format(profile, user_dir, core_dir))
    else:
        return expand_pattern(profile, input_file, cwd)


def read_ini(ini: str,  dir1: str,  dir2: str):
    """
    Read ini file by ini name/ini path.
    If ini name is given (not ini path) then search in folder1, then in folder2.
    """
    if p.splitext(p.basename(ini))[0] == ini:
        ini1 = p.join(dir1, '{}.ini'.format(ini))
        ini2 = p.join(dir2, '{}.ini'.format(ini))
        if p.isfile(ini1):
            ini_path = ini1
        elif p.isfile(ini2):
            ini_path = ini2
        else:
            raise ValueError("INI '{}' was not found.".format(ini))
    else:
        ini_path = ini

    config = configparser.ConfigParser(interpolation=None)
    config.read(ini_path)
    return config


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


"""
def user_file_query():
    import pyperclip
    
    yes = {'yes', 'y'}
    no = {'no', 'n'}

    def message(filepath):
        print("Type 'y'/'yes'+Enter to use this clipboard paste as input file:\n" +
              "--------")
        try:
            print(filepath)
        except UnicodeEncodeError:
            print(filepath.encode('utf-8'))
        print("--------\n" +
              "Type 'n'/'no'+Enter to exit.\n" +
              "Type '/'+Enter to type input file manually.\n" +
              "Type Enter to reload clipboard paste.\n\n" +
              "Hint: on Windows Shift+right-click gives new 'Copy as Path' context menu option
                     (pandoctools strips \"\").")
        return filepath

    message2 = "Please type input file path (or type '/'+Enter to exit):"

    file_path = message(pyperclip.paste())
    while True:
        answer = input().lower()
        if answer in yes:
            return file_path.strip('"').strip()
        elif answer in no:
            return None
        elif answer == '/':
            print(message2)
            file_path = input()
            while (file_path is None) or (file_path == ''):
                file_path = input()
                if file_path == '/':
                    return None
                else:
                    return file_path.strip('"').strip()
        else:
            file_path = message(pyperclip.paste())
"""

if os.name == 'nt':
    pandoctools_user_data = r"%APPDATA%\pandoc\pandoctools"
    pandoctools_user = p.join(os.environ["APPDATA"], "pandoc", "pandoctools")
    env_path = p.dirname(sys.executable)
    scripts_bin = p.join(env_path, "Scripts")
    pandoctools_bin = p.join(scripts_bin, "pandoctools.exe")
    _pdt = p.normpath(p.join(p.dirname(p.abspath(__file__)), '..'))
    pandoctools_core = p.join(_pdt, 'bat')
    _pandoctools_core = p.join(_pdt, 'sh')
else:
    pandoctools_user_data = "$HOME/.pandoc/pandoctools"
    pandoctools_user = p.join(os.environ["HOME"], ".pandoc", "pandoctools")
    scripts_bin = p.dirname(sys.executable)
    env_path = p.normpath(p.join(scripts_bin, ".."))
    pandoctools_bin = p.join(scripts_bin, "pandoctools")
    pandoctools_core = p.normpath(p.join(p.dirname(p.abspath(__file__)), '..', 'sh'))
    _pandoctools_core = pandoctools_core


help_str = """Pandoctools is a Pandoc profile manager that stores CLI filter pipelines.
(default INPUT_FILE is "Untitled").

Profiles are searched in user data: "{}" then in python module: "{}".
Profiles read from stdin and write to stdout (usually).

Some options can be set in document metadata:\n
---\n
pandoctools:\n
  prof: Default\n
  out: *.html\n
...\n
May be (?) for security concerns the user data folder should be set to write-allowed only as administrator.
""".format(pandoctools_user_data, pandoctools_core)


@click.command(help=help_str)
@click.argument('input_file', type=str, default=None, required=False)
@click.option('-p', '--profile', type=str, default=None,
              help='Pandoctools profile name or file path (default is "Default").')
@click.option('-o', '--out', type=str, default=None,
              help='Output file path like "./out/doc.html" ' +
                   'or input file path transformation like "*.html", "./out/*.r.ipynb" (default is "*.html").\n' +
                   'In --std mode only full extension is considered: "doc.r.ipynb" > "r.ipynb".')
@click.option('--stdio', is_flag=True, default=False,
              help="Read document form stdin and write to stdout in a silent mode. " +
                   "INPUT_FILE only gives a file path. If --stdio was set but stdout = '' " +
                   "then the profile (not Pandoctools itself) always writes output file to disc with these options.")
@click.option('--stdin', is_flag=True, default=False,
              help="Same as --std but always writes output file to disc (suppresses --stdio).")
@click.option('--cwd', is_flag=True, default=False,
              help="Use real CWD everywhere (instead of input file dir).")
@click.option('--detailed-out', is_flag=True, default=False,
              help="In --stdio and --stdin modes print stdout together with " +
                   "yaml metadata section with 'outpath' and 'output' keys (when --stdin 'output: None').")
@click.option('--debug', is_flag=True, default=False, help="Debug mode.")
def pandoctools(input_file, profile, out, stdio, stdin, cwd, detailed_out, debug):
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
        if input_file is None:
            print("Input file was not provided.\n" + 
                  "Recommended ways to run Pandoctools are to:\n" +
                  "- add it to 'Open With' applications for desired file format,\n" +
                  "- drag and drop file over pandoctools shortcut,\n" +
                  "- run it from console, see: pandoctools --help")
            input("Press Enter to exit.")
            return None
        with open(expandvars(input_file), 'r', encoding="utf-8") as file:
            doc = file.read()
    input_file = "untitled" if (input_file is None) else input_file

    if (profile is None) or (out is None):
        # Read metadata:
        m = re.search(r'(?:^|\n)---\n(.+?\n)(?:---|\.\.\.)(?:\n|$)', doc, re.DOTALL)
        metadata = yaml.load(m.group(1)) if m else None
        pandoctools_meta = metadata.get('pandoctools', None) if isinstance(metadata, dict) else None
        if not isinstance(pandoctools_meta, dict):
            pandoctools_meta = {}
        # Mod options if needed:
        profile = pandoctools_meta.get('profile') if (profile is None) else profile
        out = pandoctools_meta.get('out') if (out is None) else out

    # Read from INI config (Read profile, 'out'. Find python root env, bash on Windows):
    if os.name == 'nt':
        config = read_ini('Defaults', pandoctools_user, _pandoctools_core)
        win_bash = expandvars(config.get('Default', 'win_bash', fallback=''))
        if p.exists(win_bash) and not p.isdir(win_bash) and (str(profile)[-4:] != '.bat'):
            # here we implicitly use the fact that
            # ini from core sh folder (_pandoctools_core)
            # has path to git's bash
            global pandoctools_core
            pandoctools_core = _pandoctools_core
        else:
            win_bash = None
            config = read_ini('Defaults', pandoctools_user, pandoctools_core)
    else:
        win_bash = None
        config = read_ini('Defaults', pandoctools_user, pandoctools_core)

    root_env = config.get('Default', 'root_env', fallback='')
    profile = config.get('Default', 'profile', fallback=PROFILE) if (profile is None) else profile
    out = config.get('Default', 'out', fallback=OUT) if (out is None) else out

    # Expand environment vars and get abs path:
    root_env = expandvars(root_env)
    root_env = root_env if p.isabs(root_env) and p.isdir(root_env) else guess_root_env(env_path)
    input_file = p.abspath(expandvars(input_file))
    profile = expandvars(profile)
    out = expandvars(out)

    # Expand custom patterns:
    output_file = expand_pattern(out, input_file, cwd)
    profile_path = get_profile_path(profile, pandoctools_user, pandoctools_core, input_file, cwd)

    # Run profile confirmation:
    if not stdio and not stdin:
        with open(profile_path, 'r') as file:
            print('\nProfile code:\n\n{}\n'.format(file.read()))
        message = ("Type 'y/yes' to continue with:\n" +
                   "    Profile: {}\n" +
                   "    Profile path: {}\n\n" +
                   "    Out: {}\n" +
                   "    Out path: {}\n\n" +
                   "Or type 'n/no' to exit. Then press Enter.").format(profile, profile_path,
                                                                       out, output_file)
        if not user_yes_no_query(message):
            return None

    # Set environment vars to dict:
    env_vars = {}
    if os.name == 'nt':
        env_vars['PYTHONIOENCODING'] = 'utf-8'
        env_vars['LANG'] = 'C.UTF-8'
    if (os.name == 'nt') and (win_bash is None):
        env_vars['import'] = r'call "{}\pandoctools-import.bat"'.format(scripts_bin)
        env_vars['source'] = r'call "{}\path-source.bat"'.format(scripts_bin)
        env_vars['pyprepPATH'] = r'call "{}\path-pyprep.bat"'.format(scripts_bin)
        env_vars['r'] = r'call "{}\path-run.bat"'.format(scripts_bin)
        env_vars['set_resolve'] = r'call "{}\pandoctools-resolve.bat"'.format(scripts_bin)
        env_vars['resolve'] = ''
        env_vars['setUTF8'] = 'chcp 65001 > NUL && set "PYTHONIOENCODING=utf-8"'
    else:
        env_vars['import'] = p.join(scripts_bin, 'pandoctools-import')
        env_vars['source'] = p.join(scripts_bin, 'path-source')
        env_vars['pyprepPATH'] = p.join(scripts_bin, 'path-pyprep') if (os.name != 'nt') else p.join(scripts_bin,
                                                                                                     'path-pyprep-win')
        env_vars['r'] = ''
        env_vars['set_resolve'] = ''
        env_vars['resolve'] = p.join(scripts_bin, 'pandoctools-resolve')
        env_vars['setUTF8'] = ''

    env_vars['_user_config'] = pandoctools_user
    env_vars['_core_config'] = pandoctools_core
    env_vars['scripts'] = scripts_bin
    env_vars['env_path'] = env_path
    env_vars['input_file'] = input_file
    env_vars['output_file'] = output_file
    env_vars['in_ext'], env_vars['in_ext_full'] = get_extensions(input_file)
    env_vars['out_ext'], env_vars['out_ext_full'] = get_extensions(output_file)
    env_vars['root_env'] = root_env

    # convert win-paths to unix-paths if needed:
    if (os.name == 'nt') and (win_bash is not None):
        vars_ = ["import", "source", "scripts", "resolve", "pyprepPATH",
                 "env_path", "input_file", "output_file", "_core_config",
                 "_user_config", "root_env"]
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
        vars_ = ['scripts', 'import', 'source', 'pyprepPATH', 'r', 'set_resolve', 'resolve',
                 'env_path', '_core_config', '_user_config', 'input_file', 'output_file',
                 'root_env', 'in_ext', 'in_ext_full', 'out_ext', 'out_ext_full', 'PYTHONIOENCODING', 'LANG', 'setUTF8']
        for var in vars_:
            print('{}: {}'.format(var, env_vars.get(var)))
        print('win_bash: ', win_bash, '\n')
        print(os.environ["PATH"], '\n')
        print(dict(os.environ))

    # run pandoctools:
    bash = win_bash if (os.name == 'nt') else 'bash'
    bash_cwd = None if cwd else p.dirname(input_file)
    if (os.name == 'nt') and (win_bash is None):
        for key, val in env_vars.items():
            os.environ[key] = val
        proc = subprocess.run(profile_path, stdout=PIPE, input=doc,
                              encoding='utf-8', cwd=bash_cwd)
    else:
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
