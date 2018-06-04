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
    """

    def __init__(self, raise_errors=True, error_log=None):
        """
        Creates ShortCutter.

        :param bool raise_errors:
            Whether to raise exceptions or skip errors and continue.
        :param error_log:
            File object where to write errors in a skip_errors mode.
            Default is `None` - do not write errors.
            Can also be `sys.stderr` or `io.StringIO()`.
        """
        self.skip_errors = skip_errors
        self.error_log = error_log
        self.desktop_folder = self._get_desktop_folder()
        self.menu_folder = self._get_menu_folder()

    # should be overridden
    def _get_desktop_folder(self):
        raise ShortcutError("_get_desktop_folder needs overriding")

    # should be overridden
    def _get_menu_folder(self):
        raise ShortcutError("_get_menu_folder needs overriding")

    def create_desktop_shortcut(self, target, target_name=None, entry_point=False):
        """
        Creates a desktop shortcut to a target.

        :param str target:
            The target to create a shortcut for, it can be a fully qualified
            file path `/path/to/my_program` or a simple application name 
            `my_program`.
        :param str target_name:
            Name of the shortcut without extension (.lnk would be appended if needed).
            If `None` uses the target filename. Defaults to `None`.
        :param str virtual_type: `None` | `'file'` | `'dir'`
            Whether to create shortcut to yet non-existing file/dir (creates dir)
            Default is `None` - do not create

        Returns a tuple of (target_name, target_path, shortcut_file_path)
        """
        isdir, virtual = self._isdir_virtual(target, virtual_type)

        if not os.path.isdir(self.desktop_folder):
            msg = "Desktop folder '{}' not found.".format(self.desktop_folder)
            if not self._silent:
                raise ShortcutNoDesktopError(msg)
            else:
                self._err_file.write(msg + '\n')
        else:
            if isdir:
                return self.create_shortcut_to_dir(target, self.desktop_folder, target_name, virtual)
            else:
                return self.create_shortcut(target, self.desktop_folder, target_name, virtual)

    def create_menu_shortcut(self, target, target_name=None, entry_point=False):
        """
        Creates a menu shortcut to a target.

        :param str target:
            The target to create a shortcut for, it can be a fully qualified
            file path `/path/to/my_program` or a simple application name 
            `my_program`.
        :param str target_name:
            Name of the shortcut without extension (.lnk would be appended if needed).
            If `None` uses the target filename. Defaults to `None`.
        :param str virtual_type: `None` | `'file'` | `'dir'`
            Whether to create shortcut to yet non-existing file/dir (creates dir)
            Default is `None` - do not create

        Returns a tuple of (target_name, target_path, shortcut_file_path)
        """
        isdir, virtual = self._isdir_virtual(target, virtual_type)

        if not os.path.isdir(self.menu_folder):
            msg = "Menu folder '{}' not found.".format(self.menu_folder)
            if not self._silent:
                raise ShortcutNoMenuError(msg)
            else:
                self._err_file.write(msg + '\n')
        else:
            if isdir:
                return self.create_shortcut_to_dir(target, self.menu_folder, target_name, virtual)
            else:
                return self.create_shortcut(target, self.menu_folder, target_name, virtual) 

    def create_shortcut(self, target, shortcut_directory, target_name=None, entry_point=False):
        """
        Creates a shortcut to a target.

        :param str target:
            The target to create a shortcut for, it can be a fully qualified
            file path `/path/to/my_program` or a simple application name 
            `my_program`.
        :param str shortcut_directory:
            The directory path where the shortcut should be created.
        :param str target_name:
            Name of the shortcut without extension (.lnk would be appended if needed).
            If `None` uses the target filename. Defaults to `None`.
        :param bool virtual:
            Whether to create shortcut to yet non-existing file
            Default is `False` - do not create

        Returns a tuple of (target_name, target_path, shortcut_file_path)
        """
        # Check entry_point input:
        if entry_point and (os.path.basename(target) != target):
            raise ValueError('When entry_point=True target can be basename only.')

        # check if target is dir or file:
        isdir = True if os.path.isdir(target) else False

        # get the target name by getting the file name and removing the extension
        if target_name is None:
            target_name = os.path.basename(target)
            target_name = target_name if isdir or entry_point else os.path.splitext(target_name)[0]

        # find the target path:
        target_path = os.path.abspath(target) if isdir else self.find_target(target)

        if entry_point:
            if not os.path.basename(target_path) == target_path
            # Create temporal file in order to create shortcut in entry_point mode:
            clean = False

            def create_temp_target():
                if not os.path.isdir(os.path.dirname(target)):
                    os.makedirs(os.path.dirname(target))
                open(target, 'a').close()

            if target_path is None:
                if not self._silent:
                    create_temp_target()
                    clean = True
                else:
                    try:
                        create_temp_target()
                        clean = True
                    except (OSError, IOError):
                        self._err_file.write(''.join(traceback.format_exc()))

            target_path = self.find_target(target)

        def mkshrtct():
            if entry_point:
                return self._create_entry_point_shortcut(target_name, target_path, shortcut_directory)
            elif isdir:
                return self._create_shortcut_to_dir(target_name, target_path, shortcut_directory)
            else:
                return self._create_shortcut_file(target_name, target_path, shortcut_directory)

        # Create shortcut to the target_path:
        if self.raise_errors:
            shortcut_file_path = mkshrtct()
        else:
            # noinspection PyBroadException
            try:
                shortcut_file_path = mkshrtct()
            except:
                shortcut_file_path = None
                self._err_file.write(''.join(traceback.format_exc()))



        # Create shortcut to the target_path:
        if not self._silent:
            shortcut_file_path = self._create_shortcut_file(target_name, target_path, shortcut_directory)
        else:
            # noinspection PyBroadException
            try:
                shortcut_file_path = self._create_shortcut_file(target_name, target_path, shortcut_directory)
            except:
                shortcut_file_path = None
                self._err_file.write(''.join(traceback.format_exc()))

        # Delete temporal file:
        if clean:
            os.remove(target)

        return target_name, target_path, shortcut_file_path

    def create_shortcut_to_dir(self, target_path, shortcut_directory, target_name=None, virtual=False):
        """
        Creates a shortcut to a direcrory.

        :param str target_path:
            The target directory path to create a shortcut for.
        :param str shortcut_directory:
            The directory path where the shortcut should be created.
        :param str target_name:
            Name of the shortcut without extension (.lnk would be appended if needed).
            If `None` uses the target filename. Defaults to `None`.
        :param bool virtual:
            Whether to create shortcut to yet non-existing dir (creates dir)
            Default is `False` - do not create

        Returns a tuple of (target_name, target_path, shortcut_file_path)
        """
        if target_name is None:
            # get the target_name by getting the target dir name
            target_name = os.path.basename(target_path)

        # Expand to abs path:
        target_path = os.path.abspath(target_path)

        # Create target_path if it doesn't exist in virtual mode:
        if not os.path.isdir(target_path) and virtual:
            if not self._silent:
                os.makedirs(target_path)
            else:
                try:
                    os.makedirs(target_path)
                except OSError:
                    self._err_file.write(''.join(traceback.format_exc()))

        # Create shortcut to the target_path:
        if not self._silent:
            shortcut_file_path = self._create_shortcut_to_dir(target_name, target_path, shortcut_directory)
        else:
            # noinspection PyBroadException
            try:
                shortcut_file_path = self._create_shortcut_to_dir(target_name, target_path, shortcut_directory)
            except:
                shortcut_file_path = None
                self._err_file.write(''.join(traceback.format_exc()))

        return target_name, target_path, shortcut_file_path

    # should be overridden
    def _create_shortcut_to_dir(self, target_name, target_path, shortcut_directory):
        raise ShortcutError("_create_shortcut_to_dir needs overriding")

    # should be overridden
    def _create_shortcut_file(self, target_name, target_path, shortcut_directory):
        raise ShortcutError("_create_shortcut_file needs overriding")

    def makedirs(*args):
        """
        Recursively creates dirs if they don't exist.
        Utilizes self.raise_errors and self.error_log
        
        :param str *args:
            Multiple paths for folders to create. 
        """
        for path in args:
            if not sys.path.isdir(path):
                if self.raise_errors:
                    os.makedirs(path)
                else:
                    try:
                        os.makedirs(path)
                    except OSError:
                        if self.error_log is not None:
                            self.error_log.write(''.join(traceback.format_exc()))

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
            targets = self._search_for_target(target)
            if len(targets) > 0:
                return targets[0]
            else:
                return None

    def _search_for_target(self, target):
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

    @staticmethod
    def _get_paths():
        """
        Gets paths from the PATH environment variables.

        Returns a list of paths.
        """
        # get folders from PATH
        paths = os.environ['PATH'].split(os.pathsep)

        return paths
