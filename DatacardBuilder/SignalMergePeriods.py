from ROOT import *
from math import sqrt
import sys
from array import array

# hist determines whether the loop type is TH1 or THnSparse
# fn is a function with signature: fn(bN, b1)
# where bN is the N-dimensional bin axis for THnSparse
# and b1 is the 1-dimensional bin axis for TH1
# (if hist is TH1, then bN = b1)
def loopTHN(hist,fn):
	if hist.InheritsFrom(THnSparse.Class()):
		iter = THnIter(hist)
		b = long(0)
		while (b = iter.Next()) >= 0:
			fn(b,iter.GetCoord(2))
	else:
		for b in range(1,hist.GetNbinsX()+1):
			fn(b,b)

def SubtractSignalContamination(signaldirtag,sms, yearsToCombine, lumiscales):
	LLPlusHadTauAvg_file=TFile.Open("inputHistograms/histograms_137.4fb/InputsForLimits_data_formatted_LLPlusHadTau.root");
	LLPlusHadTauPrediction_AVGTF=LLPlusHadTauAvg_file.Get("LLPlusHadTauTF")
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(sms))
	NominalCorrSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_nominalOrig" %sms)
	NominalCorrSignalUnc=SigTempFile.Get("RA2bin_%s_MC2016_fast_MHTSyst" %sms)
	GenCorrSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_genMHT" %sms)
	SignalContaminReco=SigTempFile.Get("RA2bin_%s_MC2016_fast_SLm" %(sms))
	SignalContaminGEN=SigTempFile.Get("RA2bin_%s_MC2016_fast_SLm-genMHT" %(sms))
	SignalContaminReco.Reset()
	SignalContaminGEN.Reset()

	GenCorrSignal.Reset();
	NominalCorrSignal.Reset()
	NominalCorrSignalUnc.Reset();
	NominalCorrSignal.SetDirectory(0)
	NominalCorrSignalUnc.SetDirectory(0)
	GenCorrSignal.SetDirectory(0)
	SignalContaminGEN.SetDirectory(0)
	SignalContaminReco.SetDirectory(0)
	LLPlusHadTauPrediction_AVGTF.SetDirectory(0)
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(sms,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("RA2bin_%s_%s_fast_nominalOrig" %(sms,yearsToCombine[i]));
		GENSignal=SignalRunFile.Get("RA2bin_%s_%s_fast_genMHT" %(sms,yearsToCombine[i]));
		SignalContaminRecoMu=SignalRunFile.Get("RA2bin_%s_%s_fast_SLm" %(sms,yearsToCombine[i]));
		SignalContaminGenMu=SignalRunFile.Get("RA2bin_%s_%s_fast_SLm-genMHT" %(sms,yearsToCombine[i]));
		SignalContaminRecoEle=SignalRunFile.Get("RA2bin_%s_%s_fast_SLe" %(sms,yearsToCombine[i]));
		SignalContaminGenEle=SignalRunFile.Get("RA2bin_%s_%s_fast_SLe-genMHT" %(sms,yearsToCombine[i]));

		SignalRun.Scale(lumiscales[i])
		SignalRun.SetName("%s_%s" %(sms,yearsToCombine[i]))
		GENSignal.Scale(lumiscales[i])
		GENSignal.SetName("Gen%s_%s" %(sms,yearsToCombine[i]))
		GenCorrSignal.Add(GENSignal)
		NominalCorrSignal.Add(SignalRun)
		SignalContaminGenMu.Scale(lumiscales[i])
		SignalContaminGenEle.Scale(lumiscales[i])
		SignalContaminRecoMu.Scale(lumiscales[i])
		SignalContaminRecoEle.Scale(lumiscales[i])
		SignalContaminReco.Add(SignalContaminRecoMu);
		SignalContaminReco.Add(SignalContaminRecoEle);
		SignalContaminGEN.Add(SignalContaminGenMu);
		SignalContaminGEN.Add(SignalContaminGenEle);
		SignalRunFile.Close();

	def _fn(bN,b1):
		UnCorrSignal=NominalCorrSignal.GetBinContent(bN)-(SignalContaminReco.GetBinContent(bN)*LLPlusHadTauPrediction_AVGTF.GetBinContent(b1))
		GenMHTCleaned=GenCorrSignal.GetBinContent(bN)-(SignalContaminGEN.GetBinContent(bN)*LLPlusHadTauPrediction_AVGTF.GetBinContent(b1))
		NominalCorrSignal.SetBinContent(bN, (UnCorrSignal+GenMHTCleaned)/2.)
		if NominalCorrSignal.GetBinContent(bN)>0:
			NominalCorrSignalUnc.SetBinContent(bN, 1.0+(abs(UnCorrSignal-GenMHTCleaned)/2.)/NominalCorrSignal.GetBinContent(bN))
		else:
			NominalCorrSignalUnc.SetBinContent(bN,1.0)
	loopTHN(NominalCorrSignal,_fn)

	MHTCorr=[]
	MHTCorr.append(NominalCorrSignal)
	MHTCorr.append(NominalCorrSignalUnc)
	return MHTCorr

def MHTSystematicGenMHT(signaldirtag,signaltag, yearsToCombine,lumiscales):
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(signaltag))
	NominalCorrSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_nominalOrig" %signaltag)#SignalRuns[0];
	NominalCorrSignalUnc=SigTempFile.Get("RA2bin_%s_MC2016_fast_MHTSyst" %signaltag)#SignalRuns[0];
	GenCorrSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_genMHT" %signaltag)#SignalRuns[0];
	GenCorrSignal.Reset();
	NominalCorrSignal.Reset()
	NominalCorrSignalUnc.Reset();
	NominalCorrSignal.SetDirectory(0)
	NominalCorrSignalUnc.SetDirectory(0)
	GenCorrSignal.SetDirectory(0)
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("RA2bin_%s_%s_fast_nominalOrig" %(signaltag,yearsToCombine[i]));
		GENSignal=SignalRunFile.Get("RA2bin_%s_%s_fast_genMHT" %(signaltag,yearsToCombine[i]));
		SignalRun.Scale(lumiscales[i])
		SignalRun.SetName("%s_%s" %(signaltag,yearsToCombine[i]))
		GENSignal.Scale(lumiscales[i])
		GENSignal.SetName("Gen%s_%s" %(signaltag,yearsToCombine[i]))
		GenCorrSignal.Add(GENSignal)
		NominalCorrSignal.Add(SignalRun)
		SignalRunFile.Close();

	def _fn(bN,b1):
		UnCorrSignal=NominalCorrSignal.GetBinContent(bN)
		NominalCorrSignal.SetBinContent(bN, (UnCorrSignal+GenCorrSignal.GetBinContent(bN))/2.)
		if NominalCorrSignal.GetBinContent(bN)>0:
			NominalCorrSignalUnc.SetBinContent(bN, 1.0+(abs(UnCorrSignal-GenCorrSignal.GetBinContent(bN))/2.)/NominalCorrSignal.GetBinContent(bN))
		else:
			NominalCorrSignalUnc.SetBinContent(bN, 1.0)
	loopTHN(NominalCorrSignal,_fn)
	MHTCorr=[]
	MHTCorr.append(NominalCorrSignal)

	MHTCorr.append(NominalCorrSignalUnc)
	return MHTCorr


def MergeSignal(signaldirtag,signaltag, yearsToCombine, lumiscales):
	global MergedSignal
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(signaltag))
	MergedSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_nominalOrig" %signaltag)#SignalRuns[0];#.Clone("MergedSignal");
	MergedSignal.Reset();
	MergedSignal.SetDirectory(0)
	SigTempFile.Close();
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("RA2bin_%s_%s_fast_nominalOrig" %(signaltag,yearsToCombine[i]));
		SignalRun.Scale(lumiscales[i])
		SignalRun.SetName("%s_%s" %(signaltag,yearsToCombine[i]))
		if "MC2018" in yearsToCombine[i] and not "MC2018HEM" in yearsToCombine[i]:
			MergedCorrelated=SignalRun.Clone("MergedCorrelated");
			SignalRunFileHEM=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i+1]))
			SignalRunHEM=SignalRunFileHEM.Get("RA2bin_%s_%s_fast_nominalOrig" %(signaltag,yearsToCombine[i+1]))
			SignalRunHEM.Scale(lumiscales[i+1])
			SignalRunHEM.SetName("%s_%s" %(signaltag,yearsToCombine[i+1]))
			SignalRunHEMOrig = SignalRunHEM.Clone("HEMOrig")
			SignalRunHEM.Add(MergedCorrelated)
			def _fn(bN,b1):
				SignalRunHEM.SetBinError(bN, MergedCorrelated.GetBinError(bN)+SignalRunHEMOrig.GetBinError(bN))
			loopTHN(SignalRunHEM,_fn)

		if "MC2018HEM" in yearsToCombine[i]:continue
		MergedSignal.Add(SignalRun);
		SignalRunFile.Close();

	MergedSignal.SetName("RA2bin_%s_fast_nominalOrig" %signaltag)
	return MergedSignal;

def MergeUncUncorrelated(signaldirtag,signaltag, yearsToCombine, lumiscales,Unc,MergedFullRun2):
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(signaltag))
	MergedUnc=SigTempFile.Get("RA2bin_%s_MC2016_fast_%s" %(signaltag,Unc))
	MergedUnc.Reset();
	MergedUnc.SetDirectory(0)
	SigTempFile.Close();
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("RA2bin_%s_%s_fast_nominalOrig" %(signaltag,yearsToCombine[i]));
		SignalRunUnc=SignalRunFile.Get("RA2bin_%s_%s_fast_%s" %(signaltag,yearsToCombine[i],Unc));
		SignalRun.Scale(lumiscales[i])
		sign={}
		def _fn(bN,b1):
			UncQuadSum=MergedUnc.GetBinContent(bN)+pow((SignalRun.GetBinContent(bN)*abs(1-SignalRunUnc.GetBinContent(bN))),2);
			if SignalRunUnc.GetBinContent(bN)>=1.0: sign[bN] = 1.0
			else: sign[bN] = -1.0
			MergedUnc.SetBinContent(bN, UncQuadSum);
		loopTHN(MergedUnc,_fn)
		SignalRunFile.Close();
	def _fn(bN,b1):
		if MergedUnc.GetBinContent(bN)>0:
			MergedUnc.SetBinContent(bN,1.0+sign[bN]*(sqrt(MergedUnc.GetBinContent(bN))/MergedFullRun2.GetBinContent(bN)));
		else: MergedUnc.SetBinContent(bN,1.0);
	loopTHN(MergedUnc,_fn)
	return MergedUnc;

def MergeUncCorrelated(signaldirtag,signaltag, yearsToCombine, lumiscales,Unc,MergedFullRun2,isUp):
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(signaltag))
	MergedUnc=SigTempFile.Get("RA2bin_%s_MC2016_fast_%s" %(signaltag,Unc))
	MergedUnc.Reset();
	MergedUnc.SetDirectory(0)
	SigTempFile.Close();
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("RA2bin_%s_%s_fast_nominalOrig" %(signaltag,yearsToCombine[i]));
		SignalRunUnc=SignalRunFile.Get("RA2bin_%s_%s_fast_%s" %(signaltag,yearsToCombine[i],Unc));
		SignalRun.Scale(lumiscales[i])
		def _fn(bN,b1):
			UncQuadSum=MergedUnc.GetBinContent(bN)+(SignalRun.GetBinContent(bN)*abs(1-SignalRunUnc.GetBinContent(bN)));
			MergedUnc.SetBinContent(bN, UncQuadSum);
		loopTHN(MergedUnc,_fn)
		SignalRunFile.Close();
	def _fn(bN,b1):
		if MergedFullRun2.GetBinContent(bN)>0:
			if isUp: MergedUnc.SetBinContent(bN, 1.0+(MergedUnc.GetBinContent(bN))/MergedFullRun2.GetBinContent(bN));
			else:MergedUnc.SetBinContent(bN, 1.0-(MergedUnc.GetBinContent(bN))/MergedFullRun2.GetBinContent(bN));
		else: MergedUnc.SetBinContent(bN,1.0);
	loopTHN(MergedUnc,_fn)
	return MergedUnc;

def MergeUncPreFireCorrelated(signaldirtag,signaltag, yearsToCombine, lumiscales,Unc,MergedFullRun2,isUp):
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(signaltag))
	MergedUnc=SigTempFile.Get("RA2bin_%s_MC2016_fast_%s" %(signaltag,Unc))
	MergedUnc.Reset();
	MergedUnc.SetDirectory(0)
	SigTempFile.Close();
	for i in range(len(yearsToCombine)):
		if "2018" in yearsToCombine[i]:continue #NO Prefire unc
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("RA2bin_%s_%s_fast_nominalOrig" %(signaltag,yearsToCombine[i]));
		SignalRunUnc=SignalRunFile.Get("RA2bin_%s_%s_fast_%s" %(signaltag,yearsToCombine[i],Unc));
		SignalRun.Scale(lumiscales[i])
		def _fn(bN,b1):
			UncQuadSum=MergedUnc.GetBinContent(bN)+(SignalRun.GetBinContent(bN)*abs(1-SignalRunUnc.GetBinContent(bN)));
			MergedUnc.SetBinContent(bN, UncQuadSum);
		loopTHN(MergedUnc,_fn)
		SignalRunFile.Close();
	def _fn(bN,b1):
		if MergedFullRun2.GetBinContent(bN)>0:
			if isUp: MergedUnc.SetBinContent(bN, 1.0+(MergedUnc.GetBinContent(bN))/MergedFullRun2.GetBinContent(bN));
			else:MergedUnc.SetBinContent(bN, 1.0-(MergedUnc.GetBinContent(bN))/MergedFullRun2.GetBinContent(bN));
		else: MergedUnc.SetBinContent(bN,1.0);
	loopTHN(MergedUnc,_fn)
	return MergedUnc;
