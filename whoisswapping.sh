#!/bin/bash

for proc in /proc/[0-9]*; do   awk '/VmSwap/ { print $2 "\t'`readlink $proc/exe | awk '{ print $1 }'`'" }' $proc/status; done | sort -n | awk '{ total += $1 ; print $0 } END { print total "\tTotal" }' | tail -10
