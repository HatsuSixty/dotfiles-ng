#!/bin/env python3

from os import getenv, listdir, makedirs, walk
from os.path import isdir, isfile, join, dirname, basename
from shutil import copy, move
from subprocess import run
from sys import argv, stderr, stdout

def get_programs_from_packagestxt(f):
    return open(f).read().split()

if getenv("USER") != "root":
    run(["sudo", "python", __file__] + argv[1:])
    exit(0)

USER = listdir("/home")[0]
HOME = "/home/" + USER

def usage(stream):
    print("USAGE: ./install.py <SUBCOMMAND>", file=stream)
    print("  SUBCOMMANDs:", file=stream)
    print("    arch          Install configurations for Arch Linux", file=stream)
    print("    archwayland   Install configurations for Arch Linux under Wayland", file=stream)
    print("    fedora        Install configurations for Fedora", file=stream)
    print("    ubuntu        Install configurations for Fedora", file=stream)
    print("    help          Shows this help", file=stream)

if len(argv) < 2:
    print("ERROR: No subcommand was provided", file=stderr)
    usage(stderr)
    exit(1)

if argv[1] == "arch":
    run(["pacman", "-Syu", "--needed"] + get_programs_from_packagestxt("packages.arch.txt"))
elif argv[1] == "archwayland":
    run(["pacman", "-Syu", "--needed"] + get_programs_from_packagestxt("packages.arch.txt"))
    run(["pacman", "-Syu", "--needed"] + get_programs_from_packagestxt("packages.archwayland.txt"))

    # install yay
    run(["sudo", "-u", USER, "sh", "-c", f"git clone https://aur.archlinux.org/yay.git {HOME}/.cache/yay-aur"])
    run(["sh", "-c", f"cd {HOME}/.cache/yay-aur && sudo -u {USER} makepkg -si"])

    # install waybar
    run(["sudo", "-u", USER, "yay -S waybar-hyprland"])
elif argv[1] == "fedora":
    run(["dnf", "install"] + get_programs_from_packagestxt("packages.fedora.txt"))
elif argv[1] == "ubuntu":
    run(["apt", "install"] + get_programs_from_packagestxt("packages.ubuntu.txt"))
elif argv[1] == "help":
    usage(stdout)
    exit(0)
else:
    print(f"ERROR: Unknown subcommand: `{argv[1]}`", file=stderr)
    usage(stderr)
    exit(1)

# install fonts

if not isfile(HOME + "/.cache/fonts.zip"):
    run(["wget",
        "https://github.com/ryanoasis/nerd-fonts/releases/download/v2.2.2/FiraMono.zip",
        "-O",
        HOME + "/.cache/fonts.zip"])
    if not isdir(HOME + "/.cache/fonts"):
        makedirs(HOME + "/.cache/fonts")
    run(["unzip", HOME + "/.cache/fonts.zip", "-d", HOME + "/.cache/fonts"])

    for directory, folders, files in walk(HOME + "/.cache/fonts"):
        for f in files:
            fil = join(directory, f)
            move(fil, join(dirname(fil), basename(fil).replace(' ', '')))

    fonts = listdir(HOME + "/.cache/fonts")
    for f in fonts:
        if not (f.endswith(".md") or f.endswith(".txt") or f.endswith(".MD") or f.endswith(".TXT")):
            copy(HOME + "/.cache/fonts/" + f, "/usr/share/fonts/" + f)

# install configuration files

# backup .bashrc
move(f"{HOME}/.bashrc", f"{HOME}/.bashrc.bak")

run(["stow", "."])

# Install zsh-syntax-highlighting

ZSH_SH_PATH = f"{HOME}/.zshsh"
if not isdir(ZSH_SH_PATH) and not isfile(ZSH_SH_PATH):
    run(["wget", "https://github.com/zsh-users/zsh-syntax-highlighting/archive/refs/tags/0.7.1.tar.gz", "-O", f"{HOME}/.cache/a.tar.gz"])
    run(["tar", "-axvf", f"{HOME}/.cache/a.tar.gz", "-C", f"{HOME}/.cache"])
    move(f"{HOME}/.cache/zsh-syntax-highlighting-0.7.1", ZSH_SH_PATH)

# Install zsh-autosuggestions

ZSH_AS_PATH = f"{HOME}/.zshas"
if not isdir(ZSH_AS_PATH) and not isfile(ZSH_AS_PATH):
    run(["git", "clone", "--depth=1", "https://github.com/zsh-users/zsh-autosuggestions.git", ZSH_AS_PATH])

# Install powerlevel0k
run(["git", "clone", "--depth=1", "https://github.com/romkatv/powerlevel10k.git", f"{HOME}/.powerlevel10k"])
