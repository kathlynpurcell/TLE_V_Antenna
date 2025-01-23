#!/bin/bash

source tle_env/bin/activate

inotifywait -e create -e move -r -m /raid/scratch/cyborg/GBOdata
    while read path action file; do
        echo "Checking the new file is fits, check for SV later..."
        if [[ "$file" =~ .*fits$ ]]; then # Does the file end with .fits?
            echo "Running TLE_v_Antenna for: "$file
            #python TLE_V_Antenna.py -f $path$file -t SV160_TLE
            python /raid/20m/lib/python/skycode/cyborg/TLE_V_Antenna.py -f $file -dd $path
        fi
    done

deactivate