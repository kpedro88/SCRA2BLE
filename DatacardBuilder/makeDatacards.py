import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
import os
from singleBin import *
from cardUtilities import *
from searchRegion import *
from common import *
from SignalMergePeriods import SetDirectory0

def WriteSignalSystematics(sms,SigHists,signalRegion):
	#Symmetric Norm Uncertainties
	signalRegion.addSystematicsLine('lnN',['sig'],SigHists["MCStatErr"])
	signalRegion.addSystematicsLine('lnN',['sig'],SigHists["LumiUnc"])
	signalRegion.addSystematicsLine('lnN',['sig'],SigHists["JetIDUnc"])
	signalRegion.addSystematicsLine('lnN',['sig'],SigHists["IsoTrackUnc"])
	signalRegion.addSystematicsLine('lnN',['sig'],SigHists["TrigUnc"])
	signalRegion.addSystematicsLine('lnN',['sig'],SigHists["TrigSysUnc"])
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["PUUncUp"],SigHists["PUUncDown"])
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["MisTagCFUncDown"],SigHists["MisTagCFUncUp"])
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["BTagCFUncDown"],SigHists["BTagCFUncUp"])
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["CTagCFUncDown"],SigHists["CTagCFUncUp"])
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["MisTagSFUncDown"],SigHists["MisTagSFUncUp"])
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["BTagSFUncDown"],SigHists["BTagSFUncUp"])
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["JERUncDown"],SigHists["JERUncUp"])
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["JECUncDown"],SigHists["JECUncUp"])
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["ISRUncDown"],SigHists["ISRUncUp"])
	signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["PrefireUncDown"],SigHists["PrefireUncUp"])
	if "pMSSM" not in sms:
		signalRegion.addSystematicsLineAsymShape('lnN',['sig'],SigHists["ScaleUncDown"],SigHists["ScaleUncUp"])

def WriteZSystematics(inputfile,CSSystematics,SymSystematics,AsymSystematics,signalRegion):
	Z_file=TFile.Open(inputfile)
	GammaObs=Z_file.Get(CSSystematics[1])
	ZRatios=Z_file.Get(CSSystematics[0])
	signalRegion.addGammaSystematic(['zvv'],GammaObs,ZRatios )
	for z in SymSystematics:
		hsyst=Z_file.Get(z)
		signalRegion.addSystematicsLine('lnN',['zvv'],hsyst)
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
	LLPlusHadTauTF=LLPlusHadTauAvg_file.Get("LLPlusHadTauTF")
	signalRegion.addGammaSystematic(['WTop'],LLPlusHadTauControlStatistics,LLPlusHadTauTF)

	LLPlusHadTauAvg_file.Close()

def makeDatacards(options):
	SigTempFile=TFile.Open(options.sigDir+"/RA2bin_merge_%s_fast.root" %(options.smsIn))
	SigHists = {}
	for key in [k.GetName() for k in SigTempFile.GetListOfKeys()]:
		htmp = SigTempFile.Get(key)
		# project pMSSM model
		if options.params is not None:
			SigHists[key] = ProjectTHN(htmp, options.mGo, options.mLSP)
		else:
			SigHists[key] = htmp
		SetDirectory0(SigHists[key])
		# fix for missing bin labels
		if len(SigHists[key].GetXaxis().GetBinLabel(1))==0:
			for b in range(SigHists[key].GetNbinsX()):
				SigHists[key].GetXaxis().SetBinLabel(b+1,"signal_"+key)
	SigTempFile.Close()

	odir = 'testCards-Moriond-%s-%1.1f/' % ( options.sms, options.lumi );
	#AR-180426: idir=inputHistograms/histograms_137fb/. Here are various background estimates.
	idir = 'inputHistograms/histograms_%1.1ffb/' % ( options.lumi );
	if os.path.exists(odir): os.system( "rm -rf %s" % (odir) );
	os.makedirs(odir);

	#AR-180515: Return bin labels of histogram like ['NJets0_BTags0_MHT0_HT0', 'NJets0_BTags0_MHT0_HT1'....]
	tagsForSignalRegion = binLabelsToList(SigHists["nominalOrig"]);
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
		DataHist_In=TFile.Open("inputHistograms/histograms_%1.1ffb/RA2bin_signalUnblindMerged.root" %options.lumi)
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

		tmpList.append(SigHists["nominalOrig"].GetBinContent(i+1)) #signal nominal yield
		tmpList.append(LLPlusHadTauPrediction_Hist.GetBinContent(i+1))
		tmpList.append(ZPred.GetBinContent(i+1))
		tmpList.append( qcdCV.GetBinContent(i+1) )
		#AR-180515: Just filling bin contents from bkg predictions. I think the purpose is to adjust bin centre.
		qcd.Fill(i+.5,  qcdCV.GetBinContent(i+1))
		zvv.Fill(i+.5, ZPred.GetBinContent(i+1))
		ll.Fill(i+.5, + LLPlusHadTauPrediction_Hist.GetBinContent(i+1))
#AR-180515:sig histogram is now the one scaled to 35.9/fb and not corresponding to 1/pb
		sig.Fill(i+.5,SigHists["nominalOrig"].GetBinContent(i+1))
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
	signaltag = "RA2bin_proc_"+options.sms+"_Merged";
	signaltag+="_fast"
	signaltag="RA2bin_"+options.sms+"_fast";
	#MHTSyst=TestNominal[1]#signal_inputfile.Get(signaltag+"_MHTSyst")
	signalRegion.addSystematicsLine('lnU',['sig'],SigHists["MHTSyst"]);
	#AR-180516:Gets various systematics histograms associated to signal nominal yield histogram "RA2bin_T1tttt_1500_100_fast_nominal"
	WriteSignalSystematics(options.sms,SigHists,signalRegion)

	######################################################################
	######################################################################
	# 4. Write Cards
	######################################################################
	######################################################################

	print(odir)
	cards = signalRegion.writeCards( odir );

	command = ["combineCards.py"]+cards+["> "+odir+"/allcards.txt"]
	command = ' '.join(command)
	print(command)
	os.system(command)

	# disable for now because slow
#	combine_cmd = "text2workspace.py --X-allow-no-signal --X-allow-no-background {0}/allcards.txt -o {0}/allcards.root".format(odir)
#	print(combine_cmd)
#	os.system(combine_cmd)

if __name__ == '__main__':
	options = get_options(single=True)
	makeDatacards(options)
