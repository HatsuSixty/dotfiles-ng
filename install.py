#!/bin/env python3

from os import getenv, listdir, makedirs, walk
from os.path import isdir, isfile, join, dirname, basename, splitext, abspath
from shutil import copy, move
from subprocess import run
from sys import argv, stderr, stdout
import ctypes
import sys
from typing import IO, Any

def USER() -> str:
    if sys.platform == 'linux':
        return listdir("/home")[0]
    elif sys.platform == 'win32':
        print("INTERNAL ERROR: `USER` constant should not be used in Windows", file=stderr)
        exit(1)

def HOME() -> str:
    if sys.platform == 'linux':
        return "/home/" + USER()
    elif sys.platform == 'win32':
        print("INTERNAL ERROR: `HOME` constant should not be used in Windows", file=stderr)
        exit(1)

def TEMP() -> str:
    if sys.platform == 'linux':
        return "/tmp"
    elif sys.platform == 'win32':
        return getenv("TEMP")

def APPDATA() -> str:
    if sys.platform == 'linux':
        print("INTERNAL ERROR: `HOME` constant should not be used in Linux", file=stderr)
        exit(1)
    elif sys.platform == 'win32':
        return getenv("APPDATA")

def get_programs_from_packagestxt(f: str) -> list[str]:
    return open(f).read().split()

def install_packages_arch(packages: list) -> None:
    run(["pacman", "-Syu", "--needed"] + packages)

def install_packages_fedora(packages: list) -> None:
    run(["dnf", "install"] + packages)

def install_packages_ubuntu(packages: list) -> None:
    run(["apt", "install"] + packages)

def create_symlink_windows(src: str, dst: str) -> None:
    run(["cmd", "/c", "mklink /d " + dst + " " + src])

def install_fonts() -> None:
    fonts_url = "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.1.1/Iosevka.zip"

    if sys.platform == 'win32':
        run(["curl", "-fkLo", TEMP() + "\\fonts.zip", fonts_url])
        if not isdir(TEMP() + "\\fonts"):
            makedirs(TEMP() + "\\fonts")

        run(["unzip", TEMP() + "\\fonts.zip", "-d", TEMP() + "\\fonts"])

        fonts = listdir(TEMP() + "\\fonts")
        for f in fonts:
            fupper = f.upper()
            if not (fupper.endswith(".MD") or fupper.endswith(".TXT")):
                run(["cmd", "/c", TEMP() + "\\fonts\\" + f])
    elif sys.platform == 'linux':
        if not isfile(HOME() + "/.cache/fonts.zip"):
            run(["wget",
                 fonts_url,
                 "-O",
                 HOME() + "/.cache/fonts.zip"])
            if not isdir(HOME() + "/.cache/fonts"):
                makedirs(HOME() + "/.cache/fonts")

            run(["unzip", HOME() + "/.cache/fonts.zip", "-d", HOME() + "/.cache/fonts"])

            for directory, folders, files in walk(HOME() + "/.cache/fonts"):
                for f in files:
                    fil = join(directory, f)
                    move(fil, join(dirname(fil), basename(fil).replace(' ', '')))

            fonts = listdir(HOME() + "/.cache/fonts")
            for f in fonts:
                fupper = f.upper()
                if not fupper.endswith(".MD") or fupper.endswith(".TXT"):
                    copy(HOME() + "/.cache/fonts/" + f, "/usr/share/fonts/" + f)
    else:
        print("ERROR: Unsupported platform", file=stderr)
        exit(1)

def install_linux_shell() -> None:
    # Install zsh-syntax-highlighting
    ZSH_SH_PATH = f"{HOME()}/.zshsh"
    if not isdir(ZSH_SH_PATH) and not isfile(ZSH_SH_PATH):
        run(["wget", "https://github.com/zsh-users/zsh-syntax-highlighting/archive/refs/tags/0.7.1.tar.gz", "-O", f"{HOME()}/.cache/a.tar.gz"])
        run(["tar", "-axvf", f"{HOME()}/.cache/a.tar.gz", "-C", f"{HOME()}/.cache"])
        move(f"{HOME()}/.cache/zsh-syntax-highlighting-0.7.1", ZSH_SH_PATH)

    # backup .bashrc
    move(f"{HOME()}/.bashrc", f"{HOME()}/.bashrc.bak")

    # Install zsh-autosuggestions
    ZSH_AS_PATH = f"{HOME()}/.zshas"
    if not isdir(ZSH_AS_PATH) and not isfile(ZSH_AS_PATH):
        run(["git", "clone", "--depth=1", "https://github.com/zsh-users/zsh-autosuggestions.git", ZSH_AS_PATH])

    # Install powerlevel0k
    run(["git", "clone", "--depth=1", "https://github.com/romkatv/powerlevel10k.git", f"{HOME()}/.powerlevel10k"])

    # Install eza
    run(["wget", "https://github.com/eza-community/eza/releases/download/v0.17.0/eza_x86_64-unknown-linux-gnu.zip", "-O", f"{HOME()}/.cache/eza.zip"])
    run(["unzip", HOME() + "/.cache/eza.zip", "-d", HOME() + "/.cache/eza"])
    makedirs(HOME() + "/.local/bin", exist_ok=True)
    copy(HOME() + "/.cache/eza/eza", HOME() + "/.local/bin/eza")

def install_linux_dotfiles() -> None:
    run(["stow", "."])

def install_windows_dotfiles() -> None:
    create_symlink_windows(abspath(".\\.config\\emacs"), APPDATA() + "\\.emacs.d")
    create_symlink_windows(abspath(".\\.config\\nvim"),
                           abspath(APPDATA() + "\\..\\Local\\nvim"))

def usage(stream: IO[Any]) -> None:
    print("USAGE: ./install.py <SUBCOMMAND>", file=stream)
    print("  SUBCOMMANDs:", file=stream)
    print("    help          Shows this help", file=stream)
    print("    windows        Install for Windows", file=stream)
    print("    linux <DISTRO> Install for Linux <DISTRO>", file=stream)
    print("      DISTROs:")
    print("        arch          Install configurations for Arch Linux", file=stream)
    print("        archwm        Install configurations for Arch Linux under Wayland", file=stream)
    print("        fedora        Install configurations for Fedora", file=stream)
    print("        ubuntu        Install configurations for Fedora", file=stream)

if __name__ == '__main__':
    if len(argv) < 2:
        print("ERROR: No subcommand was provided", file=stderr)
        usage(stderr)
        exit(1)

    if sys.platform == 'linux':
        if getenv("USER") != "root":
            run(["sudo", "python", __file__] + argv[1:])
            exit(0)
    elif sys.platform == 'win32':
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            print("ERROR: This script must be run as administrator", file=stderr)
            exit(1)
    else:
        print("ERROR: Unsupported platform", file=stderr)
        exit(1)

    install_fonts()
    exit(0)

    subcommand = argv[1]
    if subcommand == "help":
        usage(stdout)
        exit(0)
    elif subcommand == "windows":
        install_fonts()
        install_windows_dotfiles()
    elif subcommand == "linux":
        if len(argv) < 3:
            print("ERROR: No distribution was provided", file=stderr)
            usage(stderr)
            exit(1)

        distro = argv[2]
        if distro == "arch":
            install_packages_arch(get_programs_from_packagestxt("packages.arch.txt"))
        elif distro == "archwm":
            install_packages_arch(get_programs_from_packagestxt("packages.arch.txt"))
            install_packages_arch(get_programs_from_packagestxt("packages.archwm.txt"))
        elif distro == "fedora":
            install_packages_fedora(get_programs_from_packagestxt("packages.fedora.txt"))
        elif distro == "ubuntu":
            install_packages_ubuntu(get_programs_from_packagestxt("packages.ubuntu.txt"))
        else:
            print(f"ERROR: Unsupported distribution: `{distro}`", file=stderr)
            usage(stderr)
            exit(1)

        install_fonts()
        install_linux_shell()
        install_linux_dotfiles()
        run(["gcc", "-o",
             HOME() + "/.config/scripts/terminal",
             HOME() + "/.config/scripts/terminal.c"])
    else:
        print(f"ERROR: Unknown subcommand: `{subcommand}`", file=stderr)
        usage(stderr)
        exit(1)
