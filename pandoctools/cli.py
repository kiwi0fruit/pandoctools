import sys
import os
from os.path import join, dirname, abspath
import click
import re
import yaml


def get_output_file(input_file: str, out: str):
    return ""


def get_extensions(file: str):
    return "", ""

if os.name == 'nt':
    pandoctools_user_data = r"%APPDATA%\pandoc\pandoctools"
    pandoctools_core = join(dirname(abspath(__file__)), "bat")
else:
    pandoctools_user_data = "$HOME/.pandoc/pandoctools"
    pandoctools_core = join(dirname(abspath(__file__)), "sh")

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
def pandoctools(input_file, profile, out, std):
    """
    Sets environment variables:
    * scripts, import, source
    * r (win), set_resolve (win), resolve (unix)
    * env_path, _core_config, _user_config
    * input_file, output_file
    * in_ext, in_ext_full
    * out_ext, out_ext_full
    """
    # Set other environment vars:
    env_path = dirname(sys.executable)
    if os.name == 'nt':
        pandoctools_user = join(os.environ["APPDATA"], "pandoc", "pandoctools")
        scripts_bin = join(env_path, "Scripts")
        os.environ['import'] = r'call "{}\pandoctools-import.bat"'.format(scripts_bin)
        os.environ['source'] = r'call "{}\path-source.bat"'.format(scripts_bin)
        os.environ['r'] = r'call "{}\path-run.bat"'.format(scripts_bin)
        os.environ['set_resolve'] = r'call "{}\pandoctools-resolve.bat"'.format(scripts_bin)
    else:
        pandoctools_user = join(os.environ["HOME"], ".pandoc", "pandoctools")
        scripts_bin = join(env_path, "bin")
        os.environ['import'] = join(scripts_bin, 'pandoctools-import')
        os.environ['source'] = join(scripts_bin, 'path-source')
        os.environ['resolve'] = join(scripts_bin, 'pandoctools-resolve')

    os.environ['_user_config'] = pandoctools_user
    os.environ['_core_config'] = pandoctools_core
    os.environ['scripts'] = scripts_bin
    os.environ['env_path'] = env_path

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
        profile = pandoctools_meta.get('profile', 'Default') if (profile is None) else profile
        out = pandoctools_meta.get('out', '*.html') if (out is None) else out
        std = False if (pandoctools_meta.get('std', '').upper() == 'FALSE') else std

    # Set other environment vars:
    output_file = get_output_file(input_file, out)
    os.environ['input_file'] = input_file
    os.environ['output_file'] = output_file
    os.environ['in_ext'], os.environ['in_ext_full'] = get_extensions(input_file)
    os.environ['out_ext'], os.environ['out_ext_full'] = get_extensions(output_file)

    if not std:
        input("Press Enter to continue...")
