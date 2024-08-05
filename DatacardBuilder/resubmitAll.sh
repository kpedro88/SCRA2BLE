#!/bin/bash

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
	python submitCombine.py --signal pMSSM --set $SET --sigDir root://cmseos.fnal.gov//store/user/lpcpmssm/Datacards/Run2ProductionV17_v1 --split 1 --missing missing_${SET}.txt
done
