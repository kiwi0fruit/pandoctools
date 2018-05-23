from .cli import pandoctools_user, pandoctools_bin  # noqa

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
