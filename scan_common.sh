#!/bin/bash

# doc
# http://www.konradvoelkel.com/2013/03/scan-to-pdfa/
# http://crunchbang.org/forums/viewtopic.php?id=13875

function doscan()
{
	local tiff=/tmp/scan.tiff
	local file=$1

	rm -f $tiff $file
	scanimage --progress --resolution=300 > $tiff
	convert $tiff $file
	rm -f $tiff 
	pdfsmall $file > /dev/null
}

function checkfile()
{
	local file=$1
	local final=$2

	echo "regardez le fichier, et fermez la fenêtre pour continuer"
	evince $file

	PS3='Fichier correct ? > '   # le prompt
	LISTE=("[o]ui" "[n]on")  # liste de choix disponibles
	select CHOIX in "${LISTE[@]}" ; do
		case $REPLY in
			1|o) mv $file $final; exit 0; break;;
			2|n) echo "on recommence"; break;;
		esac
	done
}