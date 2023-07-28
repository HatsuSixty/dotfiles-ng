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

remove_if_installed("bspwm")
remove_if_installed("sxhkd")
remove_if_installed("polybar-git")

remove_if_installed("sway")

install_package("xdg-desktop-portal-hyprland")
remove_if_installed("xdg-desktop-portal-wlr")

install_package("hyprland")
install_package("waybar")
