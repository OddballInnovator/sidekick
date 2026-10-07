#!/bin/bash
# 8x timelapse for build montages and the overnight run.
# Usage: ./timelapse.sh in.mp4 out.mp4
# No audio under timelapse; narration is laid over in assembly.
set -e
ffmpeg -i "$1" -vf "setpts=0.125*PTS" -r 30 -an "$2"
