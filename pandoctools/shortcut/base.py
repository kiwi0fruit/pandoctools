import sys
import os
import stat
from .exception import *

class ShortCutter(object):
    """
    Creates applicaton shortcuts for Windows, MacOS and Linux operating systems.

    To create desktop and menu shortcuts to `python`::

        from shortcut import ShortCutter
        s = ShortCutter()
        s.create_desktop_shortcut("python")
        s.create_menu_shortcut("python")
    """

    def __init__(self):
        self._desktop_folder = self._get_desktop_folder()
        self._menu_folder = self._get_menu_folder()

    # should be overridden
    def _get_desktop_folder(self):
        raise ShortcutError("_get_desktop_folder needs overriding")
    
    # should be overridden
    def _get_menu_folder(self):
        raise ShortcutError("_get_menu_folder needs overriding")

    def create_desktop_shortcut(self, target):
        """
        Creates a desktop shortcut to a target.

        :param str target:
            The target to create a shortcut for, it can be a fully qualified
            file path `/path/to/my_program` or a simple application name 
            `my_program`.

        Returns a tuple of (target_name, target_path, shortcut_file_path)
        """
        if not os.path.isdir(self._desktop_folder):
            raise ShortcutNoDesktopError("Desktop folder '{}' not found".format(self._desktop_folder))

        return self.create_shortcut(target, self._desktop_folder)

    def create_menu_shortcut(self, target):
        """
        Creates a menu shortcut to a target.

        :param str target:
            The target to create a shortcut for, it can be a fully qualified
            file path `/path/to/my_program` or a simple application name 
            `my_program`.
        
        Returns a tuple of (target_name, target_path, shortcut_file_path)
        """
        if not os.path.isdir(self._menu_folder):
            raise ShortcutNoMenuError("Menu folder '{}' not found".format(self._menu_folder))

        return self.create_shortcut(target, self._menu_folder) 

    def create_shortcut(self, target, shortcut_directory):
        """
        Creates a shortcut to a target.

        :param str target:
            The target to create a shortcut for, it can be a fully qualified
            file path `/path/to/my_program` or a simple application name 
            `my_program`.

        :param str shortcut_directory:
            The directory path where the shortcut should be created.

        Returns a tuple of (target_name, target_path, shortcut_file_path)
        """
        # get the target name by getting the file name and removing the extension
        target_name = os.path.splitext(os.path.basename(target))[0]

        # find for the target path  
        target_path = self.find_target(target)

        shortcut_file_path = self._create_shortcut_file(target_name, target_path, shortcut_directory)

        return (target_name, target_path, shortcut_file_path)

    #needs overriding
    def _create_shortcut_file(self, target_name, target_path, shortcut_directory):
        raise ShortcutError("create_shortcut_file needs overriding")

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

    @property
    def desktop_directory(self):
        """
        Sets or returns the directory used when creating desktop shortcuts. 
        """
        return self._desktop_folder

    @desktop_directory.setter
    def desktop_directory(self, value):
        self._desktop_folder = value

    @property
    def menu_directory(self):
        """
        Sets or returns the directory used when creating menu shortcuts. 
        """
        return self._menu_folder

    @menu_directory.setter
    def menu_directory(self, value):
        self._menu_folder = value