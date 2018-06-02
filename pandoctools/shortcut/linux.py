import os
import stat
# from .exception import *
from .base import ShortCutter


class ShortCutterLinux(ShortCutter):
    def _get_desktop_folder(self):
        import subprocess
        return subprocess.check_output([
            'xdg-user-dir',
            'DESKTOP'
        ]).decode('utf-8').strip()

    def _get_menu_folder(self):
        return os.path.join(os.path.join(os.path.expanduser('~')), '.local', 'share', 'applications')

    def _create_shortcut_to_dir(self, target_name, target_path, shortcut_directory):
        """
        Creates a Unix shortcut to a directory via symbolic link.

        Returns shortcut_file_path
        """
        shortcut_file_path = os.path.join(shortcut_directory, target_name)
        if os.path.islink(shortcut_file_path):
            os.remove(shortcut_file_path)
        os.symlink(target_path, shortcut_file_path)
        return shortcut_file_path

    def _create_shortcut_file(self, target_name, target_path, shortcut_directory):
        """
        Creates a Linux shortcut file.

        Returns shortcut_file_path
        """
        shortcut_file_path = os.path.join(shortcut_directory, "launch_" + target_name + ".desktop")
        with open(shortcut_file_path, "w") as shortcut:
            shortcut.write("[Desktop Entry]\n")
            shortcut.write("Name={}\n".format(target_name))
            shortcut.write("Exec={} %F\n".format(target_path))
            shortcut.write("Terminal=true\n")
            shortcut.write("Type=Application\n")

            # make the launch file executable
            st = os.stat(shortcut_file_path)
            os.chmod(shortcut_file_path, st.st_mode | stat.S_IEXEC)

        return shortcut_file_path

    def _is_file_the_target(self, target, file_name, file_path):
        match = False
        if file_name == target:
            # is the file executable
            if os.access(file_path, os.X_OK):
                match = True
            else:
                match = False
        return match
