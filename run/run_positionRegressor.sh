#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1_LHCB_7/x86_64-centos7-gcc11-opt/setup.sh

runTag=$1
energy=$2
Ntrees=$3
maxLeaves=$4
bootstrap=$5
maxSamples=$6
maxFeatures=$7
Ncpus=$8
opt=$9
echo $runTag $energy $Ntrees $maxLeaves $Ncpus $opt

if [[ $runTag == *"allRuns"* ]]; then
    if [[ $runTag == *"3mcp"* ]]; then
	if [ "$energy"x = 5x ]; then
	    runs="0 1 3 4 7 8 9 10 11"
	elif [ "$energy"x = 3x ]; then
	    runs="12 13 14 15 16 17 18 19 20"
	elif [ "$energy"x = 1x ]; then
	    runs="21"
	fi;
    else
	if [ "$energy"x = 5x ]; then
	    runs="40 41 42 43 44 45 46 47 48"
	elif [ "$energy"x = 3x ]; then
	    runs="49 50 52 53 58 57 56 55 54"
	elif [ "$energy"x = 4x ]; then
	    runs="70 71 72 73 74 75 76 77 78"
	elif [ "$energy"x = "5.8"x ]; then
	    runs="80"
	elif [ "$energy"x = 1x ]; then
	    runs="69 68 67 64 59 60 61 62 63"
	elif [ "$energy"x = 2x ]; then
	    runs="83 84 85 86 88 89 90 82 79"
	fi;
    fi;
elif [[ $runTag == *"SPS2023allPos800V"* ]]; then
    if [ "$energy"x = 100x ]; then
	runs="20 21 23 24 25 26 27 28 29"
    elif [ "$energy"x = 80x ]; then
	runs="37 38 39 40 41 42 43 44 45"
    elif [ "$energy"x = 60x ]; then
	runs="46 47 48 49 50 51 52 53 54"
    elif [ "$energy"x = 40x ]; then
	runs="55 56 57 58 59 60 61 62 64"
    elif [ "$energy"x = 20x ]; then
	runs="65 66 67 68 69 70 71 72 73"
    fi;
elif [[ $runTag == *"SPS2023allPos825V"* ]]; then
    if [ "$energy"x = 20x ]; then
	runs="74 75 76 77 78 79 80 81 82"
    elif [ "$energy"x = 40x ]; then
	runs="86 87 88 89 90 91 92 93 94"
    elif [ "$energy"x = 60x ]; then
	runs="95 96 97 98 99 100 101 102 103"
    elif [ "$energy"x = 80x ]; then
	runs="104 105 106 107 108 109 110 111 112"
    elif [ "$energy"x = 100x ]; then
	runs="113 114 115 116 117 118 119 120 121"
#    elif [ "$energy"x = 20x ]; then
#	runs="251"
    fi;
else
    runs=${runTag//'run'/''}
fi


echo runs $runs
tag="${runTag}_${energy}GeV_${Ntrees}_${maxLeaves}_${bootstrap}_${maxSamples}_${maxFeatures}${opt}"
echo $tag
mkdir -p ../out_position/${tag}
cd ../out_position/${tag}


# python3.9 ../../src/positionRegressor.py -r $runs -o $tag -t $Ncpus \
#                             -v max0 max1 max2 max3  \
#                             -nt $Ntrees -nl $maxLeaves -ms $maxSamples -b $bootstrap -mf $maxFeatures


# python3.9 ../../src/positionRegressor.py -r $runs -o $tag -t $Ncpus \
#                             -v t0_1 t1_1 t2_1 t3_1 t0_5 t1_5 t2_5 t3_5 t0_9 t1_9 t2_9 t3_9 max0 max1 max2 max3 \
#                             -nt $Ntrees -nl $maxLeaves -ms $maxSamples -b $bootstrap -mf $maxFeatures

# python3.9 ../../src/positionRegressor_flatInput.py -r $runs -o $tag -t $Ncpus \
#                             -v max0 max1 max2 max3  \
#                             -nt $Ntrees -nl $maxLeaves -ms $maxSamples -b $bootstrap -mf $maxFeatures

# python3.9 ../../src/positionRegressor_x.py -r $runs -o $tag -t $Ncpus \
#                             -v max0 max1 max2 max3  area0 area1 area2 area3 \
#                             -nt $Ntrees -nl $maxLeaves -ms $maxSamples -b $bootstrap -mf $maxFeatures

python ../../src/get_resPos.py  -i output_eval_${tag}
