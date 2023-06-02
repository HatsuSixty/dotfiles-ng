#!/bin/env python3

from subprocess import run
from os import getenv
from sys import stderr

import psutil

if "SWAY" in (p.name().upper().strip() for p in psutil.process_iter()):
    print("ERROR: You cannot uninstall Sway white it's running", file=stderr)
    exit(1)

def remove_if_installed(package):
    if run(["yay", "-Qs", package]).returncode == 0:
        run(["yay", "-Rns", package])

def install_package(package):
    run(["yay", "-S", package])

remove_if_installed("hyprland")
remove_if_installed("waybar-hyprland")

install_package("xdg-desktop-portal-wlr")
remove_if_installed("xdg-desktop-portal-hyprland")

install_package("sway")
