#!/bin/bash

ABS=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
source $ABS/checkparams.lib

if [ "$1" == 'check' ]; then
	file=$2
	ret=$(checkParam_ExistingFile $file)
	if [ "$ret" == "" ]; then
		grep 'BEGIN SSH2 PUBLIC KEY' $file &>/dev/null
		exit $?
	else
		echo "erreur: $ret"
		exit 1
	fi
else
	filesrc=$1
	filedest=$2
	if [ -z "$filedest" ]; then filedest=/dev/stdout; fi
	ret=$(checkParam_ExistingFile "$filesrc" 'source' && checkParam_NotExistingFile "$filedest" 'destination')
	if [ "$ret" == "" ]; then
		ssh-keygen -i -f $filesrc > $filedest
		exit $?
	else
		echo "erreur: $ret"
		exit 1
	fi
fi