import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
import os
from SignalMergePeriods import *
from common import *

def MergeNominal(sigDir,sms,yearsToMerge,RunLumi):
	MergedFullRun2=MergeSignal(sigDir,sms,yearsToMerge,RunLumi);
	MergedFullRun2.SetName("RA2bin_%s%s_nominalOrig" %(sms,getHistoSuffix(sms)))
	return MergedFullRun2

def NominalSignal(sigDir,sms,yearsToMerge,RunLumi):
	fprint("NominalSignal")
	MHTCorr_Unc=[]
	if "T1tttt" in sms or "T2tt" in sms or "T5qqqqVV" in sms or "pMSSM" in sms:
		MHTCorr_Unc=SubtractSignalContamination(sigDir,sms,yearsToMerge,RunLumi)
	else:MHTCorr_Unc=MHTSystematicGenMHT(sigDir,sms, yearsToMerge,RunLumi);
	return MHTCorr_Unc

def MergeStatErr(sigDir,sms,MergedNominal):
	fprint("MergeStatErr")
	SigTempFile=TFile.Open(sigDir+"/RA2bin_proc_%s_MC2018_fast.root" %(sms))
	MCStatErr=SigTempFile.Get("%s_%s_MC2018%s_MCStatErr" %(getHistoPrefix(sms),sms,getHistoSuffix(sms)));
	SetDirectory0(MCStatErr)
	MCStatErr.Reset();
	def _fn(bN,b1):
		StatErr=MergedNominal.GetBinError(bN);
		if StatErr<=0 or MergedNominal.GetBinContent(bN)<=0: StatErr=1.0;
		else:
			StatErr=1.0+(StatErr/MergedNominal.GetBinContent(bN))
		MCStatErr.SetBinContent(bN, StatErr);
	loopTHN(MergedNominal,_fn)
	SigTempFile.Close();
	return MCStatErr

def WriteSingleHist(oname,name,func,*args):
	suff = '_'.join(name) if isinstance(name,list) else name
	oname = oname.replace(".root","_{}.root".format(suff))
	ofile = TFile.Open(oname,"RECREATE")
	hist = func(*args)
	ofile.cd()
	if isinstance(hist,list):
		for h,n in zip(hist,name):
			h.Write(n)
	else:
		hist.Write(name)
	ofile.Close()

if __name__ == '__main__':
	options = get_options()

	oname = "RA2bin_merge_%s_fast.root" %(options.sms)

	oname2 = oname.replace(".root","_{}.root".format("Merged"))
	if options.operation is None:
		MergedNominal = None
	else:
		if os.path.isfile(oname2):
			mfile = TFile.Open(oname2)
			MergedNominal = mfile.Get("MergedNominal")
		else:
			MergedNominal = MergeNominal(options.sigDir,options.sms,yearsToMerge,RunLumi)
			mfile = TFile.Open(oname2,"RECREATE")
			mfile.cd()
			MergedNominal.Write("MergedNominal")
			mfile.Close()

	operations = [
		[["nominalOrig","MHTSyst"],NominalSignal,options.sigDir,options.sms,yearsToMerge,RunLumi],
		["MCStatErr",MergeStatErr,options.sigDir,options.sms,MergedNominal],
		["LumiUnc",MergeUncCorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"lumiuncUp",MergedNominal,True],
		["JetIDUnc",MergeUncCorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"jetiduncUp",MergedNominal,True],
		["IsoTrackUnc",MergeUncCorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"isotrackuncUp",MergedNominal,True],
		["PrefireUncUp",MergeUncCorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"prefireuncUp",MergedNominal,True],
		["PrefireUncDown",MergeUncCorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"prefireuncDown",MergedNominal,False],
		["ISRUncUp",MergeUncCorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"isruncUp",MergedNominal,True],
		["ISRUncDown",MergeUncCorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"isruncDown",MergedNominal,False],
		["TrigUnc",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"triguncUp",MergedNominal],
		["TrigSysUnc",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"trigsystuncUp",MergedNominal],
		["PUUncUp",MergeUncCorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"puuncUp",MergedNominal,True],
		["PUUncDown",MergeUncCorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"puuncDown",MergedNominal,False],
		["JERUncUp",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"JERup",MergedNominal],
		["JECUncUp",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"JECup",MergedNominal],
		["BTagSFUncUp",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"btagSFuncUp",MergedNominal],
		["MisTagSFUncUp",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"mistagSFuncUp",MergedNominal],
		["CTagCFUncUp",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"ctagCFuncUp",MergedNominal],
		["BTagCFUncUp",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"btagCFuncUp",MergedNominal],
		["MisTagCFUncUp",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"mistagCFuncUp",MergedNominal],
		["JERUncDown",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"JERdown",MergedNominal],
		["JECUncDown",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"JECdown",MergedNominal],
		["BTagSFUncDown",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"btagSFuncDown",MergedNominal],
		["MisTagSFUncDown",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"mistagSFuncDown",MergedNominal],
		["BTagCFUncDown",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"btagCFuncDown",MergedNominal],
		["CTagCFUncDown",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"ctagCFuncDown",MergedNominal],
		["MisTagCFUncDown",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"mistagCFuncDown",MergedNominal],
	]

	if "pMSSM" not in options.sms:
		operations.extend([
			["ScaleUncUp",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"scaleuncUp",MergedNominal],
			["ScaleUncDown",MergeUncUncorrelated,options.sigDir,options.sms,yearsToMerge,RunLumi,"scaleuncDown",MergedNominal],
		])

	if options.operation is None:
		# run each operation as separate subprocess to restrict memory usage
		for i in range(len(operations)):
			cmd = "python {} --operation {}".format(" ".join(sys.argv), i)
			fprint(cmd)
			os.system(cmd)

		# remove tmp file
		if os.path.isfile(oname2):
			os.system("rm {}".format(oname2))

		# hadd
		os.system("hadd -f {0} {1} && rm {1}".format(oname, oname.replace(".root","_*.root")))

		if options.transfer:
			os.system("xrdcp -f {0} {1}/{0}".format(oname,options.sigDir))
			os.remove(oname)
	else:
		WriteSingleHist(oname,*operations[options.operation])
