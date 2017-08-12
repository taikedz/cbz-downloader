#!/bin/bash

thisdir="$(dirname "$0")"
bindir="$HOME/.local/bin"

if [[ "$UID" = 0 ]]; then
	bindir=/usr/local/bin
else
	mkdir -p "$bindir"
fi

cp "$thisdir/bin/mfcom" "$bindir"
