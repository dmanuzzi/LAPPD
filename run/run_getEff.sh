#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1_LHCB_7/x86_64-centos7-gcc11-opt/setup.sh
run=$1
tag=$2
outdir="../out_getEff/run${run}${tag}"
rm -rf  ${outdir}
mkdir -p ${outdir}
cd ${outdir}



root -l -q -b ../../src/getEff.cpp\("${run}"\)

#cat resolution.txt >> "resolution_${tag}.dat" 

