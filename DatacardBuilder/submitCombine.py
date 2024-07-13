import os,sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
from common import get_options, fprint

jdl_template='''universe = vanilla
Executable = ../jobExecCondorRC.sh
+REQUIRED_OS = "rhel7"
+DesiredOS = REQUIRED_OS
request_disk = 1000000
request_memory = 6000
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = ../jobExecCondorRC.sh, {0}.tar.gz, ../stageOut.sh, input/args_{2}_part$(Process).txt, {4}
Output = {2}_$(Process)_$(Cluster).stdout
Error = {2}_$(Process)_$(Cluster).stderr
Log = {2}_$(Process)_$(Cluster).condor
notification = Never
x509userproxy = $ENV(X509_USER_PROXY)
Arguments = {0} {1} {2} $(Process)
on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)
on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)
on_exit_hold_reason = strcat("Job held by ON_EXIT_HOLD due to ",\\
	ifThenElse((ExitBySignal == True), "exit by signal", \\
				strcat("exit code ",ExitCode)), ".")
Queue {3}

'''

includes = [
	"makeDatacards.py",
	"runCombine.py",
	"runJob.py",
	"singleBin.py",
	"cardUtilities.py",
	"searchRegion.py",
	"common.py",
	"SignalMergePeriods.py",
]

if __name__=="__main__":
	options = get_options(jobs=True)

	idfile = TFile.Open("root://cmseos.fnal.gov//store/user/lpcpmssm/SLHATrees/{}.root".format(options.set))
	idtree = idfile.Get("mcmc")
	nmodels = idtree.GetEntries()
	njobs = nmodels/options.split
	if nmodels % options.split != 0: njobs += 1
	firsts = [i*options.split for i in range(njobs)]

	os.chdir("batch")
	argdir = "jobs/input"
	if not os.path.isdir(argdir):
		os.makedirs(argdir,exist_ok=True)
	jobname = "rc_{}".format(options.set)
	for i,first in enumerate(firsts):
		ijobname = "{}_part{}".format(jobname,i)
		with open("{}/args_{}.txt".format(argdir,ijobname),'w') as afile:
			afile.write(
				"--sigDir {} --params {} -1 -1 --firstJob {} --split {}".format(
					options.sigDir,
					options.set,
					first,
					options.split,
				)
			)

	jdlname = "jobExecCondorRC_{}.jdl".format(options.set)
	with open("jobs/"+jdlname,'w') as jfile:
		jfile.write(
			jdl_template.format(
				os.getenv("CMSSW_VERSION"),
				options.sigDir,
				jobname,
				njobs,
				', '.join(["../../"+inc for inc in includes]),
			)
		)

	if options.dryRun:
		fprint("{} jobs".format(len(firsts)))
		sys.exit(0)

	cmd = "cd jobs; condor_submit {}".format(jdlname)
	fprint(cmd)
	os.system(cmd)
