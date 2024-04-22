import argparse

def fprint(msg):
    import sys
    print(msg)
    sys.stdout.flush()

def get_options(single=False):
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	#AR-180426: When parse_args() returns from parsing this command line,options.signal will be "SMSqqqq1000", options.fastsim will be "false" in default case
	#AR-180426:sample command to run this script, coming from analysisBuilderCondor.py will be: python analysisBuilderCondor.py --signal T1tttt --mGo 1500 --mLSP 100 --fastsim --realData  --tag allBkgs
	parser.add_argument("--signal", dest="signal", type=str, required=True, help="model name (e.g. T1tttt)", metavar="signal")
	parser.add_argument("--lumi", dest="lumi", default = 10., type=float, help="luminosity in fb-1", metavar="lumi")
	parser_model = parser.add_mutually_exclusive_group()
	parser_model.add_argument("--masses", dest="masses", default=None, type=int, nargs=2, help="Mass of Gluino, mass of LSP", metavar=("mGo","mLSP"))
	if single:
		parser_model.add_argument("--params", dest="params", default=None, type=str, nargs=3, help="pMSSM params", metavar=("set","id1","id2"))
	else:
		parser_model.add_argument("--set", dest="set", default=None, type=str, help="pMSSM set name", metavar="set")
	parser.add_argument('--realData',action='store_true', dest='realData', default=False, help='use real data')
	parser.add_argument('--sigDir',dest="sigDir", default="root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/", type=str, help='input signal histogram directory', metavar="sigDir")
	if not single:
		parser.add_argument('--transfer',action='store_true', dest='transfer', default=False, help='transfer output back to input dir')
		parser.add_argument("--operation", type=int, default=None, help="operation to perform")
	options = parser.parse_args()

	# postprocessing
	options.smsIn = None
	if hasattr(options,'set') and options.set is not None:
		options.sms = options.signal+'_'+options.set
	else:
		if hasattr(options,'params') and options.params is not None:
			options.masses = options.params[1:]
			options.smsIn = options.signal+'_'+options.params[0]
		options.mGo = int(options.masses[0])
		options.mLSP = int(options.masses[1])
		options.sms = "{}_{}_{}".format(options.signal,options.mGo,options.mLSP)
	if options.smsIn is None:
		options.smsIn = options.sms

	return options

#yearsToMerge=["MC2016","MC2017","MC2018", "MC2018HEM"]
yearsToMerge=["MC2017","MC2018", "MC2018HEM"]
#RunLumi=[ 35916.403 , 41521.425,21000.905,38196.951 ]
RunLumi=[ 41521.425,21000.905,38196.951 ]

def ProjectTHN(hist, id1, id2):
	id1 = int(id1)
	id2 = int(id2)

	dims = hist.GetNdimensions()
	npmssm = 2
	pdims = dims - npmssm
	if pdims != 1:
		raise ValueError("Requested projection to {} dims".format(pdims))

	bin1 = hist.GetAxis(0).FindBin(id1)
	bin2 = hist.GetAxis(1).FindBin(id2)

	hist.GetAxis(0).SetRange(bin1,bin1)
	hist.GetAxis(1).SetRange(bin2,bin2)

	hproj = hist.Projection(2,"E")
	return hproj
