#!/bin/bash

set -e

printhelp() {
cat <<EOF

$0 all

	Install pre-requisites, engine, and modules

$0 engine

	Update just the engine

$0 modules

	Update just the modules

EOF
}

hasbin() {
	which "$1" 2>/dev/null >/dev/null
}

is_termux() {
	hasbin termux-setup-storage
}

out:fail() {
	echo "$*"
	exit 1
}

ensure_python3() {
	if is_termux; then return ; fi

	if ! hasbin python3; then
		out:fail "Python 3 not available !"
	fi

	if ! hasbin pip3; then
		out:fail "pip3 not available !"
	fi
}

termux_setup() {
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
}


determine_dirs() {
	bindir="$HOME/.local/bin"
	libdir="$HOME/.local/lib"

	if [[ "$UID" = 0 ]]; then
		bindir=/usr/local/bin
		libdir=/usr/local/lib
	fi
}

ensure_dirs() {
	echo "Creating bin and lib directories ..."

	mkdir -p "$bindir"
	mkdir -p "$libdir"
}

enqueue() {
	QUEUED_MESSAGES="${QUEUED_MESSAGES:-}$(echo -e "$*\n")"
}

flush_queue() {
	echo "${QUEUED_MESSAGES:-}"
	QUEUED_MESSAGES=''
}

path_ensure() {
	if [[ ! "$PATH" =~ "$bindir" ]]; then
		echo "export PATH='$bindir:\$PATH'" >> "$HOME/.bashrc"
		export PATH="$bindir:$PATH"
		enqueue "Please reload your .bashrc"
	fi
}

install_pip_requirements() {
	echo "Installing pip3 requirements"

	if is_termux; then
		echo "lxml compilation may take a while (maybe even 10min or more!) on Android devices ..."
	fi
	PATH="$libdir:$PATH" "$pipcmd" install -r requirements.txt
}

update_modules() {
	rsync -a --exclude="*.swp" "$thisdir/modules/" "$libdir/cbzdl/modules/"
	echo "Modules deployed."
}

update_engine() {
	rsync -a --exclude="*.swp" "$thisdir/engine/" "$libdir/cbzdl/"
	if [[ ! -e "$bindir/cbzdl" ]]; then
		ln -s "$libdir/cbzdl/main.py" "$bindir/cbzdl"
	fi

	chmod 755 "$libdir/cbzdl/main.py"

	echo "Core cbzdl deployed."
}

main() {
	pipcmd=pip3
	thisdir="$(dirname "$0")"
	determine_dirs

	case "${1}" in
	modules|modules/)
		update_modules
		;;
	engine|engine/)
		update_engine
		;;
	all)

		ensure_python3
		termux_setup

		ensure_dirs

		install_pip_requirements

		update_engine
		update_modules

		path_ensure
		flush_queue

		echo "Installed cbzdl."
		;;
	*)
		printhelp
		;;
	esac
}

main "$@"
