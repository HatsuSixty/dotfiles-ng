#!/bin/bash

function run {
    if ! pgrep $1 ;
    then
        $@&
    fi
}

run dunst
run pipewire-pulse 1>&2 > /dev/null
run fcitx-autostart
run udiskie
run dex -a

gnome_schema=org.gnome.desktop.interface
cursor_theme=Adwaita-smol

gsettings set $gnome_schema gtk-theme 'Dracula'
gsettings set $gnome_schema icon-theme 'Adwaita'
gsettings set $gnome_schema cursor-theme $cursor_theme
