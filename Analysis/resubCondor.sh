#!/bin/bash

#assumptions in this script:
#all .jdl and .condor files are in the same directory, JOBDIR
#all .jdl files are named jobExecCondor_JOBNAME.jdl
#all .condor files are named JOBNAME_$(Cluster)_$(Process).condor
#one .jdl file per JOBNAME (i.e. only "Queue 1" is used)

JOBDIR=$1
TIME=$2
OUTNAME=$3

#default is beginning of time
if [ -z "$TIME" ]; then
	#old default was 24 hrs ago
	#TIME=$(date "--date=$(date) -1 day" +"%Y-%m-%d %H:%M")
	TIME="1970-01-01 00:00"
fi

#default is resub.sh
if [ -z "$OUTNAME" ]; then
	OUTNAME="resub.sh"
fi

#setup resub script
echo "#!/bin/bash" > ${OUTNAME}
echo "" >> ${OUTNAME}
echo "cd ${JOBDIR}" >> ${OUTNAME}

#keep track of jobs that have been checked
joblist=""

#search for "return value" in condor logs newer than TIME - denotes finished job
for file in $(grep -lw "return value" $(find ${JOBDIR}/*.condor -newermt "${TIME}")); do
	#skip job if it finished successfully - return value 0
	success=$(grep -lw "return value 0" ${file})
	if [[ -n "$success" ]]; then
		continue
	fi
	
	base=$(echo $(basename ${file}) | rev | cut -d'_' -f1-2 --complement | rev)
	
	#skip job if it has already been checked
	if [[ "$joblist" == *$base* ]]; then
		continue
	fi
	
	#check for newer logs that succeeded
	newerfiles=$(find ${JOBDIR}/${base}*.condor -newer "${file}")
	newerstatus=""
	if [ -n "$newerfiles" ]; then
		newerstatus=$(grep -lw "return value 0" ${newerfiles})
	fi
	
	#if none were found, the job failed
	if [ -z "$newerstatus" ]; then
		#optional: output return value for failed job as comment in resub script
		#echo "#"$(grep -w "return value" ${file}) >> ${OUTNAME}
		echo "condor_submit jobExecCondor_${base}.jdl" >> ${OUTNAME}
	fi
	
	#append jobname to list
	joblist="${base} ${joblist}"
done
  
echo "cd -" >> ${OUTNAME}

echo "Job resubmission script created: ${OUTNAME}"
chmod +x ${OUTNAME}
