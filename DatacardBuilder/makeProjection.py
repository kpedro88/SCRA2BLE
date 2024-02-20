import argparse
from common import *
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *

if __name__=="__main__":
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--params", dest="params", default=None, type=str, nargs=3, help="pMSSM params", metavar=("set","id1","id2"))
	parser.add_argument('--sigDir',dest="sigDir", default="root://cmseos.fnal.gov//store/user/lpcpmssm/Datacards/Run2ProductionV17_v1", type=str, help='input signal histogram directory', metavar="sigDir")
	options = parser.parse_args()

	options.signal = "pMSSM"
	options.smsIn = options.signal+'_'+options.params[0]
	options.sms = "{}_{}_{}".format(options.signal,options.params[1],options.params[2])

	for year in yearsToMerge:
		SigTempFile=TFile.Open(options.sigDir+"/RA2bin_proc_%s_%s_fast.root" %(options.smsIn,year))
		SigOutFile=TFile.Open("RA2bin_proc_%s_%s_fast.root"%(options.sms,year),"RECREATE")
		for key in [k.GetName() for k in SigTempFile.GetListOfKeys()]:
			htmp = SigTempFile.Get(key)
			# project pMSSM model
			ptmp = ProjectTHN(htmp, options.params[1], options.params[2])
			ptmp.SetTitle("")
			SigOutFile.cd()
			pname = htmp.GetName().split('_')[-1]
			ptmp.Write("id1_id2_RA2bin_{}_{}_{}".format(options.sms,year,pname))
		SigTempFile.Close()
		SigOutFile.Close()
