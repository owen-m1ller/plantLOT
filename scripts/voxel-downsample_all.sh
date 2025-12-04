#!/bin/bash

for file in ../data/**/*; do
    if [[ "$file" == *.ply ]]; then
        python voxel-downsample.py "$file" 5
    fi
done

