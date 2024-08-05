import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
import os,sys,glob
from common import get_options, fprint

def runPoint(id1,id2):
	fprint("Processing model: {} {}".format(id1,id2))
	args = ' '.join(sys.argv[:]).replace('-1',str(id1),1).replace('-1',str(id2),1)
	job_options = get_options(single=True,allow_unknown=True)
	cmd = "python makeDatacards.py {}".format(args)
	fprint(cmd)
	os.system(cmd)
	cmd = "python runCombine.py {}".format(args)
	fprint(cmd)
	os.system(cmd)

if __name__=="__main__":
	options = get_options(single=True,jobs=True)

	if len(options.missing)>0:
		with open(options.missing,'r') as mfile:
			for line in mfile:
				id1, id2 = line.rstrip().split()
				runPoint(id1,id2)

	else:
		idfile = TFile.Open("root://cmseos.fnal.gov//store/user/lpcpmssm/SLHATrees/{}.root".format(options.set))
		idtree = idfile.Get("mcmc")

		maxJobs = min(options.firstJob+options.split, idtree.GetEntries())
		for entry in range(options.firstJob, maxJobs):
			idtree.GetEntry(entry)
			id1 = idtree.chain_index
			id2 = idtree.iteration_index
			runPoint(id1,id2)

	# hadd outputs
	files = glob.glob("results_*.root")
	cmd = "hadd results_{}_part{}.root {}".format(options.set, options.firstJob/options.split, " ".join(files))
	fprint(cmd[:])
	os.system(cmd)
