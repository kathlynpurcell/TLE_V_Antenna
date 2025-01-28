#!/bin/bash

#source /raid/20mversions/venvs/tle_env/bin/activate

inotifywait -e create -e move -r -m /raid/scratch/cyborg/GBOdata |
    while read path action file; do
        echo "Checking the new file is fits, check for SV later..."
        if [[ "$path" =~ "Antenna" ]]; then
            if [[ "$file" =~ .*fits$ ]]; then # Does the file end with .fits?
                echo "Running TLE_v_Antenna for: "$file
                #python TLE_V_Antenna.py -f $path$file -t SV160_TLE
                echo "Wait for scan to complete..."
                export file_size_start=0
                export file_size=$(stat --printf="%s" $path$file)
                while [ $file_size -gt $file_size_start ]; do
                    sleep 10
                    export file_size_start=$file_size
                    export file_size=$(stat --printf="%s" $path$file)
                done
                export PYTHONPATH="/opt/local/bin/python3"
                python /raid/20m/lib/python/skycode/cyborg/TLE_V_Antenna.py -f $file -dd $path
            fi
        fi
    done

deactivate
