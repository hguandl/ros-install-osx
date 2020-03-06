#!/usr/bin/python

import glob
import os
import re

WS_SRC = os.path.join(os.environ['HOME'], 'ros_catkin_ws', 'src')

def remove_signals():
    TARGET_FILE = os.path.join(WS_SRC, '*', 'CMakeLists.txt')

    for cmake in glob.glob(TARGET_FILE):
        regex = re.compile(r"(find_package\(.*Boost.*) signals(.*\))")
        with open(cmake, 'r+') as f:
            content = f.read()
            match = re.findall(regex, content)
            if match:
                result = re.sub(regex, r"\1\2", content)
                f.seek(0)
                f.write(result)


def add_class_loader():
    TARGET_PKGS = [
        os.path.join('ros_controllers', 'position_controllers'),
        os.path.join('ros_controllers', 'diff_drive_controller')
    ]

    for pkg in TARGET_PKGS:
        cmake = os.path.join(WS_SRC, pkg, 'CMakeLists.txt')
        regex = re.compile(r"(find_package\(.*catkin(?:.|\n)*?)\)")
        with open(cmake, 'r+') as f:
            content = f.read()
            result = re.sub(regex, r"\1 class_loader)", content)
            f.seek(0)
            f.write(result)


def fix_pip_setup():
    TARGET_PKGS = [os.path.join('kdl_parser', 'kdl_parser_py')]

    for pkg in TARGET_PKGS:
        setup_py = os.path.join(WS_SRC, pkg, 'setup.py')
        with open(setup_py, 'r+') as f:
            content = f.read()
            result = content.replace("package_dir={'': ''}", "package_dir={'': '.'}")
            f.seek(0)
            f.write(result)


if __name__ == "__main__":
    remove_signals()
    add_class_loader()
    fix_pip_setup()
