import os, sys, argparse
from common import *
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *

def makeProj(options):
	SigTempName=options.sigDir+"/RA2bin_%s_%s_%s_%s.root" %(options.pref,options.smsIn,options.year,options.suff)
	fprint(SigTempName)
	SigTempFile=TFile.Open(SigTempName)
	SigOutFile=TFile.Open("RA2bin_%s_%s_%s_%s.root"%(options.pref,options.sms,options.year,options.suff),"RECREATE")
	for key in [k.GetName() for k in SigTempFile.GetListOfKeys()]:
		htmp = SigTempFile.Get(key)
		# project pMSSM model
		ptmp = ProjectTHN(htmp, options.params[1], options.params[2])
		ptmp.SetTitle("")
		SigOutFile.cd()
		pname = htmp.GetName().split('_')[-1]
		ptmp.Write("id1_id2_RA2bin_{}_{}_{}".format(options.sms,options.year,pname))
	SigTempFile.Close()
	SigOutFile.Close()

if __name__=="__main__":
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--params", dest="params", default=None, type=str, nargs=3, help="pMSSM params", metavar=("set","id1","id2"))
	parser.add_argument('--sigDir',dest="sigDir", default="root://cmseos.fnal.gov//store/user/lpcpmssm/Datacards/Run2ProductionV17_v1", type=str, help='input signal histogram directory', metavar="sigDir")
	parser.add_argument('--pref',dest="pref", default="proc", type=str, help='prefix for filename RA2b_[prefix]_...')
	parser.add_argument('--suff',dest="suff", default="fast", type=str, help='suffix for filename ..._MC201X_[suffix].root')
	parser.add_argument('--year',dest="year", default=None, type=str, help='year to process (None=all)')
	options = parser.parse_args()

	options.signal = "pMSSM"
	options.smsIn = options.signal+'_'+options.params[0]
	options.sms = "{}_{}_{}".format(options.signal,options.params[1],options.params[2])

	if options.year is None:
		for year in yearsToMerge:
			cmd = "python {} --year {}".format(" ".join(sys.argv), year)
			fprint(cmd)
			os.system(cmd)
	else:
		makeProj(options)
