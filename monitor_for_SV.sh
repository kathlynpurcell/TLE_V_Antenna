#!/bin/bash

source tle_env/bin/activate

inotifywait -e create -e move -r -m /home/sandboxes/kpurcell/repos/TLE_v_Antenna |
    while read path action file; do
        echo "Checking for fits, check for SV is later..."
        if [[ "$file" =~ .*fits$ ]]; then # Does the file end with .fits?
            echo "Running TLE_v_Antenna for: "$file
            #python TLE_V_Antenna.py -f $path$file -t SV160_TLE
            python TLE_V_Antenna.py -f $file -dd $path
        fi
    done

deactivate