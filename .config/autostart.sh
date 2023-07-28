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

if pgrep bspwm ; then
    run nitrogen --restore
fi
