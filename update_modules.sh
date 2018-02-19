update_modules() {
	libdir="$1"

	rsync -a "$thisdir/modules/" "$libdir/modules/"
	echo "Modules deployed."
}

main() {
	bindir="$(dirname "$(which cbzdl)")"
	libdir="$(dirname "$bindir")/lib/cbzdl"
	thisdir="$(dirname "$0")"

	update_modules "$libdir"
}

if [[ "$(basename "$0")" = "update_modules.sh" ]]; then
	main "$@"
fi
