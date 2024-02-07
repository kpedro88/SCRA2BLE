import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
import os
from searchRegion import *
from singleBin import *
from cardUtilities import *
#from GenMHTCorrection import *
from SignalMergePeriods import *
import argparse

#########################################################################################################
## to do:
## .......
#########################################################################################################
#options.signal[2:] returns 3rd to end of list(as list index starts from zero)
def NominalSignal(inputfile,signal,mGo,mLSP,yearsToMerge,RunLumi):
	sms="%s_%s_%s" %(signal, mGo,mLSP)
	MergedFullRun2=MergeSignal(inputfile,sms,yearsToMerge,RunLumi);
	MergedFullRun2.SetName("RA2bin_%s_fast_nominalOrig" %(sms))
	MHTCorr_Unc=[]
	if "T1tttt" in signal or "T2tt" in signal or "T5qqqqVV" in signal:MHTCorr_Unc=SubtractSignalContamination(signaldirtag,signal,mGo, mLSP,yearsToMerge,RunLumi)
	else:MHTCorr_Unc=MHTSystematicGenMHT(signaldirtag,sms, yearsToMerge,RunLumi);
	return MHTCorr_Unc
def WriteSignalSystematics(signaldirtag,signal,mGo,mLSP,yearsToMerge,RunLumi,searchRegion):
	sms="%s_%s_%s" %(signal, mGo,mLSP)
	MergedNominal=MergeSignal(signaldirtag,sms,yearsToMerge,RunLumi);
	#MergedNominal.SetName("NominalOrig")
	#MergedNominal.SetDirectory(0)
	SigTempFile=TFile.Open(signaldirtag+"/RA2bin_proc_%s_MC2016_fast.root" %(sms))
	#MCStatErr=TH1D();#RA2bin_T1tttt_950_500_MC2016_fast_MCStatErr
	MCStatErr=SigTempFile.Get("RA2bin_%s_MC2016_fast_MCStatErr" %sms);
	MCStatErr.Reset();
	for i in range(1, MergedNominal.GetNbinsX()+1):
		#MCStatErr.GetXaxis().SetBinLabel(i, "MCStatErr"+MCStatErr.GetXaxis().GetBinLabel(i))
		StatErr=MergedNominal.GetBinError(i);
		if StatErr<=0 or MergedNominal.GetBinContent(i)<=0:StatErr=1.0;
		else:
			StatErr=1.0+(StatErr/MergedNominal.GetBinContent(i))
		MCStatErr.SetBinContent(i, StatErr);
	#Symmetric Norm Uncertainties
	signalRegion.addSystematicsLine('lnN',['sig'], MCStatErr);
	SigTempFile.Close();
	LumiUnc=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"lumiuncUp",MergedNominal,True)
	JetIDUnc=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"jetiduncUp",MergedNominal,True)
	IsoTrackUnc=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isotrackuncUp",MergedNominal,True)
	PrefireUncUp=MergeUncPreFireCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"prefireuncUp",MergedNominal,True)
	PrefireUncDown=MergeUncPreFireCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"prefireuncDown",MergedNominal,False)
	ISRUncUp=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isruncUp",MergedNominal,True)
	ISRUncDown=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"isruncDown",MergedNominal,False)
	TrigUnc=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"triguncUp",MergedNominal)
	TrigSysUnc=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"trigsystuncUp;",MergedNominal)
	searchRegion.addSystematicsLine('lnN',['sig'],LumiUnc)
	searchRegion.addSystematicsLine('lnN',['sig'],JetIDUnc)
	searchRegion.addSystematicsLine('lnN',['sig'],IsoTrackUnc)
	searchRegion.addSystematicsLine('lnN',['sig'],TrigUnc)
	searchRegion.addSystematicsLine('lnN',['sig'],TrigSysUnc)
	PUUncUp=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"puuncUp",MergedNominal,True)
	#searchRegion.addSystematicsLine('lnN',['sig'],PUUncUp)
	PUUncDown=MergeUncCorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"puuncDown",MergedNominal,False)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],PUUncUp,PUUncDown)
	ScaleUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"scaleuncUp",MergedNominal)
	JERUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JERup",MergedNominal)
	JECUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JECup",MergedNominal)

	BTagSFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagSFuncUp",MergedNominal)
	MisTagSFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagSFuncUp",MergedNominal)
	CTagCFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"ctagCFuncUp",MergedNominal)
	BTagCFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagCFuncUp",MergedNominal)
	MisTagCFUncUp=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagCFuncUp",MergedNominal)

	ScaleUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"scaleuncDown",MergedNominal)
	JERUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JERdown",MergedNominal)
	JECUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"JECdown",MergedNominal)
	BTagSFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagSFuncDown",MergedNominal)
	MisTagSFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagSFuncDown",MergedNominal)
	BTagCFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"btagCFuncDown",MergedNominal)
	CTagCFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"ctagCFuncDown",MergedNominal)
	MisTagCFUncDown=MergeUncUncorrelated(signaldirtag,sms,yearsToMerge,RunLumi,"mistagCFuncDown",MergedNominal)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],MisTagCFUncDown,MisTagCFUncUp)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],BTagCFUncDown,BTagCFUncUp)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],CTagCFUncDown,CTagCFUncUp)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],MisTagSFUncDown,MisTagSFUncUp)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],BTagSFUncDown,BTagSFUncUp)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],JERUncDown,JERUncUp)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],JECUncDown,JECUncUp)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],ScaleUncDown,ScaleUncUp)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],ISRUncDown,ISRUncUp)
	searchRegion.addSystematicsLineAsymShape('lnN',['sig'],PrefireUncDown,PrefireUncUp)

def WriteZSystematics(inputfile,CSSystematics,SymSystematics,AsymSystematics,signalRegion):
	Z_file=TFile.Open(inputfile)
	GammaObs=Z_file.Get(CSSystematics[1])
	#GammaObs.Scale(61.9*1000./(35916.403 +41521.425+21000.905+38196.951))#####BE CAREFUL This is hard coded
	ZRatios=Z_file.Get(CSSystematics[0])
	signalRegion.addGammaSystematic(['zvv'],GammaObs,ZRatios )
	for z in SymSystematics:
		hsyst=Z_file.Get(z)
		signalRegion.addSystematicsLine('lnN',['zvv'],hsyst)
	#print GammaObs.GetBinContent(1),ZRatios.GetBinContent(1)
	for i in range(len(AsymSystematics)):
		if i%2==0:
			UpSyst=Z_file.Get(AsymSystematics[i+1])
			DownSyst=Z_file.Get(AsymSystematics[i])
			signalRegion.addSystematicsLineAsymShape('lnN',['zvv'],DownSyst,UpSyst)
	Z_file.Close()
def WriteQCDSystematics(inputfile,ListOfSystematics,signalRegion,tagsForSignalRegion):
	QCD_file=TFile.Open(inputfile);
	for syst in ListOfSystematics:
		hTempSyst=QCD_file.Get(syst)
		if "Uncorrelated" in syst:
			for i in range(1,175):hTempSyst.GetXaxis().SetBinLabel(i,"QCDUncorrel"+tagsForSignalRegion[i-1])
		if "PredictionBTag" in syst:
			for i in range(1,175):
				if hTempSyst.GetBinContent(i)<0.0001:hTempSyst.SetBinContent(i,1.0)
				else: hTempSyst.SetBinContent(i,hTempSyst.GetBinContent(i));
		signalRegion.addSystematicsLine('lnN',['qcd'], hTempSyst);

	QCD_file.Close();
def WriteLostLeptonSystematics(inputfile, ListOfSystematics,signalRegion):
	LLPlusHadTauAvg_file=TFile.Open(inputfile);
	for syst in ListOfSystematics:
		hTempSyst=LLPlusHadTauAvg_file.Get(syst)
		#All symmetric systematics for log-normal
		if syst is not "DataCSStatistics" and syst is not "LLPlusHadTauTF":
			signalRegion.addSystematicsLine('lnN',['WTop'],hTempSyst)

	LLPlusHadTauControlStatistics=LLPlusHadTauAvg_file.Get("DataCSStatistics")
	#LLPlusHadTauControlStatistics.Scale(61.9*1000./(35916.403 +41521.425+21000.905+38196.951))#####BE CAREFUL This is hard coded
	LLPlusHadTauTF=LLPlusHadTauAvg_file.Get("LLPlusHadTauTF")
	signalRegion.addGammaSystematic(['WTop'],LLPlusHadTauControlStatistics,LLPlusHadTauTF)

	LLPlusHadTauAvg_file.Close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	#AR-180426: When parse_args() returns from parsing this command line,options.signal will be "SMSqqqq1000", options.fastsim will be "false" in default case
	#AR-180426:sample command to run this script, coming from analysisBuilderCondor.py will be: python analysisBuilderCondor.py --signal T1tttt --mGo 1500 --mLSP 100 --fastsim --realData  --tag allBkgs
	parser.add_argument("--signal", dest="signal", default = '', required=True, help="model name (e.g. T1tttt)", metavar="signal")
	parser.add_argument("--lumi", dest="lumi", default = 10.,help="luminosity in fb-1", metavar="lumi")
	parser.add_argument("--mGo", dest="mGo", default='1000', help="Mass of Gluino", metavar="mGo")
	parser.add_argument("--mLSP", dest="mLSP", default='900', help="Mass of LSP", metavar="mLSP")
	parser.add_argument('--fastsim', action='store_true', dest='fastsim', default=False, help='use fastsim signal')
	parser.add_argument('--realData',action='store_true', dest='realData', default=False, help='use real data')
	parser.add_argument('--sigDir',dest="sigDir", default="root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/",metavar="sigDir")
	options = parser.parse_args()
	#print options
	#exit(0)
	sms = "SMS"+options.signal[2:]+options.mGo;
	#AR-180426:when "fastsim" is true, sms=T1tttt_1500_100
	if options.fastsim: sms = options.signal+'_'+options.mGo+'_'+options.mLSP;
	lumi = float(options.lumi);

	odir = 'testCards-Moriond-%s-%1.1f/' % ( sms, lumi );
	#AR-180426: idir=inputHistograms/histograms_137fb/. Here are various background estimates.
	idir = 'inputHistograms/histograms_%1.1ffb/' % ( ((lumi)) );
	print idir
	#AR-180426:os.path.exists(odir):Return True if path refers to an existing path. Returns False for broken symbolic links.
	#forcefully remove directory if it exists
	if os.path.exists(odir): os.system( "rm -rf %s" % (odir) );
	#Symbol: os.makedirs(path[, mode]), ex. os.makedirs( path, 0755 ). Default mode is octal
	os.makedirs(odir);


	######################################################################
	######################################################################
	## 1. Get the input histograms from each of the background teams
	######################################################################
	######################################################################

	# --------------------------------------------
	# signal
	###Directory containing signal histograms like:"root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/"
	signaldirtag =options.sigDir
	##### Default the code accepts multiple Run Eras for the bkg inputs, signal inputs (but these list can have one item for a single/merged run era;
	yearsToMerge=["MC2016","MC2017","MC2018", "MC2018HEM"]
	RunLumi=[ 35916.403 , 41521.425,21000.905,38196.951 ]
	#Parent and LSP masses
	mLSP=int(options.mLSP)
	mGo=int(options.mGo)
	inputsigtag=options.signal
	TestNominal=NominalSignal(signaldirtag,inputsigtag,mGo,mLSP,yearsToMerge,RunLumi)
	signaltag="RA2bin_"+sms;
	#AR-180427:Here signaltag becomes "RA2bin_T1tttt_1500_100_fast
	if options.fastsim:signaltag+"_fast";
	print "%s_nominal" %signaltag
	#AR-180427:Gets signal nominal yield histogram "RA2bin_T1tttt_1500_100_fast_nominal" and scale it to "lumi*1000". This implies histogram root file corresponds to lumi of 1/pb.
	CorrSigHist=TestNominal[0]#signal_inputfile.Get("%s_nominal" %signaltag)
	CorrSigHist.SetDirectory(0)
	#signal_inputfile.Close();

	#AR-180515: Return bin labels of histogram like ['NJets0_BTags0_MHT0_HT0', 'NJets0_BTags0_MHT0_HT1'....]
	tagsForSignalRegion = binLabelsToList(CorrSigHist);
	contributionsPerBin = [];
	Data_List=[]
	for i in range(len(tagsForSignalRegion)):
		tmpcontributions = [];
		tmpcontributions.append('sig');
		tmpcontributions.append('WTop');
		tmpcontributions.append('zvv')
		tmpcontributions.append('qcd')
		contributionsPerBin.append(tmpcontributions) #AR: contributionsPerBin has saved seven elements' list per bin
	signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)
	if options.realData:
		DataHist_In=TFile.Open("inputHistograms/histograms_%1.1ffb/RA2bin_signalUnblindMerged.root" %lumi)
		Data_Hist=DataHist_In.Get("RA2bin_data_Unblind")
		Data_Hist.SetDirectory(0);
		Data_List=binsToList(Data_Hist) # creates a list of bin content
		DataHist_In.Close();
	#AR-180427: reads data prediction histograms related to LL:totalPred_LL, avgWeight_0L1L,ControlStatUnc.
	LLPlusHadTauAvg_file=TFile.Open("inputHistograms/histograms_137.4fb/InputsForLimits_data_formatted_LLPlusHadTau.root");
	LLPlusHadTauPrediction_Hist=LLPlusHadTauAvg_file.Get("totalPred_LLPlusHadTau")
	LLPlusHadTauPrediction_Hist.SetDirectory(0)
	LLPlusHadTauAvg_file.Close();
	### Central Values of Prediction for QCD
	ratesForSignalRegion_QCDList = [];
	QCDInputFile=TFile.Open(idir+"/QcdPredictionRandS.root")
	qcdCV=QCDInputFile.Get("PredictionCV")
	qcdCV.SetDirectory(0)
	QCDInputFile.Close();
	### Central Values of Prediction for Zvv
	Zinputfile = TFile.Open(idir+"ZinvHistos.root","READ")
	ZPred=Zinputfile.Get("ZinvBGpred")
	ZPred.SetDirectory(0);
	Zinputfile.Close()
	###### If data is blinded then set observation to the total background
	if not options.realData:
		for i in range(signalRegion._nBins): #174, (0-173)
			srobs=(ZPred.GetBinContent(i+1)+LLPlusHadTauPrediction_Hist.GetBinContent(i+1)+(qcdCV.GetBinContent(i+1)))
			Data_List.append(srobs)
	####Create an output file of signal, bkg, and data yields for debugging
	f = TFile(odir+'yields.root', 'recreate')
	data = TH1F( 'data', 'data', 174, 0, 174 )
	qcd = TH1F( 'QCD', 'QCD', 174, 0, 174 )
	zvv = TH1F( 'Zvv', 'Zvv', 174, 0, 174 )
	ll = TH1F( 'LL', 'LL', 174, 0, 174 )
	sig = TH1F( 'sig', 'sig', 174, 0, 174 )
	#print " contributionsPerBin ",contributionsPerBin
	#*AR:180515- creates instance of searchRegion class(signalRegion ), which will be a list of singleBins, with each single bin being referred by name='signali', tag='NJets0_BTags0_MHT0_HT1' etc., binLabels=tmpcontributions, index=bin number, rate=[], allLines = []

	signalRegion_Rates = [];
	signalRegion_Obs = [];
	#*AR:180515-Reads data histogram containing number of events per search bin
	tmpList = [];
	for i in range(signalRegion._nBins): #174, (0-173)
		srobs = 0;
		#tmpList has signal yield, LL prediction, it's avg TF, hadtau prediction, 0.25, Z prediction and QCD prediction
		tmpList = [];

		tmpList.append(CorrSigHist.GetBinContent(i+1)) #signal nominal yield
		tmpList.append(LLPlusHadTauPrediction_Hist.GetBinContent(i+1))
		tmpList.append(ZPred.GetBinContent(i+1))
		tmpList.append( qcdCV.GetBinContent(i+1) )
		#AR-180515: Just filling bin contents from bkg predictions. I think the purpose is to adjust bin centre.
		qcd.Fill(i+.5,  qcdCV.GetBinContent(i+1))
		zvv.Fill(i+.5, ZPred.GetBinContent(i+1))
		ll.Fill(i+.5, + LLPlusHadTauPrediction_Hist.GetBinContent(i+1))
#AR-180515:sig histogram is now the one scaled to 35.9/fb and not corresponding to 1/pb
		sig.Fill(i+.5,CorrSigHist.GetBinContent(i+1))
		srobs=Data_List[i] # dta events in ith bin
#tmpList has LL prediction, it's avg TF, hadtau prediction, 0.25, Z prediction and QCD prediction
		signalRegion_Rates.append(tmpList)
		signalRegion_Obs.append(srobs) # dta events in ith bin
		data.Fill(i+.5, srobs)

	signalRegion.fillRates(signalRegion_Rates ); # fills signal yield, LL prediction, it's avg TF, hadtau prediction, 0.25, Z prediction and QCD prediction in all 174 bins. 
	signalRegion.setObservedManually(signalRegion_Obs) # dta events in all 174 bins
	#*AR:180515- signalRegion is instance of searchRegion class, which will be a list of singleBins, with each single bin being referred by name='signali', tag='NJets0_BTags0_MHT0_HT1' etc., binLabels=tmpcontributions(length=174*7), index=bin number, rate=signalRegion_Rates.

	signalRegion.writeRates();
	f.Write()
	f.Close() #closes yields.root with data, signal and background histograms
	########################


	#######################
	#Get Histograms:
#AR-180515:signaltag=RA2bin_T1tttt_1500_100_fast
	LLSystematicsList=["LLPlusHadTauTF","DataCSStatistics","LLPlusHadTauTFErr","totalPredBMistagDown_LLPlusHadTau","totalPredJECSysDown_LLPlusHadTau","totalPredMTSysDown_LL","totalPredPDFDown_LLPlusHadTau","totalPredScaleDown_LLPlusHadTau","totalPredEleIDSysDown_LL","totalPredEleIsoSysDown_LL","totalPredEleRecoSysDown_LL","totalPredMuIsoSysDown_LL","totalPredMuIDSysDown_LL"]

	WriteLostLeptonSystematics(idir+"/InputsForLimits_data_formatted_LLPlusHadTau.root",LLSystematicsList,signalRegion)
	QCDSystematics=["PredictionCore","hSyst_tail","PredictionUncorrelated","PredictionBTag"]
	WriteQCDSystematics(idir+"/QcdPredictionRandS.root",QCDSystematics,signalRegion,tagsForSignalRegion)
	ZSystematicsCS=["hzvvTF","hzvvgJNobs"]
	ZSystematicsSym=["hzvvgJEtrgErr","hzvvgJPurErr","hzvvScaleErr","hzvvDYsysPur","hzvvDYstat","hzvvDYsysKin"]
	ZSystematicsASym=["hzvvNbCorrelUp","hzvvNbCorrelLow","hzvvDYMCerrLow","hzvvDYMCerrUp"]
	WriteZSystematics(idir+"ZinvHistos.root",ZSystematicsCS,ZSystematicsSym,ZSystematicsASym,signalRegion)
	#Signal Systematics
	signaltag = "RA2bin_proc_"+sms+"_Merged";
	signaltag+="_fast"
	signaltag="RA2bin_"+sms+"_fast";
	#MHTSyst=TestNominal[1]#signal_inputfile.Get(signaltag+"_MHTSyst")
	signalRegion.addSystematicsLine('lnU',['sig'],TestNominal[1]);
	#AR-180516:Gets various systematics histograms associated to signal nominal yield histogram "RA2bin_T1tttt_1500_100_fast_nominal"
	inputsigtag=options.signal
	WriteSignalSystematics(signaldirtag,inputsigtag,mGo,mLSP,yearsToMerge,RunLumi,signalRegion)

	######################################################################
	######################################################################
	# 4. Write Cards
	######################################################################
	######################################################################

	print odir
	signalRegion.writeCards( odir );
