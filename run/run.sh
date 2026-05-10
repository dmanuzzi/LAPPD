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
elif [[ $runTag == *"SPS2023center800V"* ]]; then
    if [ "$energy"x = 100x ]; then
		runs="20"
    elif [ "$energy"x = 80x ]; then
		runs="37"
    elif [ "$energy"x = 60x ]; then
		runs="46"
    elif [ "$energy"x = 40x ]; then
		runs="55"
    elif [ "$energy"x = 20x ]; then
		runs="65"
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
	fi
elif [[ $runTag == *"SPS2023center825V"* ]]; then
    if [ "$energy"x = 20x ]; then
		runs="82"
    elif [ "$energy"x = 40x ]; then
		runs="86"
    elif [ "$energy"x = 60x ]; then
		runs="95"
    elif [ "$energy"x = 80x ]; then
		runs="104"
    elif [ "$energy"x = 100x ]; then
		runs="113"
	fi
elif [[ $runTag == *"SPS2023center875V"* ]]; then
    if [ "$energy"x = 20x ]; then
		runs="123"
    fi;
elif [[ $runTag == "SPS2023center685V3mcp" ]]; then
    if [ "$energy"x = 100x ]; then
		runs="16"
    fi;
elif [[ $runTag == "SPS2023center685V3mcpLEDinhib500kHz" ]]; then
    if [ "$energy"x = 20x ]; then
		runs="188"
    elif [ "$energy"x = 40x ]; then
		runs="185"
    elif [ "$energy"x = 60x ]; then
		runs="182"
    elif [ "$energy"x = 80x ]; then
		runs="179"
    elif [ "$energy"x = 100x ]; then
		runs="175"
	fi
elif [[ $runTag == *"SPS2023center685V3mcpLEDinhib1MHz"* ]]; then
    if [ "$energy"x = 20x ]; then
		runs="209"
    elif [ "$energy"x = 40x ]; then
		runs="206"
    elif [ "$energy"x = 60x ]; then
		runs="203"
    elif [ "$energy"x = 80x ]; then
		runs="200"
    elif [ "$energy"x = 100x ]; then
		runs="197"
	fi
elif [[ $runTag == *"SPS2023center685V3mcpLEDinhib5MHz"* ]]; then
    if [ "$energy"x = 20x ]; then
		runs="227"
    elif [ "$energy"x = 40x ]; then
		runs="224"
    elif [ "$energy"x = 60x ]; then
		runs="221"
    elif [ "$energy"x = 80x ]; then
		runs="218"
    elif [ "$energy"x = 100x ]; then
		runs="212"
	fi
elif [[ $runTag == *"SPS2023center685V3mcpLEDinhib20MHz"* ]]; then
    if [ "$energy"x = 20x ]; then
		runs="246"
    elif [ "$energy"x = 40x ]; then
		runs="243"
    elif [ "$energy"x = 60x ]; then
		runs="238"
    elif [ "$energy"x = 80x ]; then
		runs="235"
    elif [ "$energy"x = 100x ]; then
		runs="230"
	fi
elif [[ $runTag == *"SPS2023center685V3mcpLEDinhibAllRates"* ]]; then
    if [ "$energy"x = 20x ]; then
		runs="188 209 227 246"
    elif [ "$energy"x = 40x ]; then
		runs="185 206 224 243"
    elif [ "$energy"x = 60x ]; then
		runs="182 203 221 238"
    elif [ "$energy"x = 80x ]; then
		runs="179 200 218 235"
    elif [ "$energy"x = 100x ]; then
		runs="175 197 212 230"
	fi

else
    runs=${runTag//'run'/''}
fi

echo runs $runs
tag="${runTag}_${energy}GeV_${Ntrees}_${maxLeaves}_${bootstrap}_${maxSamples}_${maxFeatures}${opt}"
echo $tag
mkdir -p ../out/${tag}
cd ../out/${tag}


rm -f "./output*.dat"
rm -f "./resolution*.dat"
rm -f "./resolution.txt"


python3.9 ../../src/GBDT.py -r $runs -o $tag -t $Ncpus \
                             -v xwc0 ywc0 t0_1 t1_1 t2_1 t3_1 t0_5 t1_5 t2_5 t3_5 t0_9 t1_9 t2_9 t3_9 max0 max1 max2 max3 \
                             -nt $Ntrees -nl $maxLeaves -ms $maxSamples -b $bootstrap -mf $maxFeatures

root -l -q -b ../../src/calctime.C\(\""${tag}.dat"\"\)
cat resolution.txt >> "resolution_${tag}.dat" 

python3.9 ../../src/get_resT.py -i  output_evalMoreVar_${tag}
python3.9 ../../src/getEff_v2.py -i  output_data_${tag}
