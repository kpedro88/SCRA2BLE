import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
import os
from singleBin import *
from cardUtilities import *
from SignalMergePeriods import *
from common import *

def NominalSignal(inputfile,sms,yearsToMerge,RunLumi):
	MergedFullRun2=MergeSignal(inputfile,sms,yearsToMerge,RunLumi);
	MergedFullRun2.SetName("RA2bin_%s_fast_nominalOrig" %(sms))
	MHTCorr_Unc=[]
	if "T1tttt" in signal or "T2tt" in signal or "T5qqqqVV" in signal or "pMSSM" in signal:
		MHTCorr_Unc=SubtractSignalContamination(signaldirtag,sms,yearsToMerge,RunLumi)
	else:MHTCorr_Unc=MHTSystematicGenMHT(signaldirtag,sms, yearsToMerge,RunLumi);
	return MHTCorr_Unc

def MergeStatErr(signaldirtag,sms,MergedNominal):
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(sms))
	MCStatErr=SigTempFile.Get("RA2bin_%s_MC2016_fast_MCStatErr" %sms);
	MCStatErr.SetDirectory(0)
	MCStatErr.Reset();
	for i in range(1, MergedNominal.GetNbinsX()+1):
		StatErr=MergedNominal.GetBinError(i);
		if StatErr<=0 or MergedNominal.GetBinContent(i)<=0:StatErr=1.0;
		else:
			StatErr=1.0+(StatErr/MergedNominal.GetBinContent(i))
		MCStatErr.SetBinContent(i, StatErr);
	SigTempFile.Close();
	return MCStatErr

def MergeSignalSystematics(signaldirtag,sms,yearsToMerge,RunLumi):
	MergedNominal=MergeSignal(signaldirtag,sms,yearsToMerge,RunLumi);
	systs = dict(
		MCStatErr=MergeStatErr(signaldirtag,sms,MergedNominal),
		#Symmetric Norm Uncertainties
		LumiUnc=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"lumiuncUp",MergedNominal,True),
		JetIDUnc=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"jetiduncUp",MergedNominal,True),
		IsoTrackUnc=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isotrackuncUp",MergedNominal,True),
		PrefireUncUp=MergeUncPreFireCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"prefireuncUp",MergedNominal,True),
		PrefireUncDown=MergeUncPreFireCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"prefireuncDown",MergedNominal,False),
		ISRUncUp=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isruncUp",MergedNominal,True),
		ISRUncDown=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isruncDown",MergedNominal,False),
		TrigUnc=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"triguncUp",MergedNominal),
		TrigSysUnc=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"trigsystuncUp;",MergedNominal),
		PUUncUp=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"puuncUp",MergedNominal,True),
		PUUncDown=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"puuncDown",MergedNominal,False),
		ScaleUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"scaleuncUp",MergedNominal),
		JERUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JERup",MergedNominal),
		JECUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JECup",MergedNominal),
		BTagSFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagSFuncUp",MergedNominal),
		MisTagSFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagSFuncUp",MergedNominal),
		CTagCFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"ctagCFuncUp",MergedNominal),
		BTagCFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagCFuncUp",MergedNominal),
		MisTagCFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagCFuncUp",MergedNominal),
		ScaleUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"scaleuncDown",MergedNominal),
		JERUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JERdown",MergedNominal),
		JECUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JECdown",MergedNominal),
		BTagSFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagSFuncDown",MergedNominal),
		MisTagSFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagSFuncDown",MergedNominal),
		BTagCFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagCFuncDown",MergedNominal),
		CTagCFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"ctagCFuncDown",MergedNominal),
		MisTagCFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagCFuncDown",MergedNominal),
	)
	return systs

if __name__ == '__main__':
	options = get_options()

	ofile
	odir = 'testCards-Moriond-%s-%1.1f/' % ( sms, lumi );
	#forcefully remove directory if it exists
	if os.path.exists(odir): os.system( "rm -rf %s" % (odir) );
	os.makedirs(odir);

	# --------------------------------------------
	# signal

	TestNominal=NominalSignal(options.sigDir,options.sms,yearsToMerge,RunLumi)

	systs = MergeSignalSystematics(options.sigDir,options.sms,yearsToMerge,RunLumi)

	ofilename = "RA2bin_merge_%s_fast.root" %(options.sms)
	ofile = TFile.Open(ofilename,"RECREATE")
	ofile.cd()
	for h in TestNominal:
		h.Write()
	for k,v in systs.iteritems():
		v.Write(k)
	ofile.Close()
	os.system("xrdcp -f {0} {1}/{0}".format(ofilename,options.sigDir))
	os.remove(ofilename)
