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
