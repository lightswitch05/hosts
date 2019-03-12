#!/bin/bash
git fetch
git checkout .
git checkout automatic-updates
git pull
git pull --ff-only origin master
python3 update_hosts_file.py -u -v
python3 update_hosts_file.py -l amp-hosts -u -v
python3 update_hosts_file.py -l tracking-aggressive -u -v
git add *extended.txt docs/lists/*extended.txt
git commit -m "Automatic list update"
git push

