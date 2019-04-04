#!/bin/bash
git fetch
git checkout .
git checkout automatic-updates
git pull
git pull --ff-only origin master
EVEN_DAY=$((($(date +%u)+0)%2))
if [ $EVEN_DAY -eq 0 ];
then
    echo "Updating primary list"
    python3 update_hosts_file.py -u -v
else
    echo "Updating secondary lists"
    python3 update_hosts_file.py -l amp-hosts -u -v
    python3 update_hosts_file.py -l tracking-aggressive -u -v
fi
git add *extended.txt docs/lists/*extended.txt
git commit -m "Automatic list update"
git push

