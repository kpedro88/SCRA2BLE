from ROOT import *
from math import sqrt
import sys
'''
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--signal", dest="signal", default = 'SMSqqqq',help="mass of LSP", metavar="signal")
parser.add_option("--mGo", dest="mGo", default='1000', help="Mass of Gluino", metavar="mGo")
parser.add_option("--mLSP", dest="mLSP", default='900', help="Mass of LSP", metavar="mLSP")
(options, args) = parser.parse_args()
'''
def SubstractSignalContamination(signaldirtag,signalregion,mGo,mLSP, yearsToCombine, lumiscales):
	signaltag="%s_%s_%s" %(signalregion,mGo,mLSP)
	LLPlusHadTauAvg_file=TFile.Open("inputHistograms/histograms_137.4fb/InputsForLimits_data_formatted_LLPlusHadTau.root");
	LLPlusHadTauPrediction_AVGTF=LLPlusHadTauAvg_file.Get("LLPlusHadTauTF")
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(signaltag))
	NominalCorrSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_nominalOrig" %signaltag)#SignalRuns[0];#.Clone("MergedSignal");
	NominalCorrSignalUnc=SigTempFile.Get("RA2bin_%s_MC2016_fast_MHTSyst" %signaltag)#SignalRuns[0];#.Clone("MergedSignal");
	GenCorrSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_genMHT" %signaltag)#SignalRuns[0];#.Clone("MergedSignal");
	#SignalContaminReco.Scale(lumiscales[0]+lumiscales[1]+lumiscales[2]+lumiscales[3])
	#SignalContaminGEN.Scale(lumiscales[0]+lumiscales[1]+lumiscales[2]+lumiscales[3])
	SignalContaminReco=SigTempFile.Get("RA2bin_%s_MC2016_fast_SLm" %(signaltag))
	SignalContaminGEN=SigTempFile.Get("RA2bin_%s_MC2016_fast_SLm-genMHT" %(signaltag))
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
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("RA2bin_%s_%s_fast_nominalOrig" %(signaltag,yearsToCombine[i]));
		GENSignal=SignalRunFile.Get("RA2bin_%s_%s_fast_genMHT" %(signaltag,yearsToCombine[i]));
		SignalContaminRecoMu=SignalRunFile.Get("RA2bin_%s_%s_fast_SLm" %(signaltag,yearsToCombine[i]));
		SignalContaminGenMu=SignalRunFile.Get("RA2bin_%s_%s_fast_SLm-genMHT" %(signaltag,yearsToCombine[i]));
		SignalContaminRecoEle=SignalRunFile.Get("RA2bin_%s_%s_fast_SLe" %(signaltag,yearsToCombine[i]));
		SignalContaminGenEle=SignalRunFile.Get("RA2bin_%s_%s_fast_SLe-genMHT" %(signaltag,yearsToCombine[i]));

		SignalRun.Scale(lumiscales[i])
		SignalRun.SetName("%s_%s" %(signaltag,yearsToCombine[i]))
		GENSignal.Scale(lumiscales[i])
		GENSignal.SetName("Gen%s_%s" %(signaltag,yearsToCombine[i]))
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
	for b in range(1,NominalCorrSignal.GetNbinsX()+1):
		UnCorrSignal=NominalCorrSignal.GetBinContent(b)-(SignalContaminReco.GetBinContent(b)*LLPlusHadTauPrediction_AVGTF.GetBinContent(b))
		GenMHTCleaned=GenCorrSignal.GetBinContent(b)-(SignalContaminGEN.GetBinContent(b)*LLPlusHadTauPrediction_AVGTF.GetBinContent(b))
		NominalCorrSignal.SetBinContent(b, (UnCorrSignal+GenMHTCleaned)/2.)
		if NominalCorrSignal.GetBinContent(b)>0:NominalCorrSignalUnc.SetBinContent(b, 1.0+(abs(UnCorrSignal-GenMHTCleaned)/2.)/NominalCorrSignal.GetBinContent(b))
		else: NominalCorrSignalUnc.SetBinContent(b,1.0)
	MHTCorr=[]#[NominalCorrSignal,NominalCorrSignalUnc]
	MHTCorr.append(NominalCorrSignal)
	MHTCorr.append(NominalCorrSignalUnc)
	return MHTCorr

def SubstractSignalContaminationCrossCheck(signaldirtag,signalregion,mGo,mLSP, yearsToCombine, lumiscales):
	SignalContaminRecoFile=TFile.Open("inputHistograms/SignalContamin/Run2Legacy/%s_RecoMHT_SignalFiles_190215.root" %signalregion)
	SignalContaminReco=SignalContaminRecoFile.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo,mLSP))
	SignalContaminGENFile=TFile.Open("inputHistograms/SignalContamin/Run2Legacy/%s_GenMHT_SignalFiles_190215.root" %signalregion)
	SignalContaminGEN=SignalContaminGENFile.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo,mLSP))
	signaltag="%s_%s_%s" %(signalregion,mGo,mLSP)
	#SignalContaminReco.Scale(137.421*1000)
	#SignalContaminGEN.Scale(137.421*1000)
	SignalContaminReco.Scale(lumiscales[0]+lumiscales[1]+lumiscales[2]+lumiscales[3])
	SignalContaminGEN.Scale(lumiscales[0]+lumiscales[1]+lumiscales[2]+lumiscales[3])
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(signaltag))
	NominalCorrSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_nominalOrig" %signaltag)#SignalRuns[0];#.Clone("MergedSignal");
	NominalCorrSignalUnc=SigTempFile.Get("RA2bin_%s_MC2016_fast_MHTSyst" %signaltag)#SignalRuns[0];#.Clone("MergedSignal");
	GenCorrSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_genMHT" %signaltag)#SignalRuns[0];#.Clone("MergedSignal");
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
	for b in range(1,NominalCorrSignal.GetNbinsX()+1):
		UnCorrSignal=NominalCorrSignal.GetBinContent(b)-SignalContaminReco.GetBinContent(b)
		GenMHTCleaned=GenCorrSignal.GetBinContent(b)-SignalContaminGEN.GetBinContent(b)
		NominalCorrSignal.SetBinContent(b, (UnCorrSignal+GenMHTCleaned)/2.)
		if NominalCorrSignal.GetBinContent(b)>0:NominalCorrSignalUnc.SetBinContent(b, 1.0+(abs(UnCorrSignal-GenMHTCleaned)/2.)/NominalCorrSignal.GetBinContent(b))
		else: NominalCorrSignalUnc.SetBinContent(b,1.0)
	MHTCorr=[]#[NominalCorrSignal,NominalCorrSignalUnc]
	MHTCorr.append(NominalCorrSignal)
	MHTCorr.append(NominalCorrSignalUnc)
	return MHTCorr

	#for i in range(len(yearsToCombine)):
def MHTSystematicGenMHT(signaldirtag,signaltag, yearsToCombine,lumiscales):
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(signaltag))
	NominalCorrSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_nominalOrig" %signaltag)#SignalRuns[0];#.Clone("MergedSignal");
	NominalCorrSignalUnc=SigTempFile.Get("RA2bin_%s_MC2016_fast_MHTSyst" %signaltag)#SignalRuns[0];#.Clone("MergedSignal");
	GenCorrSignal=SigTempFile.Get("RA2bin_%s_MC2016_fast_genMHT" %signaltag)#SignalRuns[0];#.Clone("MergedSignal");
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
		#print SignalRun.Integral()
		SignalRunFile.Close();
	for b in range(1,NominalCorrSignal.GetNbinsX()+1):
			UnCorrSignal=NominalCorrSignal.GetBinContent(b)
			NominalCorrSignal.SetBinContent(b, (UnCorrSignal+GenCorrSignal.GetBinContent(b))/2.)
			if NominalCorrSignal.GetBinContent(b)>0:NominalCorrSignalUnc.SetBinContent(b, 1.0+(abs(UnCorrSignal-GenCorrSignal.GetBinContent(b))/2.)/NominalCorrSignal.GetBinContent(b))
			else:NominalCorrSignalUnc.SetBinContent(b, 1.0)
	MHTCorr=[]#[NominalCorrSignal,NominalCorrSignalUnc]
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
			#print "special case"
			MergedCorrelated=SignalRun.Clone("MergedCorrelated");
			SignalRunFileHEM=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i+1]))
			SignalRunHEM=SignalRunFileHEM.Get("RA2bin_%s_%s_fast_nominalOrig" %(signaltag,yearsToCombine[i+1]))
			SignalRunHEM.Scale(lumiscales[i+1])
			SignalRunHEM.SetName("%s_%s" %(signaltag,yearsToCombine[i+1]))
			for j in range(1, 175):
				SignalRun.SetBinContent(j, MergedCorrelated.GetBinContent(j)+SignalRunHEM.GetBinContent(j))
				SignalRun.SetBinError(j, MergedCorrelated.GetBinError(j)+SignalRunHEM.GetBinError(j))

		if "MC2018HEM" in yearsToCombine[i]:continue
		MergedSignal.Add(SignalRun);
		SignalRunFile.Close();

	MergedSignal.SetName("RA2bin_%s_fast_nominalOrig" %signaltag)
	return MergedSignal;
	#return MergedSignal

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
		#print SignalRunUnc
		#SignalRunFile.Close();
		SignalRun.Scale(lumiscales[i])
		sign=[]
		for b in range(1,MergedUnc.GetNbinsX()+1):
			UncQuadSum=MergedUnc.GetBinContent(b)+pow((SignalRun.GetBinContent(b)*abs(1-SignalRunUnc.GetBinContent(b))),2);
			#sign=1.0
			if SignalRunUnc.GetBinContent(b)>=1.0:sign.append(1.0)
			else: sign.append(-1.0)
			MergedUnc.SetBinContent(b, UncQuadSum);
		SignalRunFile.Close();
	#print sign;
	for b in range(1,MergedUnc.GetNbinsX()+1):
			if MergedUnc.GetBinContent(b)>0:
				MergedUnc.SetBinContent(b,1.0+sign[b-1]*(sqrt(MergedUnc.GetBinContent(b))/MergedFullRun2.GetBinContent(b)));
			else: MergedUnc.SetBinContent(b,1.0);
	return MergedUnc;
def MergeUncCorrelated(signaldirtag,signaltag, yearsToCombine, lumiscales,Unc,MergedFullRun2,isUp):
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(signaltag))
	MergedUnc=SigTempFile.Get("RA2bin_%s_MC2016_fast_%s" %(signaltag,Unc))
	MergedUnc.Reset();
	MergedUnc.SetDirectory(0)
	SigTempFile.Close();
	#for i in range(0,2):
	for i in range(len(yearsToCombine)):
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("RA2bin_%s_%s_fast_nominalOrig" %(signaltag,yearsToCombine[i]));
		SignalRunUnc=SignalRunFile.Get("RA2bin_%s_%s_fast_%s" %(signaltag,yearsToCombine[i],Unc));
		#for b in range(1,SignalRunUnc.GetNbinsX()+1):
			#if "lumi" in Unc and yearsToCombine[i]=="MC2017":
			#	SignalRunUnc.SetBinContent(b, 1.023);
		#SignalRunFile.Close();
		SignalRun.Scale(lumiscales[i])
		for b in range(1,MergedUnc.GetNbinsX()+1):
			UncQuadSum=MergedUnc.GetBinContent(b)+(SignalRun.GetBinContent(b)*abs(1-SignalRunUnc.GetBinContent(b)));
			MergedUnc.SetBinContent(b, UncQuadSum);
		SignalRunFile.Close();
	for b in range(1,MergedUnc.GetNbinsX()+1):
			if MergedFullRun2.GetBinContent(b)>0:
				if isUp :MergedUnc.SetBinContent(b,  1.0+(MergedUnc.GetBinContent(b))/MergedFullRun2.GetBinContent(b));
				else:MergedUnc.SetBinContent(b,  1.0-(MergedUnc.GetBinContent(b))/MergedFullRun2.GetBinContent(b));
			else: MergedUnc.SetBinContent(b,1.0);
	return MergedUnc;
def MergeUncPreFireCorrelated(signaldirtag,signaltag, yearsToCombine, lumiscales,Unc,MergedFullRun2,isUp):
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(signaltag))
	MergedUnc=SigTempFile.Get("RA2bin_%s_MC2016_fast_%s" %(signaltag,Unc))
	MergedUnc.Reset();
	MergedUnc.SetDirectory(0)
	SigTempFile.Close();
	#for i in range(0,2):
	for i in range(len(yearsToCombine)):
		if "2018" in yearsToCombine[i]:continue #NO Prefire unc
		SignalRunFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_%s_fast.root" %(signaltag,yearsToCombine[i]))
		SignalRun=SignalRunFile.Get("RA2bin_%s_%s_fast_nominalOrig" %(signaltag,yearsToCombine[i]));
		SignalRunUnc=SignalRunFile.Get("RA2bin_%s_%s_fast_%s" %(signaltag,yearsToCombine[i],Unc));
		#SignalRunFile.Close();
		SignalRun.Scale(lumiscales[i])
		for b in range(1,MergedUnc.GetNbinsX()+1):
			UncQuadSum=MergedUnc.GetBinContent(b)+(SignalRun.GetBinContent(b)*abs(1-SignalRunUnc.GetBinContent(b)));
			MergedUnc.SetBinContent(b, UncQuadSum);
		SignalRunFile.Close();
	for b in range(1,MergedUnc.GetNbinsX()+1):
			if MergedFullRun2.GetBinContent(b)>0:
				if isUp :MergedUnc.SetBinContent(b,  1.0+(MergedUnc.GetBinContent(b))/MergedFullRun2.GetBinContent(b));
				else:MergedUnc.SetBinContent(b,  1.0-(MergedUnc.GetBinContent(b))/MergedFullRun2.GetBinContent(b));
			else: MergedUnc.SetBinContent(b,1.0);
	return MergedUnc;

'''
if __name__ == '__main__':
	signal=options.signal
	mLSP=int(options.mLSP)
	mGo=int(options.mGo)
	sms="%s_%s_%s" %(signal, mGo,mLSP)#%(sys.argv[1],sys.argv[2],sys.argv[3])
	signaldirtag="inputHistograms/fastsimSignal%s/" %signal
	yearsToMerge=["MC2016","MC2017"]
	RunLumi=[35900., 101499.]
	#TestMerge=TH1D();
	MergedFullRun2=MergeSignal(signaldirtag,sms,yearsToMerge,RunLumi);
	MHTCorr_Unc=[]

	if "T1tttt" in signal or "T2tt" in signal or "T5qqqqVV" in signal:MHTCorr_Unc=SubstractSignalContamination(signaldirtag,signal,mGo, mLSP,yearsToMerge,RunLumi)
	else:MHTCorr_Unc=MHTSystematicGenMHT(signaldirtag,sms, yearsToMerge,RunLumi);
	MergedFullRun2.SetName("RA2bin_%s_fast_nominalOrig" %(sms))
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(sms))
	#MCStatErr=TH1D();#RA2bin_T1tttt_950_500_MC2016_fast_MCStatErr
	MCStatErr=SigTempFile.Get("RA2bin_%s_MC2016_fast_MCStatErr" %sms);
	MCStatErr.Reset();
	MCStatErr.SetDirectory(0);
	#Normalize computed unc by the total Nsig
	#Uncorrelated Signal Uncertainties
	#Correlated Signal Uncertainties

	LumiUncUp=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"lumiuncUp",MergedFullRun2,True)
	IsoTrackUncUp=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isotrackuncUp",MergedFullRun2,True)
	JetIDUncUp=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"jetiduncUp",MergedFullRun2,True)
	PrefireUncUp=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"prefireuncUp",MergedFullRun2,True)
	TrigUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"triguncUp",MergedFullRun2,True)

	#THESE NEED A DOWN UNCERTAINTY Because they are shape uncertainties
	#Uncorrelated Signal Uncertainties
	ScaleUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"scaleuncUp",MergedFullRun2,True)
	JERUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JERup",MergedFullRun2,True)
	JECUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JECup",MergedFullRun2,True)
	BTagSFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagSFuncUp",MergedFullRun2,True)
	MisTagSFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagSFuncUp",MergedFullRun2,True)
	ISRUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isruncUp",MergedFullRun2,True)

	ScaleUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"scaleuncDown",MergedFullRun2,False)
	JERUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JERdown",MergedFullRun2,False)
	JECUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JECdown",MergedFullRun2,False)
	BTagSFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagSFuncDown",MergedFullRun2,False)
	MisTagSFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagSFuncDown",MergedFullRun2,False)
	ISRUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isruncDown",MergedFullRun2,False)
	#print MergedFullRun2.GetBinContent(165)

	for i in range(1, MergedFullRun2.GetNbinsX()+1):
		MCStatErr.GetXaxis().SetBinLabel(i, "MCStatErr"+MCStatErr.GetXaxis().GetBinLabel(i))
		StatErr=MergedFullRun2.GetBinError(i);
		if StatErr==0:StatErr=1.0;
		else:
			StatErr=1.0+(StatErr/MergedFullRun2.GetBinContent(i))
		MCStatErr.SetBinContent(i, StatErr);
		#print StatErr
	fout=TFile("%s/RA2bin_proc_%s_Merged_fast.root" %(signaldirtag,sms), "RECREATE");
	#print MHTCorr_Unc[0].GetBinContent(164)
	#print type(MergedFullRun2)
	#print MergedFullRun2.GetName()
	#print gDirectory.GetName();
	MergedFullRun2.Write("RA2bin_%s_fast_nominalOrig" %sms)#Total Yields weighted to lumi
	JetIDUncUp.Write("RA2bin_%s_fast_jetidunc" %sms)
	TrigUncUp.Write("RA2bin_%s_fast_trigunc" %sms)
	MCStatErr.Write("RA2bin_%s_fast_MCStatErr" %sms);
	LumiUncUp.Write("RA2bin_%s_fast_lumiunc" %sms);
	IsoTrackUncUp.Write("RA2bin_%s_fast_isotrackunc" %sms)
	PrefireUncUp.Write("RA2bin_%s_fast_prefireunc" %(sms))

	ScaleUncUp.Write("RA2bin_%s_fast_scaleuncUp" %(sms))
	JERUncUp.Write("RA2bin_%s_fast_JERup" %sms)
	JECUncUp.Write("RA2bin_%s_fast_JECup" %sms)
	ISRUncUp.Write("RA2bin_%s_fast_isruncUp" %(sms))
	BTagSFUncUp.Write("RA2bin_%s_fast_btagSFuncUp" %sms)
	MisTagSFUncUp.Write("RA2bin_%s_fast_mistagSFuncUp" %sms)
	ScaleUncDown.Write("RA2bin_%s_fast_scaleuncDown" %(sms))
	JERUncDown.Write("RA2bin_%s_fast_JERdown" %sms)
	JECUncDown.Write("RA2bin_%s_fast_JECdown" %sms)
	ISRUncDown.Write("RA2bin_%s_fast_isruncDown" %(sms))
	BTagSFUncDown.Write("RA2bin_%s_fast_btagSFuncDown" %sms)
	MisTagSFUncDown.Write("RA2bin_%s_fast_mistagSFuncDown" %sms)
	MHTCorr_Unc[0].Write("RA2bin_%s_fast_nominal" %sms)
	MHTCorr_Unc[1].Write("RA2bin_%s_fast_MHTSyst" %sms)
'''
