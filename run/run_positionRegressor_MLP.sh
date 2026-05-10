#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1_LHCB_7/x86_64-centos7-gcc11-opt/setup.sh

energy=$1
Ncpus=$2
opt=$3
echo $energy $Ntrees $maxLeaves $Ncpus
tag="allRuns_${energy}GeV${opt}"
echo $tag
mkdir -p ../out_positionRegressor/${tag}
cd ../out_positionRegressor/${tag}
if [ "$1"x = 5x ]; then
#  runs="40"
#  runs="0 1 3 4 7 8 9 10 11"
  runs="40 41 42 43 44 45 46 47 48"
elif [ "$energy"x = 3x ]; then
#  runs="12 13 14 15 16 17 18 19 20"
  runs="49 50 52 53 58 57 56 55 54"
elif [ "$energy"x = 4x ]; then
  runs="70 71 72 73 74 75 76 77 78"
elif [ "$energy"x = "5.8"x ]; then
  runs="80"
elif [ "$energy"x = 1x ]; then
  runs="69 68 67 64 59 60 61 62 63"
elif [ "$energy"x = 2x ]; then
  runs="83 84 85 86 88 89 90 82 79"
fi

# rm -f "./output*.dat"
# rm -f "./resolution*.dat"
# rm -f "./resolution.txt"



python3.9 ../../src/positionRegressor_MLP.py -r $runs -o $tag -t $Ncpus \
                            -v max0 max1 max2 max3 \
                            