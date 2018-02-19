#!/bin/bash

set -e

# Termux is a GNU/Linux sub-environment for Android
if which termux-info 2>/dev/null >/dev/null ; then
	apt update && apt install python clang libxml2-dev libxslt-dev python-dev

	echo "lxml compilation may take a while (maybe even 10min or more!) on Android devices ..."

	pip install -r requirements.txt

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
echo "Ensure you have lxml (\`[sudo] pip install lxml\`)"
