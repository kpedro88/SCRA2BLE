import argparse

def get_options():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	#AR-180426: When parse_args() returns from parsing this command line,options.signal will be "SMSqqqq1000", options.fastsim will be "false" in default case
	#AR-180426:sample command to run this script, coming from analysisBuilderCondor.py will be: python analysisBuilderCondor.py --signal T1tttt --mGo 1500 --mLSP 100 --fastsim --realData  --tag allBkgs
	parser.add_argument("--signal", dest="signal", type=str, required=True, help="model name (e.g. T1tttt)", metavar="signal")
	parser.add_argument("--lumi", dest="lumi", default = 10., type=float, help="luminosity in fb-1", metavar="lumi")
	parser_model = parser.add_mutually_exclusive_group()
	parser_model.add_argument("--masses", dest="masses", default=None, type=int, nargs=2, help="Mass of Gluino, mass of LSP", metavar=("mGo","mLSP"))
	parser_model.add_argument("--set", dest="set", default=None, type=str, help="pMSSM set name", metavar="set")
	parser.add_argument('--realData',action='store_true', dest='realData', default=False, help='use real data')
	parser.add_argument('--sigDir',dest="sigDir", default="root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/", type=str, help='input signal histogram directory', metavar="sigDir")
	parser.add_argument('--transfer',action='store_true', dest='transfer', default=False, help='transfer output back to input dir')
	parser.add_argument("--operation", type=int, default=None, help="operation to perform")
	options = parser.parse_args()

	# postprocessing
	if options.set is not None:
		options.sms = options.signal+'_'+options.set
	else:
		options.mGo = options.masses[0]
		options.mLSP = options.masses[1]
		options.sms = "{}_{}_{}".format(options.signal,options.mGo,options.mLSP)

	return options

#yearsToMerge=["MC2016","MC2017","MC2018", "MC2018HEM"]
yearsToMerge=["MC2017","MC2018", "MC2018HEM"]
#RunLumi=[ 35916.403 , 41521.425,21000.905,38196.951 ]
RunLumi=[ 41521.425,21000.905,38196.951 ]
