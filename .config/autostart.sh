#!/bin/bash

function run {
    if ! pgrep $1 ;
    then
        $@&
    fi
}

run dunst
run pulseaudio --start
run fcitx-autostart
run udiskie
run dex -a

gnome_schema=org.gnome.desktop.interface
cursor_theme=macOS-Monterey

hyprctl setcursor macOS-Monterey 24
gsettings set $gnome_schema gtk-theme 'Qogir-Dark'
gsettings set $gnome_schema icon-theme 'Qogir-Dark'
gsettings set $gnome_schema cursor-theme $cursor_theme
