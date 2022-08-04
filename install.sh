#!/bin/sh

INSTALL_DIR="~/.local/bin"

Install(){
    mkdir -p "$INSTALL_DIR"
    cp mkmenu.py "$INSTALL_DIR/mkmenu"
    chmod 755 "$INSTALL_DIR/mkmenu"
}

Uninstall(){
    rm -f "$INSTALL_DIR/mkmenu"
}

if [ "$1" = "i" ]; then
    Install
elif [ "$1" = "u" ]; then
    Uninstall
else
    printf "Options:\n\ti\tinstall\n\tu\tuninstall"
fi