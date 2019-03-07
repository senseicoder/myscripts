#!/bin/bash

function cntip
{
	local name=$1

	IP=$(docker inspect $name | grep IPAd | awk -F'"' '{print $4}'| uniq | xargs)
	echo $IP
}
