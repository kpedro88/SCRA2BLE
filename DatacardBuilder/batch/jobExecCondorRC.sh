#!/bin/bash

#
# variables from arguments string in jdl
#

echo "Starting job on " `date` #Only to display the starting of production date
echo "Running on " `uname -a` #Only to display the machine where the job is running
echo "System release " `cat /etc/redhat-release` #And the system release
echo "CMSSW on Condor"

CMSSWVER="$1"
STORE="$2"
JOBNAME="$3"
PROCESS="$4"

echo ""
echo "parameter set:"
echo "CMSSWVER:   $CMSSWVER"
echo "STORE:      $STORE"
echo "JOBNAME:    $JOBNAME"
echo "PROCESS:    $PROCESS"

source stageOut.sh
tar -xzf ${CMSSWVER}.tar.gz
cd ${CMSSWVER}
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram b ProjectRename
# cmsenv
eval `scramv1 runtime -sh`
cd $_CONDOR_SCRATCH_DIR

# run combine
ARGS=$(cat args_${JOBNAME}_part${PROCESS}.txt)
(set -x;
python runJob.py --signal pMSSM --lumi 137.4 --realData $ARGS 2>&1)

PYEXIT=$?

if [[ $PYEXIT -ne 0 ]]; then
	rm *.root
	echo "exit code $PYEXIT from $JOBNAME, skipping xrdcp"
	exit $PYEXIT
fi

# copy output to eos
echo "xrdcp output for condor"
for FILE in results_part*.root; do
	echo "xrdcp -f ${FILE} ${STORE}/${FILE}"
	stageOut -x "-f" -i ${FILE} -o ${STORE}/${FILE}
	XRDEXIT=$?
	if [[ $XRDEXIT -ne 0 ]]; then
		rm *.root
		echo "exit code $XRDEXIT, failure in xrdcp"
		exit $XRDEXIT
	fi
done
rm *.root
