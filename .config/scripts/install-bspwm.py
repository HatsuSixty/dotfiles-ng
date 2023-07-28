#!/bin/env python3

from subprocess import run
from os import getenv
from sys import stderr

import psutil

processes = (p.name().upper().strip() for p in psutil.process_iter())

if "SWAY" in processes or "HYPRLAND" in processes:
    print("ERROR: You cannot uninstall Sway or Hyprland white it's running", file=stderr)
    exit(1)

def remove_if_installed(package):
    if run(["yay", "-Qs", package]).returncode == 0:
        run(["yay", "-Rns", package])

def install_package(package):
    run(["yay", "-S", package])

remove_if_installed("sway")
remove_if_installed("hyprland")
remove_if_installed("xdg-desktop-portal-hyprland")
remove_if_installed("xdg-desktop-portal-wlr")

install_package("bspwm")
install_package("sxhkd")
install_package("polybar-git")
