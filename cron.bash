#!/bin/bash
git fetch
git pull --ff-only origin master
python3 update_hosts_file.py -u -v
python3 update_hosts_file.py -l amp-hosts -u -v
python3 update_hosts_file.py -l tracking-aggressive -u -v
git add ads-and-tracking-extended.txt tracking-aggressive-extended.txt amp-hosts-extended.txt
git commit -m "Automatic list update"

