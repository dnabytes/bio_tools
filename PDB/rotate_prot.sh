#!/bin/bash
if [ ! -f "$2" ]; then
    printf "usage:\n  rotate_prot coordinates filename.pdb\n"
    exit
fi
awk -v UT="$1" 'BEGIN {split(UT, arr, ",")} {
    if ($0 ~ /^ATOM|^HETATM/) {
        x = $7
        y = $8
        z = $9
        x_new = (x * arr[1] + y * arr[2] + z * arr[3]) + arr[10]
        y_new = (x * arr[4] + y * arr[5] + z * arr[6]) + arr[11]
        z_new = (x * arr[7] + y * arr[8] + z * arr[9]) + arr[12]
        printf "%-6s%5d  %-4s%3s %s%4d    %8.3f%8.3f%8.3f%6.2f%6.2f          %2s\n", $1, $2, $3, $4, $5, $6, x_new, y_new, z_new, $11, $12, $13
    }
    else {
        print $0
    }
}' "$2" > rot_"$2"
