#!/bin/bash

function run {
    if ! pgrep $process ;
    then
        $@&
    fi
}

run dunst
run pulseaudio --start
run fcitx-autostart
run udiskie

gnome_schema=org.gnome.desktop.interface

gsettings set $gnome_schema gtk-theme 'Qogir-Dark'
gsettings set $gnome_schema icon-theme 'Qogir-Dark'
