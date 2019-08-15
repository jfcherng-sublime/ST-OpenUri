#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PNG_SIZE=48

SOURCE_DIRS=(
    "FontAwesome"
)

pushd "${SCRIPT_DIR}" || exit

for source_dir in "${SOURCE_DIRS[@]}"; do
    pushd "${source_dir}" || exit

    for svg_file in *.svg; do
        png_file=${svg_file%.*}.png

        rm -f "${png_file}"
        svg2png "${svg_file}" -w "${PNG_SIZE}" -h "${PNG_SIZE}" -o "${png_file}"
    done

    popd || exit
done

popd || exit
