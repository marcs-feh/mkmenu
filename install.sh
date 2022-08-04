#!/bin/sh

INSTALL_DIR="$HOME/.local/bin"

Install(){
	echo "Installing."
	mkdir -p "$INSTALL_DIR"
	cp mkmenu.py "$INSTALL_DIR/mkmenu"
	chmod 755 "$INSTALL_DIR/mkmenu"
}

Uninstall(){
	echo "Uninstalling."
	rm -f "$INSTALL_DIR/mkmenu"
}

if [ "$1" = "i" ]; then
	Install
elif [ "$1" = "u" ]; then
	Uninstall
else
	printf "Options:\n\ti\tinstall\n\tu\tuninstall\n"
fi
