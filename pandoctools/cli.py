import sys
import os
from os import path as p
import click
import re
import yaml
from subprocess import run, PIPE
import configparser
import io


def expand_pattern(pattern: str,  target_file: str,  cwd: bool) -> str:
    """
    Make file path from pattern and target file path:
      - If (target = c/d/doc.md) then (* = doc.md) and (<*> = doc)
      - If (target = c/d/doc.md.html) then (* = doc.md.html) and (<*> = doc.md)
    Pattern can be a simple relative path - it would be relative to input file dir
    (or relative to CWD if cwd=True).
      - ./doc2.md     + dir/doc.md      -> dir/doc2.md
      - doc2.md       + dir/doc.md      -> dir/doc2.md
      - doc2.md       + dir/doc.md      -> doc2.md (cwd=True)
      - C:/*.md       + dir/doc.md      -> C:/doc.md.md
      - ./*.md        + dir/doc.md      -> dir/doc.md.md
      - *.md          + dir/doc.md      -> dir/doc.md.md
      - ./out/<*>.pdf + dir/doc.md      -> dir/out/doc.pdf
      - out/*.md      + dir/doc.md      -> dir/out/doc.md.md
      - ../*.md       + dir2/dir/doc.md -> dir2/doc.md.md
      - ../out/*.md   + dir2/dir/doc.md -> dir2/out/doc.md.md
      - ../doc2.md    + dir2/dir/doc.md -> dir2/doc2.md
      - ../*.md       + dir2/dir/doc.md -> ../doc.md.md (cwd=True)
    """
    target_name = p.basename(target_file)
    file_path = pattern.replace('<*>', p.splitext(target_name)[0]).replace('*', target_name)
    if not p.isabs(file_path) and not cwd:
        file_path = p.normpath(p.join(p.dirname(target_file), file_path))
    return file_path


def get_extensions(file_path: str):
    """Get extension and full extension like 'tag.gz'."""
    ext = p.splitext(file_path)[1][1:]
    match = re.search(r'[.]([.0-9a-zA-Z]*)$', p.basename(file_path))
    ext_full = match.group(1) if match else ""
    return ext, ext_full


def get_profile_path(profile: str,
                     dir1: str,
                     dir2: str,
                     input_file: str,
                     cwd: bool) -> str:
    """
    Find profile path by profile name/profile path.
    In profile name is given (not profile path) then search in folder1, then in folder2.
    """
    if p.splitext(p.basename(profile))[0] == profile:
        ext = 'bat' if (os.name == 'nt') else 'sh'
        profile1 = p.join(dir1, 'Profile-{}.{}'.format(profile, ext))
        profile2 = p.join(dir2, 'Profile-{}.{}'.format(profile, ext))
        if p.isfile(profile1):
            return profile1
        elif p.isfile(profile2):
            return profile2
        else:
            raise ValueError("Profile '{}' was not found.".format(profile))
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

    config = configparser.ConfigParser()
    config.read(ini_path)
    return config


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


def user_file_query():
    import pyperclip
    yes = {'yes', 'y'}
    no = {'no', 'n'}

    def message(filepath):
        print("Type 'y/yes' to use clipboard paste as input file:")
        try:
            print(filepath)
        except UnicodeEncodeError:
            print(filepath.encode('utf-8'))
        print("Type 'n/no' to exit and ENTER to reload clipboard paste.")
        return filepath

    file_path = message(pyperclip.paste())
    while True:
        answer = input().lower()
        if answer in yes:
            return file_path
        elif answer in no:
            return None
        else:
            file_path = message(pyperclip.paste())


env_path = p.dirname(sys.executable)
if os.name == 'nt':
    pandoctools_user_data = r"%APPDATA%\pandoc\pandoctools"
    pandoctools_user = p.join(os.environ["APPDATA"], "pandoc", "pandoctools")
    pandoctools_core = p.join(p.dirname(p.abspath(__file__)), "bat")
    scripts_bin = p.join(env_path, "Scripts")
    pandoctools_bin = p.join(scripts_bin, "pandoctools.exe")
else:
    pandoctools_user_data = "$HOME/.pandoc/pandoctools"
    pandoctools_user = p.join(os.environ["HOME"], ".pandoc", "pandoctools")
    pandoctools_core = p.join(p.dirname(p.abspath(__file__)), "sh")
    scripts_bin = p.join(env_path, "bin")
    pandoctools_bin = p.join(scripts_bin, "pandoctools")


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
@click.option('--std', is_flag=True, default=False,
              help="Read document form stdin and write to stdout in a silent mode. " +
                   "INPUT_FILE only gives a file path. If --std was set but stdout = '' " +
                   "then the profile always writes output file to disc with these options.")
@click.option('--debug', is_flag=True, default=False, help="Debug mode.")
@click.option('--cwd', is_flag=True, default=False,
              help="Use real CWD in profile and out options (instead of input file dir).")
def pandoctools(input_file, profile, out, std, debug, cwd):
    """
    Sets environment variables:
    * scripts, import, source
    * r (win), set_resolve (win), resolve (unix)
    * env_path, _core_config, _user_config
    * input_file, output_file
    * in_ext, in_ext_full
    * out_ext, out_ext_full
    """
    # Set environment vars:
    if os.name == 'nt':
        os.environ['import'] = r'call "{}\pandoctools-import.bat"'.format(scripts_bin)
        os.environ['source'] = r'call "{}\path-source.bat"'.format(scripts_bin)
        os.environ['pyprepPATH'] = r'call "{}\path-pyprep.bat"'.format(scripts_bin)
        os.environ['r'] = r'call "{}\path-run.bat"'.format(scripts_bin)
        os.environ['set_resolve'] = r'call "{}\pandoctools-resolve.bat"'.format(scripts_bin)
        os.environ['resolve'] = ""
        os.environ['setUTF8'] = 'chcp 65001 > NUL'
        os.environ['PYTHONIOENCODING'] = 'utf-8'
    else:
        os.environ['import'] = p.join(scripts_bin, 'pandoctools-import')
        os.environ['source'] = p.join(scripts_bin, 'path-source')
        os.environ['pyprepPATH'] = p.join(scripts_bin, 'path-pyprep')
        os.environ['r'] = ""
        os.environ['set_resolve'] = ""
        os.environ['resolve'] = p.join(scripts_bin, 'pandoctools-resolve')
        os.environ['setUTF8'] = ""

    os.environ['_user_config'] = pandoctools_user
    os.environ['_core_config'] = pandoctools_core
    os.environ['scripts'] = scripts_bin
    os.environ['env_path'] = env_path

    # Read document and mod input_file if needed:
    if std:
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        doc = input_stream.read()  # doc = sys.stdin.read()
    else:
        if input_file is None:
            print('Input file was not provided.')
            input_file = user_file_query()
            if input_file is None:
                return None
        with open(input_file, 'r', encoding="utf-8") as file:
            doc = file.read()
    input_file = "untitled" if (input_file is None) else input_file

    if (profile is None) or (out is None):
        # Read metadata:
        m = re.search(r'(?:^|\n)---\n(.+)(?:---|\.\.\.)(?:\n|$)', doc, re.DOTALL)
        metadata = yaml.load(m.group(1)) if m else {}
        pandoctools_meta = metadata.get('pandoctools', None)
        if not isinstance(pandoctools_meta, dict):
            pandoctools_meta = {}
        # Mod options if needed:
        profile = pandoctools_meta.get('profile', 'Default') if (profile is None) else profile
        out = pandoctools_meta.get('out', '*.html') if (out is None) else out

    # Set other environment vars:
    output_file = expand_pattern(out, input_file, cwd)
    os.environ['input_file'] = input_file
    os.environ['output_file'] = output_file
    os.environ['in_ext'], os.environ['in_ext_full'] = get_extensions(input_file)
    os.environ['out_ext'], os.environ['out_ext_full'] = get_extensions(output_file)

    profile_path = get_profile_path(profile, pandoctools_user, pandoctools_core, input_file, cwd)

    # Run profile confirmation:
    if not std:
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

    # Find python root env:
    #   https://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python3
    config = read_ini('Defaults', pandoctools_user, pandoctools_core)
    root_env = config.get('Default', 'root_env')
    os.environ["root_env"] = root_env if p.isabs(root_env) and p.isdir(root_env) else guess_root_env(env_path)

    if debug:
        vars_ = ['scripts', 'import', 'source', 'pyprepPATH', 'r', 'set_resolve', 'resolve',
                 'env_path', '_core_config', '_user_config', 'input_file', 'output_file',
                 'root_env', 'in_ext', 'in_ext_full', 'out_ext', 'out_ext_full', 'PYTHONIOENCODING']
        for var in vars_:
            print('{}: {}'.format(var, os.environ.get(var)))
        print(os.environ["PATH"])

    proc = run(profile_path, stdout=PIPE, input=doc, encoding='utf8')

    if proc.stderr is not None:
        error_stream = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        error_stream.write(proc.stderr)  # sys.stderr.write(proc.stderr)
    if not std:
        if (proc.stdout is not None) and (proc.stdout != ""):
            print(proc.stdout, file=open(output_file, 'w', encoding="utf-8"))
            print('Pandoctools wrote profile\'s stdout to:')
        else:
            print('Profile\'s stdout is empty. Presumably profile wrote to:')
        try:
            print('    ' + output_file)
        except UnicodeEncodeError:
            print(('    ' + output_file).encode('utf-8'))
        input("Press Enter to continue...")
    else:
        output_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        output_stream.write(proc.stdout)  # sys.stdout.write(proc.stdout)
