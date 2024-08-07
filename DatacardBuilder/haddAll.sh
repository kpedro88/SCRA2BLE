#!/bin/bash

ARGS="$1"

SETS=(
set1LL \
set1prompt1 \
set1prompt2 \
set1prompt3 \
set2LL1 \
set2LL2 \
set2prompt1 \
set2prompt2 \
)

for SET in ${SETS[@]}; do
	echo $SET
	./batch/haddEOS.sh -i results_${SET} -x root://cmseos.fnal.gov/ -d /store/user/lpcpmssm/Datacards/Run2ProductionV17_v1 -g _part $ARGS -r
done
