from os import path as p
import os


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
