# Mangafox Compiler

Download full mangas from mangafox.

## Requirements

Written with Ubuntu users in mind

Should also work on Windows using Cygwin

May work on BSD/macOS/UNIX but I cannot guarantee this in the slightest...

## Install

Run the install script

	./install

## Usage

Run the `mfcom` command with the URL to any mangafox manga main page

For example

	MFCOM_MAKE_ARCHIVE=cbz # optional - make a CBZ file

	mfcom 'http://mangafox.me/manga/stop_time/' 3 5

First argument is the URL to the manga main page

Second argument is the start index

Third argument is the end index; requires start index to have been specified

## Known issues

Numbering does not follow chapter numbers; instead it uses the entry order number from the list of chapters (to be fixed soon)

