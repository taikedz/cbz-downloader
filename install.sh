#!/bin/bash

set -e
is_termux() {
	which termux-info 2>/dev/null >/dev/null
}

pipcmd=pip3

# Termux is a GNU/Linux sub-environment for Android
if is_termux ; then
	apt update && apt install python clang libxml2-dev libxslt-dev python-dev rsync

	pipcmd=pip

	# cbzdl is pretty useless if we can't put the files in an accessible location
	if [[ ! -d "$HOME/storage" ]]; then
		echo "Setting up storage access - you may want to download your files into ~/storage/downloads/ when operating"
		termux-setup-storage
	fi
fi

thisdir="$(dirname "$0")"
bindir="$HOME/.local/bin"
libdir="$HOME/.local/lib"

if [[ "$UID" = 0 ]]; then
	bindir=/usr/local/bin
	libdir=/usr/local/lib
fi

if is_termux; then
	echo "lxml compilation may take a while (maybe even 10min or more!) on Android devices ..."
fi
PATH="$libdir:$PATH" "$pipcmd" install -r requirements.txt

echo "Creating bin and lib directories ..."

mkdir -p "$bindir"
mkdir -p "$libdir"

echo "Copying files ..."

rsync -a "$thisdir/cbzdl/" "$libdir/cbzdl/"
if [[ ! -e "$bindir/cbzdl" ]]; then
	ln -s "$libdir/cbzdl/main.py" "$bindir/cbzdl"
fi
chmod 755 "$libdir/cbzdl/main.py"

echo "Installed cbzdl."
