#!/bin/bash

ABS=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source $ABS/checkparams.lib

if [ "$1" == 'check' ]; then
	file=$2
	ret=$(checkParam_ExistingFile $file)
	for forme in PKCS8; do 
		ssh-keygen -f pem -i -m $forme &>/dev/null
		if [ $? -eq 0 ]; then exit 0; fi
	done
	exit 1
else
	filesrc=$1
	filedest=$2
	if [ -z "$filedest" ]; then filedest=/dev/stdout; fi
	ret=$(checkParam_ExistingFile "$filesrc" 'source' && checkParam_NotExistingFile "$filedest" 'destination')
	if [ "$ret" == "" ]; then
		for forme in PKCS8; do 
			ssh-keygen -f pem -i -m $forme > $filedest
		done
		exit $?
	else
		echo "erreur: $ret"
		exit 1
	fi
fi
