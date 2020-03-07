#!/usr/bin/python3

import glob
import os
import re
import sys


def log_patching(file, reason):
    print(f"Patching {file} for {reason}...")


def remove_signals(WS_SRC):
    TARGET_FILE = os.path.join(WS_SRC, '**', 'CMakeLists.txt')

    for cmake in glob.glob(TARGET_FILE, recursive=True):
        regex = re.compile(r"(find_package\(.*Boost.*) signals(.*\))")
        with open(cmake, 'r+') as f:
            content = f.read()
            match = re.findall(regex, content)
            if match:
                log_patching(cmake, "remove signals")
                result = re.sub(regex, r"\1\2", content)
                f.seek(0)
                f.truncate()
                f.write(result)


def add_class_loader(WS_SRC):
    TARGET_PKGS = [
        os.path.join('ros_controllers', 'position_controllers'),
        os.path.join('ros_controllers', 'diff_drive_controller')
    ]

    for pkg in TARGET_PKGS:
        cmake = os.path.join(WS_SRC, pkg, 'CMakeLists.txt')
        regex = re.compile(r"(find_package\(.*catkin(?:.|\n)*?)\)")
        with open(cmake, 'r+') as f:
            log_patching(cmake, "link class_loader")
            content = f.read()
            result = re.sub(regex, r"\1 class_loader)", content)
            f.seek(0)
            f.truncate()
            f.write(result)


def fix_pip_setup(WS_SRC):
    TARGET_PKGS = [os.path.join('kdl_parser', 'kdl_parser_py')]

    for pkg in TARGET_PKGS:
        setup_py = os.path.join(WS_SRC, pkg, 'setup.py')
        with open(setup_py, 'r+') as f:
            log_patching(setup_py, "setup script")
            content = f.read()
            result = content.replace("package_dir={'': ''}", "package_dir={'': '.'}")
            f.seek(0)
            f.truncate()
            f.write(result)


def rename_boost_python(WS_SRC):
    TARGET_FILE = os.path.join(WS_SRC, '**', 'CMakeLists.txt')
    regex = re.compile(r"(find_package\(.*Boost.*) python3(.*\))")

    for cmake in glob.glob(TARGET_FILE, recursive=True):
        with open(cmake, 'r+') as f:
            content = f.read()
            match = re.findall(regex, content)
            if match:
                log_patching(cmake, "boost python")
                result = re.sub(regex, r"\1 python\2", content)
                f.seek(0)
                f.truncate()
                f.write(result)


def openssl_inc(WS_SRC):
    TARGET_PKG = os.path.join(WS_SRC, 'ros_comm', 'rosbag_storage')
    cmake = os.path.join(TARGET_PKG, 'CMakeLists.txt')
    insert_entry = "project(rosbag_storage)"
    insert_contents = [
        insert_entry,
        ""
        "if(APPLE)",
        "  include_directories(\"/usr/local/opt/openssl@1.1/include\")",
        "  link_directories(\"/usr/local/opt/openssl@1.1/lib\")",
        "  link_directories(\"/usr/local/lib\")",
        "endif()"
    ]
    insert_content = '\n'.join(insert_contents)

    with open(cmake, 'r+') as f:
        log_patching(cmake, "openssl")
        content = f.read()
        result = content.replace(insert_entry, insert_content)
        f.seek(0)
        f.truncate()
        f.write(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 patch.py <src>")
        exit(0)

    remove_signals(sys.argv[1])
    add_class_loader(sys.argv[1])
    fix_pip_setup(sys.argv[1])
    rename_boost_python(sys.argv[1])
    openssl_inc(sys.argv[1])
