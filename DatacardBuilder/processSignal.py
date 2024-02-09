import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
import os
from singleBin import *
from cardUtilities import *
from SignalMergePeriods import *
from common import *

def NominalSignal(signaldirtag,sms,yearsToMerge,RunLumi):
	print("NominalSignal")
	MergedFullRun2=MergeSignal(signaldirtag,sms,yearsToMerge,RunLumi);
	MergedFullRun2.SetName("RA2bin_%s%s_nominalOrig" %(sms,getHistoSuffix(sms)))
	MHTCorr_Unc=[]
	if "T1tttt" in sms or "T2tt" in sms or "T5qqqqVV" in sms or "pMSSM" in sms:
		MHTCorr_Unc=SubtractSignalContamination(signaldirtag,sms,yearsToMerge,RunLumi)
	else:MHTCorr_Unc=MHTSystematicGenMHT(signaldirtag,sms, yearsToMerge,RunLumi);
	return MergedFullRun2, MHTCorr_Unc

def MergeStatErr(signaldirtag,sms,MergedNominal):
	print("MergeStatErr")
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2018_fast.root" %(sms))
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

def MergeSignalSystematic(oname,name,func,*args):
	oname = oname.replace(".root","_{}.root".format(name))
	ofile = TFile.Open(oname,"RECREATE")
	hist = func(*args)
	ofile.cd()
	hist.Write(name)
	ofile.Close()

def MergeSignalSystematics(signaldirtag,sms,yearsToMerge,RunLumi,MergedNominal,oname):
	MergeSignalSystematic(oname,"MCStatErr",MergeStatErr,signaldirtag,sms,MergedNominal)
	MergeSignalSystematic(oname,"LumiUnc",MergeUncCorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"lumiuncUp",MergedNominal,True)
	MergeSignalSystematic(oname,"JetIDUnc",MergeUncCorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"jetiduncUp",MergedNominal,True)
	MergeSignalSystematic(oname,"IsoTrackUnc",MergeUncCorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"isotrackuncUp",MergedNominal,True)
	MergeSignalSystematic(oname,"PrefireUncUp",MergeUncPreFireCorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"prefireuncUp",MergedNominal,True)
	MergeSignalSystematic(oname,"PrefireUncDown",MergeUncPreFireCorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"prefireuncDown",MergedNominal,False)
	MergeSignalSystematic(oname,"ISRUncUp",MergeUncCorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"isruncUp",MergedNominal,True)
	MergeSignalSystematic(oname,"ISRUncDown",MergeUncCorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"isruncDown",MergedNominal,False)
	MergeSignalSystematic(oname,"TrigUnc",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"triguncUp",MergedNominal)
	MergeSignalSystematic(oname,"TrigSysUnc",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"trigsystuncUp",MergedNominal)
	MergeSignalSystematic(oname,"PUUncUp",MergeUncCorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"puuncUp",MergedNominal,True)
	MergeSignalSystematic(oname,"PUUncDown",MergeUncCorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"puuncDown",MergedNominal,False)
	MergeSignalSystematic(oname,"JERUncUp",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"JERup",MergedNominal)
	MergeSignalSystematic(oname,"JECUncUp",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"JECup",MergedNominal)
	MergeSignalSystematic(oname,"BTagSFUncUp",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"btagSFuncUp",MergedNominal)
	MergeSignalSystematic(oname,"MisTagSFUncUp",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"mistagSFuncUp",MergedNominal)
	MergeSignalSystematic(oname,"CTagCFUncUp",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"ctagCFuncUp",MergedNominal)
	MergeSignalSystematic(oname,"BTagCFUncUp",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"btagCFuncUp",MergedNominal)
	MergeSignalSystematic(oname,"MisTagCFUncUp",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"mistagCFuncUp",MergedNominal)
	MergeSignalSystematic(oname,"JERUncDown",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"JERdown",MergedNominal)
	MergeSignalSystematic(oname,"JECUncDown",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"JECdown",MergedNominal)
	MergeSignalSystematic(oname,"BTagSFUncDown",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"btagSFuncDown",MergedNominal)
	MergeSignalSystematic(oname,"MisTagSFUncDown",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"mistagSFuncDown",MergedNominal)
	MergeSignalSystematic(oname,"BTagCFUncDown",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"btagCFuncDown",MergedNominal)
	MergeSignalSystematic(oname,"CTagCFUncDown",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"ctagCFuncDown",MergedNominal)
	MergeSignalSystematic(oname,"MisTagCFUncDown",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"mistagCFuncDown",MergedNominal)

	if "pMSSM" not in sms:
		MergeSignalSystematic(oname,"ScaleUncUp",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"scaleuncUp",MergedNominal)
		MergeSignalSystematic(oname,"ScaleUncDown",MergeUncUncorrelated,signaldirtag,sms,yearsToMerge,RunLumi,"scaleuncDown",MergedNominal)

if __name__ == '__main__':
	options = get_options()

	# --------------------------------------------
	# signal

	MergedNominal, MergedFinal = NominalSignal(options.sigDir,options.sms,yearsToMerge,RunLumi)

	ofilename = "RA2bin_merge_%s_fast.root" %(options.sms)

	MergeSignalSystematics(options.sigDir,options.sms,yearsToMerge,RunLumi,MergedNominal,ofilename)

	ofile = TFile.Open(ofilename.replace(".root","_Nominal.root"),"RECREATE")
	ofile.cd()
	for h in MergedFinal:
		h.Write()
	ofile.Close()

	# hadd
	os.system("hadd {0} {1} && rm {1}".format(ofilename, ofilename.replace(".root","_*.root")))

	if options.transfer:
		os.system("xrdcp -f {0} {1}/{0}".format(ofilename,options.sigDir))
		os.remove(ofilename)
