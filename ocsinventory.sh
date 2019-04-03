#!/bin/bash
#note: doit être lancé en root

#installation: 
# sudo rm /etc/cron.daily/ocsinventory-agent
# sudo ln -s /home/cedric/bin/public/ocsinventory.sh /etc/cron.hourly/ocsinventory

log=/var/log/epiconcept/ocsinventory.log
okfortheday=/var/run/ocsinventory

if [[ ! -e "$okfortheday" || $(find "$okfortheday" -mtime +1 -print 2>/dev/null) ]]; then
	ping -c1 -w3 $(cat /etc/ocsinventory/ocsinventory-agent.cfg | sed 's/.*=//g') &>/dev/null
	if [ $? -eq 0 ]; then
		echo "$(date +%F:%H:%M:%S);$(ocsinventory-agent 2>&1 | xargs)" >> $log
		rc=$?
		if [ $rc -ne 0 ]; then 
			echo "$(date +%F:%H:%M:%S);error $rc" >> $log
		else
			touch $okfortheday
		fi
	else
		echo "$(date +%F:%H:%M:%S);notavailable" >> $log
	fi
fi