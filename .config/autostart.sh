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
run udiskie -t
run dex -a
run picom

if pgrep bspwm ; then
    run nitrogen --restore
    run polybar
    run caffeine
    xsetroot -cursor_name left_ptr
    pgrep -x sxhkd > /dev/null || sxhkd -c ~/.config/sxhkd/sxhkdrc ~/.config/sxhkd/keys.conf &
fi

if pgrep dwm ; then
    run nitrogen --restore
    run caffeine
    pgrep -x sxhkd > /dev/null || sxhkd -c ~/.config/sxhkd/sxhkdrc ~/.config/sxhkd/keys.conf &
fi
