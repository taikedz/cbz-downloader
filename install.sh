#!/bin/bash

set -e

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
