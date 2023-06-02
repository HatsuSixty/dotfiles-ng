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
cursor_theme=Adwaita-smol

hyprctl setcursor $cursor_theme 24
gsettings set $gnome_schema gtk-theme 'adw-gtk3-dark'
gsettings set $gnome_schema icon-theme 'Adwaita'
gsettings set $gnome_schema cursor-theme $cursor_theme
