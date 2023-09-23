#!/bin/env python3

from os import getenv, listdir, makedirs, walk, name
from os.path import isdir, isfile, join, dirname, basename, splitext, abspath
from shutil import copy, move
from subprocess import run
from sys import argv, stderr, stdout
if name == 'nt':
    import ctypes

USER = ""
HOME = ""
TEMP = ""
APPDATA = ""
if name == 'posix':
    USER = listdir("/home")[0]
    HOME = "/home/" + USER
    TEMP = "/tmp"
if name == 'nt':
    TEMP = getenv("TEMP")
    APPDATA = getenv("APPDATA")

def get_programs_from_packagestxt(f):
    return open(f).read().split()

def install_packages_arch(packages):
    assert isinstance(packages, list)
    run(["pacman", "-Syu", "--needed"] + packages)

def install_packages_fedora(packages):
    assert isinstance(packages, list)
    run(["dnf", "install"] + packages)

def install_packages_ubuntu(packages):
    assert isinstance(packages, list)
    run(["apt", "install"] + packages)

def create_symlink_windows(src, dst):
    run(["cmd", "/c", "mklink /d " + dst + " " + src])

def install_fonts():
    fonts_url = "https://github.com/ryanoasis/nerd-fonts/releases/download/v2.2.2/FiraMono.zip"

    if name == 'nt':
        run(["curl", "-fkLo", TEMP + "\\fonts.zip", fonts_url])
        if not isdir(TEMP + "\\fonts"):
            makedirs(TEMP + "\\fonts")

        run(["unzip", TEMP + "\\fonts.zip", "-d", TEMP + "\\fonts"])

        fonts = listdir(TEMP + "\\fonts")
        for f in fonts:
            fupper = f.upper()
            if not (fupper.endswith(".MD") or fupper.endswith(".TXT")):
                run(["cmd", "/c", TEMP + "\\fonts\\" + f])
    elif name == 'posix':
        if not isfile(HOME + "/.cache/fonts.zip"):
            run(["wget",
                 fonts_url,
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
                fupper = f.upper()
                if not fupper.endswith(".MD") or fupper.endswith(".TXT"):
                    copy(HOME + "/.cache/fonts/" + f, "/usr/share/fonts/" + f)
    else:
        print("ERROR: Unsupported platform", file=stderr)
        exit(1)

def install_linux_shell():
    # Install zsh-syntax-highlighting
    ZSH_SH_PATH = f"{HOME}/.zshsh"
    if not isdir(ZSH_SH_PATH) and not isfile(ZSH_SH_PATH):
        run(["wget", "https://github.com/zsh-users/zsh-syntax-highlighting/archive/refs/tags/0.7.1.tar.gz", "-O", f"{HOME}/.cache/a.tar.gz"])
        run(["tar", "-axvf", f"{HOME}/.cache/a.tar.gz", "-C", f"{HOME}/.cache"])
        move(f"{HOME}/.cache/zsh-syntax-highlighting-0.7.1", ZSH_SH_PATH)

        # backup .bashrc
        move(f"{HOME}/.bashrc", f"{HOME}/.bashrc.bak")

        # Install zsh-autosuggestions
        ZSH_AS_PATH = f"{HOME}/.zshas"
        if not isdir(ZSH_AS_PATH) and not isfile(ZSH_AS_PATH):
            run(["git", "clone", "--depth=1", "https://github.com/zsh-users/zsh-autosuggestions.git", ZSH_AS_PATH])

        # Install powerlevel0k
        run(["git", "clone", "--depth=1", "https://github.com/romkatv/powerlevel10k.git", f"{HOME}/.powerlevel10k"])

def install_linux_dotfiles():
    run(["stow", "."])

def install_windows_dotfiles():
    create_symlink_windows(abspath(".\\.config\\emacs"), APPDATA + "\\.emacs.d")
    create_symlink_windows(abspath(".\\.config\\nvim"),
                           abspath(APPDATA + "\\..\\Local\\nvim"))

if name == 'posix':
    if getenv("USER") != "root":
        run(["sudo", "python", __file__] + argv[1:])
        exit(0)
elif name == 'nt':
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        print("ERROR: This script must be run as administrator", file=stderr)
        exit(1)
else:
    print("ERROR: Unsupported platform", file=stderr)
    exit(1)

def usage(stream):
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

if len(argv) < 2:
    print("ERROR: No subcommand was provided", file=stderr)
    usage(stderr)
    exit(1)

if argv[1] == "help":
    usage(stdout)
    exit(0)
elif argv[1] == "windows":
    install_fonts()
    install_windows_dotfiles()
elif argv[1] == "linux":
    if len(argv) < 3:
        print("ERROR: No distribution was provided", file=stderr)
        usage(stderr)
        exit(1)
    if argv[2] == "arch":
        install_packages_arch(get_programs_from_packagestxt("packages.arch.txt"))
    elif argv[2] == "archwm":
        install_packages_arch(get_programs_from_packagestxt("packages.arch.txt"))
        install_packages_arch(get_programs_from_packagestxt("packages.archwm.txt"))
    elif argv[2] == "fedora":
        install_packages_fedora(get_programs_from_packagestxt("packages.fedora.txt"))
    elif argv[2] == "ubuntu":
        install_packages_ubuntu(get_programs_from_packagestxt("packages.ubuntu.txt"))
    else:
        print(f"ERROR: Unsupported distribution: `{argv[2]}`", file=stderr)
        usage(stderr)
        exit(1)

    install_fonts()
    install_linux_shell()
    install_linux_dotfiles()
else:
    print(f"ERROR: Unknown subcommand: `{argv[1]}`", file=stderr)
    usage(stderr)
    exit(1)
