#!/bin/bash

for file in ../data/**/*; do
    if [ -f "$file" ]; then
        if [[ "$file" == *.txt ]]; then
            echo $file
            ./convert_txt_to_ply.sh $file
        fi
    fi
done

