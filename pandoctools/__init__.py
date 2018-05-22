from .panfl import main as panfl, autorun_filters, pandoctools_user, pandoctools_core, pandoctools_bin  # noqa

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
