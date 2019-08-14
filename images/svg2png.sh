#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
THREAD_CNT=$(getconf _NPROCESSORS_ONLN)
PNG_SIZE=48

pushd "${SCRIPT_DIR}" || exit

for svg_file in *.svg; do
    png_file=${svg_file%.*}.png

    rm -f "${png_file}"
    svg2png "${svg_file}" -w "${PNG_SIZE}" -h "${PNG_SIZE}" -o "${png_file}"
done

popd || exit
