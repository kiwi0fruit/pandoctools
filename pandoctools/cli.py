import sys
import os
import click
import re


def cat_md():
    """
    Joins markdown files with "\n\n" separator and writes to stdout.
    If file is 'stdin' then reads it from stdin.
    """
    sources_list, stdin = [], None
    for file in sys.argv[1:]:
        if file == 'stdin':
            if stdin is None:
                stdin = sys.stdin.read()
            sources_list.append(stdin)
        else:
            with open(file, "r", encoding="utf-8") as f:
                sources_list.append(f.read())
    sys.stdout.write('\n\n'.join(sources_list))


@click.argument('profile_script', type=str)
@click.argument('input_file', type=str)
@click.argument('out_ext', type=str, default=None, required=False)
@click.option('-c', '--config', type=str, default=None,
              help="Directory with Pandoctools shell scripts configs that override defaults. " +
              "Recommended to be write allowed only as administrator. Special options: " +
              "`none` (no folder), `pandoc` (`%APPDATA%\\pandoc\\pandoctools` or `$HOME/.pandoc/pandoctools`). " +
              "When not set pandoctools try to read `PANDOCTOOLSDATA` environment variable.")
def pandoctools(profile_script, input_file, out_ext, data_dir):
    config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
    # TODO: set env args: input_file, in_ext, out_ext, config (pandoctools\config), pandoc_data_dir (~/.pandoc), user_config (--config), scripts (Python\Scripts)
    # TODO: --list -l - список переменных, которые задаются пандоктулзом и дефолтным скриптом.
    # TODO: --bash -b - использовать баш в винде (на свой страх и риск) тут задается путь к башу. Если вместу путя 'default', то пытаться найти его (но только в ПЭТХ, но не в текущей папке).
    # TODO: see `scripts`, `bat`, `sh` folders, `./cli` file. 
