# Mangafox Compiler

Download full mangas from mangafox.

## Requirements

Written with Ubuntu users in mind

Should also work on any GNU/Linux
	* Debian
	* Fedora
	* Arch
	* etc ...

Probably works on Windows using Cygwin and the appropriate standard GNU tools. Note that you will need `zip` command to create Comic Book Archive (cbz) files

May work on BSD/macOS/UNIX but I cannot guarantee this in the slightest...

## Install

Run the install script

	./install

This installs to ~/.local/bin for the current user. To install for all users, run

	sudo ./install

## Usage

Run the `mfcom` command with the URL to any mangafox manga main page

For example

	MFCOM_MAKE_ARCHIVE=cbz # optional - make a CBZ file

	# Download pages 3 and 4 of the manga
	mfcom 'http://mangafox.me/manga/stop_time/' 3 5

First argument is the URL to the manga main page; it can also be the folder where previous downloads have been stored.

	# Download page 5 of the manga
	mfcom stop_time/ 5 6

Second argument is the start index

Third argument is the end index; requires start index to have been specified. The third index can also be "+" followed by the number of pages to download

	# Download pages 3 and 4 (2 pages)
	mfcom 'http://mangafox.me/manga/stop_time/' 3 +2
