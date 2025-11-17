#!/bin/bash

for folder in ../data/*; do
    cd "$folder" > /dev/null
    rm *.ply > /dev/null 2>&1
    cd -  > /dev/null
done

