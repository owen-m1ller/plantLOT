#!/bin/bash

input_file="$1"
zmin=5

num_pts=$(awk -v zmin="$zmin" '($3 >= zmin) {count++} END {print count+0}' "$input_file")

output_file=$(echo "$input_file" | sed 's/\(_a\)\?\.txt$/.ply/')

cat > "$output_file" <<EOF
ply
format ascii 1.0
element vertex $num_pts
property float x
property float y
property float z
end_header
EOF

awk -v zmin="$zmin" '($3 >= zmin) {
    printf "%.6f %.6f %.6f\n", $1+47, $2+739, $3
}' "$input_file" >> "$output_file"

