from ROOT import *
from math import sqrt
import sys
from array import array

def getHistoPrefix(sms):
	if "pMSSM" in sms:
		return "id1_id2_RA2bin"
	else:
		return "RA2bin"

def getHistoSuffix(sms):
	if "pMSSM" in sms:
		return ""
	else:
		return "_fast"

def SetDirectory0(hist):
	if hist.InheritsFrom(TH1.Class()):
		hist.SetDirectory(0)

# hist determines whether the loop type is TH1 or THnSparse
# fn is a function with signature: fn(bN, b1)
# where bN is the N-dimensional bin axis for THnSparse
# and b1 is the 1-dimensional bin axis for TH1
# (if hist is TH1, then bN = b1)
def loopTHN(hist,fn):
	if hist.InheritsFrom(THnSparse.Class()):
		iter = THnIter(hist)
		b = long(0)
		idx = [0]*hist.GetNdimensions()
		idx = array('i',idx)
		while True:
			b = iter.Next(idx)
			if b>=0:
				fn(idx,idx[-1])
			else:
				break
	else:
		for b in range(1,hist.GetNbinsX()+1):
			fn(b,b)

def SubtractSignalContamination(signaldirtag,sms, yearsToCombine, lumiscales):
	print("SubtractSignalContamination")
	LLPlusHadTauAvg_file=TFile.Open("inputHistograms/histograms_137.4fb/InputsForLimits_data_formatted_LLPlusHadTau.root");
	LLPlusHadTauPrediction_AVGTF=LLPlusHadTauAvg_file.Get("LLPlusHadTauTF")
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(sms,yearsToCombine[0]))
	NominalCorrSignal=SigTempFile.Get("%s_%s_%s%s_nominalOrig" %(getHistoPrefix(sms),sms,yearsToCombine[0],getHistoSuffix(sms)))
	NominalCorrSignalUnc=SigTempFile.Get("%s_%s_%s%s_MHTSyst" %(getHistoPrefix(sms),sms,yearsToCombine[0],getHistoSuffix(sms)))
	GenCorrSignal=SigTempFile.Get("%s_%s_%s%s_genMHT" %(getHistoPrefix(sms),sms,yearsToCombine[0],getHistoSuffix(sms)))
	SignalContaminReco=SigTempFile.Get("%s_%s_%s%s_SLm" %(getHistoPrefix(sms),sms,yearsToCombine[0],getHistoSuffix(sms)))
	SignalContaminGEN=SigTempFile.Get("%s_%s_%s%s_SLm-genMHT" %(getHistoPrefix(sms),yearsToCombine[0],sms,getHistoSuffix(sms)))
	SignalContaminReco.Reset()
	SignalContaminGEN.Reset()

	GenCorrSignal.Reset();
	NominalCorrSignal.Reset()
	NominalCorrSignalUnc.Reset();
	SetDirectory0(NominalCorrSignal)
	SetDirectory0(NominalCorrSignalUnc)
	SetDirectory0(GenCorrSignal)
	SetDirectory0(SignalContaminGEN)
	SetDirectory0(SignalContaminReco)
	SetDirectory0(LLPlusHadTauPrediction_AVGTF)
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(sms,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("%s_%s_%s%s_nominalOrig" %(getHistoPrefix(sms),sms,yearsToCombine[i],getHistoSuffix(sms)));
		GENSignal=SignalRunFile.Get("%s_%s_%s%s_genMHT" %(getHistoPrefix(sms),sms,yearsToCombine[i],getHistoSuffix(sms)));
		SignalContaminRecoMu=SignalRunFile.Get("%s_%s_%s%s_SLm" %(getHistoPrefix(sms),sms,yearsToCombine[i],getHistoSuffix(sms)));
		SignalContaminGenMu=SignalRunFile.Get("%s_%s_%s%s_SLm-genMHT" %(getHistoPrefix(sms),sms,yearsToCombine[i],getHistoSuffix(sms)));
		SignalContaminRecoEle=SignalRunFile.Get("%s_%s_%s%s_SLe" %(getHistoPrefix(sms),sms,yearsToCombine[i],getHistoSuffix(sms)));
		SignalContaminGenEle=SignalRunFile.Get("%s_%s_%s%s_SLe-genMHT" %(getHistoPrefix(sms),sms,yearsToCombine[i],getHistoSuffix(sms)));

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
	print("MHTSystematicGenMHT")
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[0]))
	NominalCorrSignal=SigTempFile.Get("%s_%s_%s%s_nominalOrig" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[0],getHistoSuffix(signaltag)))
	NominalCorrSignalUnc=SigTempFile.Get("%s_%s_%s%s_MHTSyst" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[0],getHistoSuffix(signaltag)))
	GenCorrSignal=SigTempFile.Get("%s_%s_%s%s_genMHT" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[0],getHistoSuffix(signaltag)))
	GenCorrSignal.Reset();
	NominalCorrSignal.Reset()
	NominalCorrSignalUnc.Reset();
	SetDirectory0(NominalCorrSignal)
	SetDirectory0(NominalCorrSignalUnc)
	SetDirectory0(GenCorrSignal)
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("%s_%s_%s%s_nominalOrig" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[i],getHistoSuffix(signaltag)));
		GENSignal=SignalRunFile.Get("%s_%s_%s%s_genMHT" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[i],getHistoSuffix(signaltag)));
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
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("%s_%s_%s%s_nominalOrig" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[i],getHistoSuffix(signaltag)));
		SignalRun.Scale(lumiscales[i])
		SignalRun.SetName("%s_%s" %(signaltag,yearsToCombine[i]))
		if "MC2018" in yearsToCombine[i] and not "MC2018HEM" in yearsToCombine[i]:
			MergedCorrelated=SignalRun.Clone("MergedCorrelated");
			SignalRunFileHEM=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i+1]))
			SignalRunHEM=SignalRunFileHEM.Get("%s_%s_%s%s_nominalOrig" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[i+1],getHistoSuffix(signaltag)))
			SignalRunHEM.Scale(lumiscales[i+1])
			SignalRunHEM.SetName("%s_%s" %(signaltag,yearsToCombine[i+1]))
			SignalRunHEMOrig = SignalRunHEM.Clone("HEMOrig")
			SignalRunHEM.Add(MergedCorrelated)
			def _fn(bN,b1):
				SignalRunHEM.SetBinError(bN, MergedCorrelated.GetBinError(bN)+SignalRunHEMOrig.GetBinError(bN))
			loopTHN(SignalRunHEM,_fn)

		if "MC2018HEM" in yearsToCombine[i]:continue
		if i==0:
			MergedSignal = SignalRun
			SetDirectory0(MergedSignal)
		else:
			MergedSignal.Add(SignalRun);
		SignalRunFile.Close();

	MergedSignal.SetName("RA2bin_%s%s_nominalOrig" %(signaltag,getHistoSuffix(signaltag)))
	return MergedSignal;

def MergeUncUncorrelated(signaldirtag,signaltag, yearsToCombine, lumiscales,Unc,MergedFullRun2):
	print(Unc)
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[0]))
	MergedUnc=SigTempFile.Get("%s_%s_%s%s_%s" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[0],getHistoSuffix(signaltag),Unc))
	SetDirectory0(MergedUnc)
	SigTempFile.Close();
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("%s_%s_%s%s_nominalOrig" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[i],getHistoSuffix(signaltag)));
		SignalRunUnc=SignalRunFile.Get("%s_%s_%s%s_%s" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[i],getHistoSuffix(signaltag),Unc));
		SignalRun.Scale(lumiscales[i])
		def _fn(bN,b1):
			UncQuadSum=(abs(MergedUnc.GetBinContent(bN)) if i>0 else 0)+pow((SignalRun.GetBinContent(bN)*abs(1-SignalRunUnc.GetBinContent(bN))),2);
			if SignalRunUnc.GetBinContent(bN)>=1.0: sign = 1.0
			else: sign = -1.0
			MergedUnc.SetBinContent(bN, sign*UncQuadSum);
		loopTHN(MergedUnc,_fn)
		SignalRunFile.Close();
	def _fn(bN,b1):
		MergedUncContent = MergedUnc.GetBinContent(bN)
		if MergedUncContent>=1.0: sign = 1.0
		else: sign = -1.0
		MergedUncContent = abs(MergedUncContent)
		if MergedUncContent>0:
			MergedUnc.SetBinContent(bN,1.0+sign*(sqrt(MergedUncContent)/MergedFullRun2.GetBinContent(bN)));
		else: MergedUnc.SetBinContent(bN,1.0);
	loopTHN(MergedUnc,_fn)
	return MergedUnc;

def MergeUncCorrelated(signaldirtag,signaltag, yearsToCombine, lumiscales,Unc,MergedFullRun2,isUp):
	print(Unc)
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[0]))
	MergedUnc=SigTempFile.Get("%s_%s_%s%s_%s" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[0],getHistoSuffix(signaltag),Unc))
	SetDirectory0(MergedUnc)
	SigTempFile.Close();
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("%s_%s_%s%s_nominalOrig" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[i],getHistoSuffix(signaltag)));
		SignalRunUnc=SignalRunFile.Get("%s_%s_%s%s_%s" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[i],getHistoSuffix(signaltag),Unc));
		SignalRun.Scale(lumiscales[i])
		def _fn(bN,b1):
			UncQuadSum=(MergedUnc.GetBinContent(bN) if i>0 else 0)+(SignalRun.GetBinContent(bN)*abs(1-SignalRunUnc.GetBinContent(bN)));
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
	print(Unc)
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[0]))
	MergedUnc=SigTempFile.Get("%s_%s_%s%s_%s" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[0],getHistoSuffix(signaltag),Unc))
	SetDirectory0(MergedUnc)
	SigTempFile.Close();
	for i in range(len(yearsToCombine)):
		if "2018" in yearsToCombine[i]:continue #NO Prefire unc
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("%s_%s_%s%s_nominalOrig" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[i],getHistoSuffix(signaltag)));
		SignalRunUnc=SignalRunFile.Get("%s_%s_%s%s_%s" %(getHistoPrefix(signaltag),signaltag,yearsToCombine[i],getHistoSuffix(signaltag),Unc));
		SignalRun.Scale(lumiscales[i])
		def _fn(bN,b1):
			UncQuadSum=(MergedUnc.GetBinContent(bN) if i>0 else 0)+(SignalRun.GetBinContent(bN)*abs(1-SignalRunUnc.GetBinContent(bN)));
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
