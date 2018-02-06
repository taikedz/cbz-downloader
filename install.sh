#!/bin/bash

thisdir="$(dirname "$0")"
bindir="$HOME/.local/bin"
libdir="$HOME/.local/lib"

if [[ "$UID" = 0 ]]; then
	bindir=/usr/local/bin
	libdir=/usr/local/lib
else
	mkdir -p "$bindir"
	mkdir -p "$libdir"
fi

cp "$thisdir/bin/mfcom" "$thisdir/bin/comicarchive" "$bindir"
cp -r "$thisdir/assets" "$libdir/mfcom"

echo "Done."
