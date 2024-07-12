import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
import os,sys,glob,shlex
from common import get_options, fprint
from makeDatacards import makeDatacards
from runCombine import runCombine

if __name__=="__main__":
	argv_orig = sys.argv[:]
	options = get_options(single=True,jobs=True)

	idfile = TFile.Open("root://cmseos.fnal.gov//store/user/lpcpmssm/SLHATrees/{}.root".format(options.set))
	idtree = idfile.Get("mcmc")

	maxJobs = min(options.firstJob+options.split, idtree.GetEntries())
	for entry in range(options.firstJob, maxJobs):
		idtree.GetEntry(entry)
		id1 = idtree.chain_index
		id2 = idtree.iteration_index
		fprint("Processing model: {} {}".format(id1,id2))
		sys.argv = shlex.split(' '.join(argv_orig).replace('-1',str(id1),1).replace('-1',str(id2),1))
		job_options = get_options(single=True,allow_unknown=True)
		fprint("Making datacards")
		makeDatacards(job_options)
		fprint("Running combine")
		runCombine(job_options)

	# hadd outputs
	files = glob.glob("results_*.root")
	cmd = "hadd results_{}_part{}.root {}".format(options.set, options.firstJob/options.split, " ".join(files))
	fprint(cmd[:])
	os.system(cmd)
