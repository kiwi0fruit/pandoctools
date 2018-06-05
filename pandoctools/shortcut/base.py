import sys
import os
# import stat
from .exception import ShortcutError, ShortcutNoDesktopError, ShortcutNoMenuError
import traceback


class ShortCutter(object):
    """
    Creates applicaton shortcuts for Windows, MacOS and Linux operating systems.

    To create desktop and menu shortcuts to `python`::

        from shortcut import ShortCutter
        s = ShortCutter()
        s.create_desktop_shortcut("python")
        s.create_menu_shortcut("python")
        
    Attributes:
    -----------
    raise_errors : bool, default True
        Whether to raise exceptions or skip errors and continue
    error_log : object, default None
        File object where to write errors when raise_errors=False.
        Default is `None` - do not write errors.
        Can also be `sys.stderr` or `io.StringIO()`.
    desktop_folder : str
        Directory used when creating desktop shortcuts
    menu_folder : str
        Directory used when creating menu shortcuts
    bin_folder : str
        `Scripts` or `bin` dir path
        (the one to where setup.py installs if use `ShortCutter()` from setup.py)
    site_packages : str
        Site packages dir path
        (the one to where setup.py installs if use `ShortCutter()` from setup.py)
    """

    def __init__(self, raise_errors=True, error_log=None):
        """
        Creates ShortCutter.

        :param bool raise_errors:
            Whether to raise exceptions or skip errors and continue.
        :param error_log:
            File object where to write errors when raise_errors=False.
            Default is `None` - do not write errors.
            Can also be `sys.stderr` or `io.StringIO()`.
        """
        self.raise_errors = raise_errors
        self.error_log = error_log
        self.desktop_folder = self._get_desktop_folder()
        self.menu_folder = self._get_menu_folder()
        self.bin_folder = self._get_bin_folder()
        self.site_packages = self._get_site_packages()
        self._custom_init()

    # might be overridden if needed
    def _custom_init(self):
        pass

    # should be overridden
    def _get_desktop_folder(self):
        raise ShortcutError("_get_desktop_folder needs overriding")

    # should be overridden
    def _get_menu_folder(self):
        raise ShortcutError("_get_menu_folder needs overriding")

    # should be overridden
    def _get_bin_folder(self):
        raise ShortcutError("_get_bin_folder needs overriding")

    # should be overridden
    def _get_site_packages(self):
        raise ShortcutError("_get_site_packages needs overriding")

    def create_desktop_shortcut(self, target, shortcut_name=None, entry_point=False):
        """
        Creates a desktop shortcut to a target.

        :param str target:
            The target to create a shortcut for, it can be a fully qualified
            file path `/path/to/my_program` or a simple application name 
            `my_program`.
        :param str shortcut_name:
            Name of the shortcut without extension (.lnk would be appended if needed).
            If `None` uses the target filename. Defaults to `None`.
        :param bool entry_point:
            Whether to create shortcut to executable created via `entry_points` > `'console_scripts'` in `setup.py`
            If `create_shortcut` is run inside `setup.py` executable was not moved to it's place yet.

        Returns a tuple of (shortcut_name, target_path, shortcut_file_path)
        """
        if not os.path.isdir(self.desktop_folder):
            msg = "Desktop folder '{}' not found.".format(self.desktop_folder)
            if self.raise_errors:
                raise ShortcutNoDesktopError(msg)
            else:
                self.error_log.write(msg + '\n')
        else:
            return self.create_shortcut(target, self.desktop_folder, shortcut_name, entry_point)

    def create_menu_shortcut(self, target, shortcut_name=None, entry_point=False):
        """
        Creates a menu shortcut to a target.

        :param str target:
            The target to create a shortcut for, it can be a fully qualified
            file path `/path/to/my_program` or a simple application name 
            `my_program`.
        :param str shortcut_name:
            Name of the shortcut without extension (.lnk would be appended if needed).
            If `None` uses the target filename. Defaults to `None`.
        :param bool entry_point:
            Whether to create shortcut to executable created via `entry_points` > `'console_scripts'` in `setup.py`
            If `create_shortcut` is run inside `setup.py` executable was not moved to it's place yet.

        Returns a tuple of (shortcut_name, target_path, shortcut_file_path)
        """
        if not os.path.isdir(self.menu_folder):
            msg = "Menu folder '{}' not found.".format(self.menu_folder)
            if self.raise_errors:
                raise ShortcutNoMenuError(msg)
            else:
                self.error_log.write(msg + '\n')
        else:
            return self.create_shortcut(target, self.menu_folder, shortcut_name, entry_point)

    def create_shortcut(self, target, shortcut_directory, shortcut_name=None, entry_point=False):
        """
        Creates a shortcut to a target.

        :param str target:
            The target to create a shortcut for, it can be a fully qualified
            file path `/path/to/my_program` or a simple application name 
            `my_program`.
        :param str shortcut_directory:
            The directory path where the shortcut should be created.
        :param str shortcut_name:
            Name of the shortcut without extension (.lnk would be appended if needed).
            If `None` uses the target filename. Defaults to `None`.
        :param bool entry_point:
            Whether to create shortcut to executable created via `entry_points` > `'console_scripts'` in `setup.py`
            If `create_shortcut` is run inside `setup.py` executable was not moved to it's place yet.

        Returns a tuple of (shortcut_name, target_path, shortcut_file_path)
        """
        # Check entry_point input:
        if entry_point and os.path.basename(target) != target:
            raise ValueError('When entry_point=True target can be basename only.')

        # Check if target is dir or file:
        if entry_point:
            isdir = False
        elif (os.path.basename(target) == target) and (self.find_target(target) is not None):
            isdir = False
        else:
            isdir = True if os.path.isdir(target) else False

        # Set shortcut name:
        if shortcut_name is None:
            if entry_point:
                shortcut_name = target
            elif isdir:
                shortcut_name = os.path.basename(target)
            else:
                # getting the file name and removing the extension:
                shortcut_name = os.path.splitext(os.path.basename(target))[0]

        # Set the target path:
        if entry_point:
            target_path = os.path.join(self.bin_folder,
                                       target + ('.exe' if (os.name == 'nt') else ''))
        elif isdir:
            target_path = os.path.abspath(target)
        else:
            target_path = self.find_target(target)

        # Create shortcut:
        def create():
            if isdir:
                return self._create_shortcut_to_dir(shortcut_name, target_path, shortcut_directory)
            else:
                return self._create_shortcut_file(shortcut_name, target_path, shortcut_directory)

        if self.raise_errors:
            shortcut_file_path = create()
        else:
            # noinspection PyBroadException
            try:
                shortcut_file_path = create()
            except:
                shortcut_file_path = None
                self.error_log.write(''.join(traceback.format_exc()))

        return shortcut_name, target_path, shortcut_file_path

    # should be overridden
    def _create_shortcut_to_dir(self, shortcut_name, target_path, shortcut_directory):
        raise ShortcutError("_create_shortcut_to_dir needs overriding")

    # should be overridden
    def _create_shortcut_file(self, shortcut_name, target_path, shortcut_directory):
        raise ShortcutError("_create_shortcut_file needs overriding")

    def makedirs(self, *args):
        """
        Recursively creates dirs if they don't exist.
        Utilizes self.raise_errors and self.error_log

        :param args:
            Multiple paths (str) for folders to create.

        Returns True on success False of failure
        """
        ret = True
        for path in args:
            if not os.path.isdir(path):
                if self.raise_errors:
                    os.makedirs(path)
                else:
                    try:
                        os.makedirs(path)
                    except OSError:
                        if self.error_log is not None:
                            self.error_log.write(''.join(traceback.format_exc()))
                        ret = False
        return ret

    def find_target(self, target):
        """
        Finds a file path for a target application.

        :param str target:
            The target to find, it can be a fully qualified
            file path `/path/to/my_program` or a simple application name 
            `my_program`.

        Returns a single target file path or ``None`` if a path cant be found.
        """
        if os.path.isfile(target):
            return os.path.abspath(target)
        else:
            targets = self.search_for_target(target)
            if len(targets) > 0:
                return targets[0]
            else:
                return None

    def search_for_target(self, target):
        """
        Searches for a target application.

        :param str target:
            The target to find.

        Returns a list of potential target file paths, it no paths are found an empty list is returned.s
        """
        # potential list of app paths
        target_paths = []

        # create list of potential directories
        paths = self._get_paths()

        # loop through each folder
        for path in paths:
            if os.path.exists(path):
                # is it a directory?
                if os.path.isdir(path):
                    # get files in directory
                    for file_name in os.listdir(path):
                        file_path = os.path.join(path, file_name)
                        if os.path.isfile(file_path):
                            if self._is_file_the_target(target, file_name, file_path):
                                target_paths.append(file_path)
                else:
                    # its not a directory, is it the app we are looking for?
                    pass

        return target_paths

    # needs overriding
    def _is_file_the_target(self, target, file_name, file_path):
        raise ShortcutError("_is_file_the_target needs overriding")

    def _get_paths(self):
        """
        Gets paths from the PATH environment variables.

        Returns a list of paths.
        """
        # get folders from PATH
        paths = os.environ['PATH'].split(os.pathsep)

        return paths
