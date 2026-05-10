#!/bin/bash

if [ "$1"x = 100x ]; then
  runs="20 21 23 24 25 26 27 28 29"
elif [ "$1"x = 80x ]; then
  runs="37 38 39 40 41 42 43 44 45"
elif [ "$1"x = 60x ]; then
  runs="46 47 48 49 50 51 52 53 54"
elif [ "$1"x = "40"x ]; then
  runs="55 56 57 58 59 60 61 62 64"
elif [ "$1"x = 20x ]; then
  runs="65 66 67 68 69 70 71 72 73"
elif [ "$1"x = 20bx ]; then
  runs="74 75 76 77 78 79 80 81 82"
elif [ "$1"x = 40bx ]; then
  runs="86 87 88 89 90 91 92 93 94"
elif [ "$1"x = 60bx ]; then
  runs="95 96 97 98 99 100 101 102 103"
elif [ "$1"x = "80b"x ]; then
  runs="104 105 106 107 108 109 110 111 112"
elif [ "$1"x = 100bx ]; then
  runs="113 114 115 116 117 118 119 120 121"
elif [ "$1"x = 20cx ]; then
  runs="251"
fi

rm -f resolution_$1"GeV.dat"

for i in $(seq 1 1); do

  echo "Running count " $i

  python3.9 GBDT.py -r $runs -o _allruns_$1"GeV" -v xwc0 ywc0 t0_1 t1_1 t2_1 t3_1 t0_5 t1_5 t2_5 t3_5 t0_9 t1_9 t2_9 t3_9 max0 max1 max2 max3 -t32

#  python3.9 GBDT.py -r $runs -o _allruns_$1"GeV" -v t0_5 t1_5 t2_5 t3_5 -t32

  root -l -q calctime.C\(\"allruns_$1"GeV.dat"\"\)

  cat resolution.txt >> resolution_$1"GeV.dat" 

done
