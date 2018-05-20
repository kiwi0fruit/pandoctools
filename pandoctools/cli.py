import sys
import os
from os import path as p
import click
import re
import yaml
from subprocess import run, PIPE
import configparser


def get_output_file(input_file: str, out: str) -> str:
    """Make output file path from input file path and out pattern."""
    out = out.replace('*', p.basename(input_file))
    if not p.isabs(out):
        out = p.normpath(p.join(p.dirname(input_file), out))
    return out


def get_extensions(file_path: str):
    """Get extension and full extension like 'tag.gz'."""
    ext = p.splitext(file_path)[1][1:]
    match = re.search(r'[.](.*)', p.basename(file_path))
    ext_full = match.group(1) if match else ""
    return ext, ext_full


def get_profile_path(profile: str, dir1: str, dir2: str):
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
        return profile


def read_ini(ini: str, dir1: str, dir2: str):
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
    Checks if python root env is "../../"
    ("<...>/root_python/envs/the_env").
    """
    # TODO
    if True
        return ""
    else:
        return None


def user_yes_no_query(message):
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


if os.name == 'nt':
    pandoctools_user_data = r"%APPDATA%\pandoc\pandoctools"
    pandoctools_core = p.join(p.dirname(p.abspath(__file__)), "bat")
else:
    pandoctools_user_data = "$HOME/.pandoc/pandoctools"
    pandoctools_core = p.join(p.dirname(p.abspath(__file__)), "sh")

help_str = """Pandoctools is a Pandoc profile manager that stores CLI filter pipelines.
(default INPUT_FILE is "Untitled").

Profiles are searched in user data: "{}" then in python module: "{}".
Profiles read from stdin and write to stdout (usually).

Some options can be set in document metadata:\n
---\n
pandoctools:\n
  prof: Default\n
  out: *.html\n
  std: False\n
...\n
Note that "std: True" does not work.\n
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
@click.option('-s', '--std', is_flag=True, default=False,
              help="Read document form stdin and write to stdout in a silent mode. " +
                   "INPUT_FILE only gives a file path. If --std was set but stdout = '' " +
                   "then the profile always writes output file to disc with these options.")
@click.option('--debug', is_flag=True, default=False, help="Debug mode.")
def pandoctools(input_file, profile, out, std, debug):
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
    env_path = p.dirname(sys.executable)
    if os.name == 'nt':
        pandoctools_user = p.join(os.environ["APPDATA"], "pandoc", "pandoctools")
        scripts_bin = p.join(env_path, "Scripts")
        os.environ['import'] = r'call "{}\pandoctools-import.bat"'.format(scripts_bin)
        os.environ['source'] = r'call "{}\path-source.bat"'.format(scripts_bin)
        os.environ['r'] = r'call "{}\path-run.bat"'.format(scripts_bin)
        os.environ['set_resolve'] = r'call "{}\pandoctools-resolve.bat"'.format(scripts_bin)
    else:
        pandoctools_user = p.join(os.environ["HOME"], ".pandoc", "pandoctools")
        scripts_bin = p.join(env_path, "bin")
        os.environ['import'] = p.join(scripts_bin, 'pandoctools-import')
        os.environ['source'] = p.join(scripts_bin, 'path-source')
        os.environ['resolve'] = p.join(scripts_bin, 'pandoctools-resolve')

    os.environ['_user_config'] = pandoctools_user
    os.environ['_core_config'] = pandoctools_core
    os.environ['scripts'] = scripts_bin
    os.environ['env_path'] = env_path

    # Read document and mod input_file if needed:
    if (not std) and (input_file is not None):
        with open(input_file, 'r') as file:
            doc = file.read()
    else:
        doc = sys.stdin.read()
    input_file = "untitled" if (input_file is None) else input_file

    if (profile is None) or (out is None) or std:
        # Read metadata:
        m = re.search(r'(?:^|\n)---\n(.+)(?:---|\.\.\.)(?:\n|$)', doc, re.DOTALL)
        metadata = yaml.load(m.group(1)) if m else {}
        pandoctools_meta = metadata.get('pandoctools', None)
        if not isinstance(pandoctools_meta, dict):
            pandoctools_meta = {}
        # Mod options if needed:
        profile = pandoctools_meta.get('profile', 'Default') if (profile is None) else profile
        out = pandoctools_meta.get('out', '*.html') if (out is None) else out
        std = False if (pandoctools_meta.get('std', '').upper() == 'FALSE') else std

    # Set other environment vars:
    output_file = get_output_file(input_file, out)
    os.environ['input_file'] = input_file
    os.environ['output_file'] = output_file
    os.environ['in_ext'], os.environ['in_ext_full'] = get_extensions(input_file)
    os.environ['out_ext'], os.environ['out_ext_full'] = get_extensions(output_file)

    profile_path = get_profile_path(profile, pandoctools_user, pandoctools_core)
    if not std:
        with open(profile_path, 'r') as file:
            print('\nOut: {}\nProfile code:\n'.format(out))
            print(file.read())
        message = ("Type 'y/yes' to continue with:\n    Profile: {}\n    Profile path: {}\n\n" +
                   "Or type 'n/no' to exit. Then press Enter.").format(profile, profile_path)
        if not user_yes_no_query(message):
            return None

    if debug:
        vars_ = ['scripts', 'import', 'source', 'r', 'set_resolve', 'resolve',
                 'env_path', '_core_config', '_user_config', 'input_file', 'output_file',
                 'in_ext', 'in_ext_full', 'out_ext', 'out_ext_full']
        for var in vars_:
            print('{}: {}'.format(var, os.environ.get(var)))

    # https://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python3
    config = read_ini('Defaults', pandoctools_user, pandoctools_core)
    root_env = config.get('Default', 'root_env')
    root_env = root_env if p.isabs(root_env) and p.isdir(root_env) else guess_root_env(env_path)

    print(root_env)
    # TODO: modfy $PATH

    # proc = run(profile_path, stdout=PIPE, input=doc, encoding='utf8')
    # print(proc.stdout)
    # print(proc.stderr)

    if not std:
        input("Press Enter to continue...")
