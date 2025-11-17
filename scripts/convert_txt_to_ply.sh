#!/bin/bash

input_file="$1"

num_pts=$(wc -l < "$input_file")

output_file=$(echo "$input_file" | sed 's/\(_a\)\?\.txt$/.ply/')

cat >  "$output_file" <<EOF
ply
format ascii 1.0
element vertex $num_pts
property float x
property float y
property float z
end_header
EOF

awk '{printf "%.6f %.6f %.6f\n", $1+47, $2+739, $3}' "$input_file" >> "$output_file"

