#!/bin/bash
git fetch
git checkout ./**/*.txt *.txt ./docs/index.html
git checkout automatic-updates
git pull
git pull --ff-only origin master
LIST_TYPE=$1

if [ "$LIST_TYPE" == "primary" ]; then
    echo "Updating primary list"
    python3 update_hosts_file.py -u -v
elif [ "$LIST_TYPE" == "secondary" ]; then
    echo "Updating secondary lists"
    python3 update_hosts_file.py -l amp-hosts -u -v
    python3 update_hosts_file.py -l tracking-aggressive -u -v
    python3 update_hosts_file.py -l facebook -u -v
else
    echo "Unknown list time, please supply either 'primary' or 'secondary'"
fi

git add *extended.txt docs/lists/*extended.txt docs/index.html
git commit -m "Automatic list update"
git push
