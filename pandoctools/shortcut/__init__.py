# get operating system
import sys
platform = sys.platform
if sys.platform.startswith("linux"):
    platform = "linux"

# operating system specific imports
if platform == "win32":
    from .windows import ShortCutterWindows as ShortCutter
elif platform == "linux":
    from .linux import  ShortCutterLinux as ShortCutter
elif platform == "darwin":
    from .macos import ShortCutterMacOS as ShortCutter
else:
    raise Exception("Error: '{}' platform is not supported.")

from .exception import *

def main():
    
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Auto shortcut creator")
    parser.add_argument("target", help="The target executable to create Desktop and Menu shortcuts")
    parser.add_argument("-d", "--desktop", help="Only create a desktop shortcut", action="store_true")
    parser.add_argument("-m", "--menu", help="Only create a menu shortcut", action="store_true")
    args = parser.parse_args()
    
    create_desktop = args.desktop
    create_menu = args.menu

    # if desktop or menu hasnt been specified create both (i.e. the default)
    if not create_desktop and not create_menu:
        create_desktop = True
        create_menu = True

    shortcutter = ShortCutter()

    try:
        target_path = shortcutter.find_target(args.target)

        if target_path:

            desktop_created = False
            if create_desktop:
                try:
                    shortcutter.create_desktop_shortcut(target_path)
                    desktop_created = True
                except ShortcutNoDesktopError as e:
                    print("Failed to create desktop shortcut")
                    print(e)

            menu_created = False
            if create_menu:    
                try:
                    shortcutter.create_menu_shortcut(target_path)
                    menu_created = True
                except ShortcutNoMenuError as e:
                    print("Failed to create menu shortcut")
                    print(e)
                
            if desktop_created or menu_created:
                print("Shortcut created for '{}'".format(args.target))

        else:
            print("Shortcut failed: unable to find '{}'".format(args.target))

    except ShortcutError as e:
        print("Shortcut failed: '{}'".format(e))

