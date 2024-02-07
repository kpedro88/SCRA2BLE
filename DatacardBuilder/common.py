import argparse

def get_options():
	parser = argparse.ArgumentParser()
	#AR-180426: When parse_args() returns from parsing this command line,options.signal will be "SMSqqqq1000", options.fastsim will be "false" in default case
	#AR-180426:sample command to run this script, coming from analysisBuilderCondor.py will be: python analysisBuilderCondor.py --signal T1tttt --mGo 1500 --mLSP 100 --fastsim --realData  --tag allBkgs
	parser.add_argument("--signal", dest="signal", type=str, required=True, help="model name (e.g. T1tttt)", metavar="signal")
	parser.add_argument("--lumi", dest="lumi", default = 10., type=float, help="luminosity in fb-1", metavar="lumi")
	parser_model = parser.add_mutually_exclusive_group()
	parser_sms = parser_model.add_group()
	parser_sms.add_argument("--mGo", dest="mGo", default=1000, type=int, help="Mass of Gluino", metavar="mGo")
	parser_sms.add_argument("--mLSP", dest="mLSP", default=900, type=int, help="Mass of LSP", metavar="mLSP")
	parser_model.add_argument("--set", dest="set", default="set1prompt1", type=str, help="pMSSM set name", metavar="set")
	parser.add_argument('--realData',action='store_true', dest='realData', default=False, help='use real data')
	parser.add_argument('--sigDir',dest="sigDir", default="root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/", type=str, help='input signal histogram directory', metavar="sigDir")
	options = parser.parse_args()

	# postprocessing
	if hasattr(options,'set'):
		options.sms = options.signal+'_'+options.set
	else:
		options.sms = options.signal+'_'+options.mGo+'_'+options.mLSP

	return options

yearsToMerge=["MC2016","MC2017","MC2018", "MC2018HEM"]
RunLumi=[ 35916.403 , 41521.425,21000.905,38196.951 ]
