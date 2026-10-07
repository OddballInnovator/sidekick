#!/bin/bash
# Assemble the Sidekick film: picture + VO.
# Each act's visuals are stretched/looped to match its VO track duration.
set -e
cd "$(dirname "$0")"

# VO durations (seconds): act1 19.08, act2 14.64, act3 29.11, act4 11.28, act5 48.53, closing 4.99
# Visual mapping:
#   Act1 -> s1-needs (loop to 19s)
#   Act2 -> s2-arch (loop to 14.6s)
#   Act3 -> s3-compare (loop to 29s)
#   Act4 -> s4-build (loop to 11.3s)
#   Act5 -> s5-chat (6s) + s6-joblog (3s) + s7-briefing (2s), then hold s7 to fill 48.5s
#   Closing -> s9-endcard (5s)

mk() { # $1=out $2=dur $3..=inputs (concat, looped to fill)
  local out=$1 dur=$2; shift 2
  local inputs=() filters=""
  local i=0
  for f in "$@"; do inputs+=(-i "$f"); filters+="[${i}:v]settb=AVTB,fps=30[v${i}];"; i=$((i+1)); done
  local concat=""
  for ((j=0;j<i;j++)); do concat+="[v${j}]"; done
  # tpad holds the last frame to reach the target duration
  ffmpeg -y -v error "${inputs[@]}" -filter_complex \
    "${filters}${concat}concat=n=${i}:v=1:a=0,scale=1920:1080,tpad=stop=-1:stop_mode=clone:stop_duration=${dur},trim=duration=${dur},format=yuv420p" \
    -r 30 "$out"
}

echo "building act clips..."
mk takes/act1.mp4 19.08 takes/s1-needs.mp4
mk takes/act2.mp4 14.64 takes/s2-arch.mp4
mk takes/act3.mp4 29.11 takes/s3-compare.mp4
mk takes/act4.mp4 11.28 takes/s4-build.mp4
mk takes/act5.mp4 48.53 takes/s5-chat.mp4 takes/s6-joblog.mp4 takes/s7-briefing.mp4
mk takes/closing.mp4 4.99 takes/s9-endcard.mp4

echo "concatenating picture..."
ffmpeg -y -v error -i takes/act1.mp4 -i takes/act2.mp4 -i takes/act3.mp4 \
  -i takes/act4.mp4 -i takes/act5.mp4 -i takes/closing.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v][4:v][5:v]concat=n=6:v=1:a=0,format=yuv420p" \
  -r 30 takes/picture.mp4

echo "mixing audio..."
ffmpeg -y -v error -i audio/act1.mp3 -i audio/act2.mp3 -i audio/act3.mp3 \
  -i audio/act4.mp3 -i audio/act5.mp3 -i audio/closing.mp3 \
  -filter_complex "[0:a][1:a][2:a][3:a][4:a][5:a]concat=n=6:v=0:a=1" \
  audio/vo-mix.mp3

echo "muxing final..."
ffmpeg -y -v error -i takes/picture.mp4 -i audio/vo-mix.mp3 \
  -c:v libx264 -preset medium -crf 20 -c:a aac -shortest \
  sidekick-film.mp4

echo "DONE: sidekick-film.mp4"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 sidekick-film.mp4
