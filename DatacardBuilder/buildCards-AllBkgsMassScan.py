from ROOT import *

import os
import math
import sys
from searchRegion import *
from singleBin import *
from cardUtilities import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option("--signal", dest="signal", default = 'SMSqqqq1000',help="mass of LSP", metavar="signal")
parser.add_option("--tag", dest="tag", default = 'SinglePhoton1',help="mass of LSP", metavar="tag")
parser.add_option("--mu", dest="mu", default = 1.,help="mass of LSP", metavar="mu")
parser.add_option("--lumi", dest="lumi", default = 10.,help="mass of LSP", metavar="lumi")
parser.add_option('--fastsim', action='store_true', dest='fastsim', default=False, help='no X11 windows')
parser.add_option('--realData', action='store_true', dest='realData', default=False, help='no X11 windows')

parser.add_option('--qcdOnly', action='store_true', dest='qcdOnly', default=False, help='no X11 windows')
parser.add_option('--zvvOnly', action='store_true', dest='zvvOnly', default=False, help='no X11 windows')
parser.add_option('--tauOnly', action='store_true', dest='tauOnly', default=False, help='no X11 windows')
parser.add_option('--llpOnly', action='store_true', dest='llpOnly', default=False, help='no X11 windows')
parser.add_option('--allBkgs', action='store_true', dest='allBkgs', default=False, help='no X11 windows')
parser.add_option("--mGo", dest="mGo", default='1000', help="Mass of Gluino", metavar="mGo")
parser.add_option("--mLSP", dest="mLSP", default='900', help="Mass of LSP", metavar="mLSP")
(options, args) = parser.parse_args()


#########################################################################################################
## to do:
## .......
#########################################################################################################
if __name__ == '__main__':

    sms = "SMS"+options.signal[2:]+options.mGo;
    if options.fastsim: sms = options.signal+'_'+options.mGo+'_'+options.mLSP;
    tag = options.tag;
    lumi = float(options.lumi);
    signalmu = float(options.mu);
    odir = 'testCards-%s-%s-%1.1f-mu%0.1f/' % ( tag,sms, lumi, signalmu );
    idir = 'inputHistograms/histograms_%1.1ffb/' % ( ((lumi)) );
    if os.path.exists(odir): os.system( "rm -r %s" % (odir) );
    os.makedirs(odir);

    print odir, signalmu

    ######################################################################
    ######################################################################
    ## 1. Get the input histograms from each of the background teams
    ######################################################################
    ######################################################################

    # --------------------------------------------
    # signal 
    signaldirtag = idir;
    if options.fastsim: signaldirtag += "/fastsimSignalScan";
    signaltag = "RA2bin_"+sms;
    parse=sms.split('_')
    model=parse[0]
    #print parse
    if options.fastsim: signaltag+="_fast"

    signalSFB_file =TFile(signaldirtag+"/RA2bin_signal.root");

    signalSysSFUp_file=TFile(signaldirtag+"/RA2bin_signal_btagSFuncUp.root");
    signalSysSFDown_file=TFile(signaldirtag+"/RA2bin_signal_btagSFuncDown.root");
    signalSysMisSFUp_file=TFile(signaldirtag+"/RA2bin_signal_mistagSFuncUp.root");
    signalSysMisSFDown_file=TFile(signaldirtag+"/RA2bin_signal_mistagSFuncDown.root");
    signalSysCharmSFUp_file=TFile(signaldirtag+"/RA2bin_signal_ctagSFuncUp.root");
    signalSysCharmSFDown_file=TFile(signaldirtag+"/RA2bin_signal_ctagSFuncDown.root");
    signalSysTrigSystUp_file=TFile(signaldirtag+"/RA2bin_signal_trigSystUncUp.root");
    signalSysTrigSystDown_file=TFile(signaldirtag+"/RA2bin_signal_trigSystUncDown.root");
    signalSysTrigStatUp_file=TFile(signaldirtag+"/RA2bin_signal_trigStatUncUp.root");
    signalSysTrigStatDown_file=TFile(signaldirtag+"/RA2bin_signal_trigStatUncDown.root");

    signalSysJECUp_file    =TFile(signaldirtag+"/RA2bin_signal_JECup.root");
    signalSysJECDown_file      =TFile(signaldirtag+"/RA2bin_signal_JECdown.root");
    signalSysScaleUp_file      =TFile(signaldirtag+"/RA2bin_signal_scaleuncUp.root");
    signalSysScaleDown_file    =TFile(signaldirtag+"/RA2bin_signal_scaleuncDown.root");
    signalSysPUUp_file     =TFile(signaldirtag+"/RA2bin_signal_puuncUp.root");
    signalSysPUDown_file       =TFile(signaldirtag+"/RA2bin_signal_puuncDown.root");
    signalSysPDFUp_file     =TFile(signaldirtag+"/RA2bin_signal_pdfuncUp.root");
    signalSysPDFDown_file       =TFile(signaldirtag+"/RA2bin_signal_pdfuncDown.root");
    signalSysISRUp_file     =TFile(signaldirtag+"/RA2bin_signal_isruncUp.root");
    signalSysISRDown_file       =TFile(signaldirtag+"/RA2bin_signal_isruncDown.root");
    signalRegion_sigHist      = signalSFB_file.Get(signaltag);
    tagsForSignalRegion = binLabelsToList(signalRegion_sigHist);

    signalRegion_sigHistSFUp      = signalSysSFUp_file.Get(signaltag);
    signalRegion_sigHistSFDown    = signalSysSFDown_file.Get(signaltag);
    signalRegion_sigHistMisSFUp   = signalSysMisSFUp_file.Get(signaltag)
    signalRegion_sigHistMisSFDown = signalSysMisSFDown_file.Get(signaltag)
    signalRegion_sigHistCharmSFUp   = signalSysCharmSFUp_file.Get(signaltag)
    signalRegion_sigHistCharmSFDown = signalSysCharmSFDown_file.Get(signaltag)
    signalRegion_sigHistTrigSystUp   = signalSysTrigSystUp_file.Get(signaltag)
    signalRegion_sigHistTrigSystDown = signalSysTrigSystDown_file.Get(signaltag)
    signalRegion_sigHistTrigStatUp   = signalSysTrigStatUp_file.Get(signaltag)
    signalRegion_sigHistTrigStatDown = signalSysTrigStatDown_file.Get(signaltag)
    signalSysISRUpHist =signalSysISRUp_file.Get(signaltag)
    signalSysISRDnHist =signalSysISRDown_file.Get(signaltag)

    signalSysISRUpHist.Scale(lumi/3.)
    signalSysISRDnHist.Scale(lumi/3.)
    signalRegion_sigHist.Scale(lumi/3.);
    signalRegion_sigHistSFUp.Scale(lumi/3.);
    signalRegion_sigHistSFDown.Scale(lumi/3.);
    signalRegion_sigHistMisSFUp.Scale(lumi/3.);
    signalRegion_sigHistMisSFDown.Scale(lumi/3.);
    signalRegion_sigHistCharmSFUp.Scale(lumi/3.);
    signalRegion_sigHistCharmSFDown.Scale(lumi/3.);
    signalRegion_sigHistTrigSystUp.Scale(lumi/3.);
    signalRegion_sigHistTrigSystDown.Scale(lumi/3.);
    signalRegion_sigHistTrigStatUp.Scale(lumi/3.);  
    signalRegion_sigHistTrigStatDown.Scale(lumi/3.);

    signalRegion_sigList = binsToList( signalRegion_sigHist );
    signalRegion_sigListMCstatErr = binsErrorsToList( signalRegion_sigHist );    
    signalRegion_sigListSFUp=binsToList( signalRegion_sigHistSFUp );
    signalRegion_sigListSFDown=binsToList( signalRegion_sigHistSFDown );
    signalRegion_sigListMisSFUp=binsToList( signalRegion_sigHistMisSFUp );
    signalRegion_sigListMisSFDown=binsToList( signalRegion_sigHistMisSFDown );
    signalRegion_sigListCharmSFUp=binsToList(   signalRegion_sigHistCharmSFUp );
    signalRegion_sigListCharmSFDown=binsToList( signalRegion_sigHistCharmSFDown );
    signalRegion_sigListTrigSystUp=binsToList( signalRegion_sigHistTrigSystUp );
    signalRegion_sigListTrigSystDown=binsToList( signalRegion_sigHistTrigSystDown );
    signalRegion_sigListTrigStatUp=binsToList( signalRegion_sigHistTrigStatUp );  
    signalRegion_sigListTrigStatDown=binsToList( signalRegion_sigHistTrigStatDown );
    signalRegion_sigHistJECUp     = signalSysJECUp_file.Get(signaltag);
    signalRegion_sigHistJECDown   = signalSysJECDown_file.Get(signaltag);
    signalRegion_sigHistScaleUp   = signalSysScaleUp_file.Get(signaltag);
    signalRegion_sigHistScaleDown = signalSysScaleDown_file.Get(signaltag);
    signalRegion_sigHistPUUp      = signalSysPUUp_file.Get(signaltag);
    signalRegion_sigHistPUDown    = signalSysPUDown_file.Get(signaltag);
    signalRegion_sigHistPDFUp      = signalSysPDFUp_file.Get(signaltag);
    signalRegion_sigHistPDFDown    = signalSysPDFDown_file.Get(signaltag);

    signalRegion_sigHistJECUp.Scale(lumi/3.);   
    signalRegion_sigHistJECDown.Scale(lumi/3.);   
    signalRegion_sigHistScaleUp.Scale(lumi/3.);   
    signalRegion_sigHistScaleDown.Scale(lumi/3.); 
    signalRegion_sigHistPUUp.Scale(lumi/3.);      
    signalRegion_sigHistPUDown.Scale(lumi/3.);    
    signalRegion_sigHistPDFUp.Scale(lumi/3.);      
    signalRegion_sigHistPDFDown.Scale(lumi/3.);    
    signalRegion_sigListJECUp     =binsToList( signalRegion_sigHistJECUp );
    signalRegion_sigListJECDown   =binsToList( signalRegion_sigHistJECDown );
    signalRegion_sigListScaleUp   =binsToList( signalRegion_sigHistScaleUp );
    signalRegion_sigListScaleDown =binsToList( signalRegion_sigHistScaleDown );
    signalRegion_sigListPUUp      =binsToList( signalRegion_sigHistPUUp );
    signalRegion_sigListPUDown    =binsToList( signalRegion_sigHistPUDown );
    signalRegion_sigListPDFUp      =binsToList( signalRegion_sigHistPDFUp );
    signalRegion_sigListPDFDown    =binsToList( signalRegion_sigHistPDFDown );
    signalRegion_sigListISRUp      =binsToList( signalSysISRUpHist );
    signalRegion_sigListISRDown    =binsToList( signalSysISRDnHist );

    signalRegion_sigListbtagCFuncUp = [];
    signalRegion_sigListbtagCFuncDown = [];
    signalRegion_sigListctagCFuncUp = [];
    signalRegion_sigListctagCFuncDown = [];
    signalRegion_sigListmistagCFuncUp = [];
    signalRegion_sigListmistagCFuncDown = [];

    if options.fastsim:

        signalSysbtagCFuncUp_file=TFile(signaldirtag+"/RA2bin_signal_btagCFuncUp.root");
        signalSysbtagCFuncDown_file=TFile(signaldirtag+"/RA2bin_signal_btagCFuncDown.root");
        signalSysctagCFuncUp_file=TFile(signaldirtag+"/RA2bin_signal_ctagCFuncUp.root");
        signalSysctagCFuncDown_file=TFile(signaldirtag+"/RA2bin_signal_ctagCFuncDown.root");
        signalSysmistagCFuncUp_file=TFile(signaldirtag+"/RA2bin_signal_mistagCFuncUp.root");
        signalSysmistagCFuncDown_file=TFile(signaldirtag+"/RA2bin_signal_mistagCFuncDown.root");

        signalRegion_sigHistbtagCFuncUp = signalSysbtagCFuncUp_file.Get(signaltag)
        signalRegion_sigHistbtagCFuncUp.Scale(lumi/3.);
        signalRegion_sigListbtagCFuncUp=binsToList( signalRegion_sigHistbtagCFuncUp );
        signalRegion_sigHistctagCFuncUp = signalSysctagCFuncUp_file.Get(signaltag)
        signalRegion_sigHistctagCFuncUp.Scale(lumi/3.);
        signalRegion_sigListctagCFuncUp=binsToList( signalRegion_sigHistctagCFuncUp );
        signalRegion_sigHistmistagCFuncUp = signalSysmistagCFuncUp_file.Get(signaltag)
        signalRegion_sigHistmistagCFuncUp.Scale(lumi/3.);
        signalRegion_sigListmistagCFuncUp=binsToList( signalRegion_sigHistmistagCFuncUp );    

        signalRegion_sigHistbtagCFuncDown = signalSysbtagCFuncDown_file.Get(signaltag)
        signalRegion_sigHistbtagCFuncDown.Scale(lumi/3.);
        signalRegion_sigListbtagCFuncDown=binsToList( signalRegion_sigHistbtagCFuncDown );
        signalRegion_sigHistctagCFuncDown = signalSysctagCFuncDown_file.Get(signaltag)
        signalRegion_sigHistctagCFuncDown.Scale(lumi/3.);
        signalRegion_sigListctagCFuncDown=binsToList( signalRegion_sigHistctagCFuncDown );
        signalRegion_sigHistmistagCFuncDown = signalSysmistagCFuncDown_file.Get(signaltag)
        signalRegion_sigHistmistagCFuncDown.Scale(lumi/3.);
        signalRegion_sigListmistagCFuncDown=binsToList( signalRegion_sigHistmistagCFuncDown );    
        
    # --------------------------------------------
    # z invisible
    sphotonRegion_file = TFile(idir+"/RA2bin_GJet_PhotonBins.root");

    DYinputfile = TFile(idir+"/ZinvHistos.root")
    signalRegion_zvvRatesFromDY = DYinputfile.Get("hDYvalue")
    signalRegion_zvvList = binsToList( signalRegion_zvvRatesFromDY );

    # --------------------------------------------
    # lost lepton
    LL_file = TFile(idir+"/LLPrediction.root");
    LLPrediction_Hist=LL_file.Get("Prediction_data/totalPred_LL");
    LLCS_Hist=LL_file.Get("Prediction_data/totalCS_LL");
    LLWeight_Hist=LL_file.Get("Prediction_data/avgWeight_LL");
    LLMCWeight_Hist=LL_file.Get("Prediction_MC/avgWeight_LL_MC");

    #stat Uncertainties on eff
    LLStatIsoTrackUp_Hist=LL_file.Get("Prediction_data/totalPredIsoTrackStatUp_LL")
    LLStatIsoTrackDown_Hist=LL_file.Get("Prediction_data/totalPredIsoTrackStatDown_LL")
    LLStatMTUp_Hist=LL_file.Get("Prediction_data/totalPredMTWStatUp_LL");
    LLStatMTDown_Hist=LL_file.Get("Prediction_data/totalPredMTWStatDown_LL");
    LLStatPurUp_Hist=LL_file.Get("Prediction_data/totalPredPurityStatUp_LL");    
    LLStatPurDown_Hist=LL_file.Get("Prediction_data/totalPredPurityStatDown_LL");
    LLStatSinglePurUp_Hist=LL_file.Get("Prediction_data/totalPredSingleLepPurityStatUp_LL");
    LLStatSinglePurDown_Hist=LL_file.Get("Prediction_data/totalPredSingleLepPurityStatDown_LL");
    LLStatDiLepPurUp_Hist=LL_file.Get("Prediction_data/totalPredDiLepFoundStatUp_LL")
    LLStatDiLepPurDown_Hist=LL_file.Get("Prediction_data/totalPredDiLepFoundStatDown_LL")
    LLStatMuIsoUp_Hist=LL_file.Get("Prediction_data/totalPredMuIsoStatUp_LL");
    LLStatMuIsoDown_Hist=LL_file.Get("Prediction_data/totalPredMuIsoStatDown_LL");
    LLStatMuRecoUp_Hist=LL_file.Get("Prediction_data/totalPredMuRecoStatUp_LL");
    LLStatMuRecoDown_Hist=LL_file.Get("Prediction_data/totalPredMuRecoStatDown_LL")
    LLStatMuAccUp_Hist=LL_file.Get("Prediction_data/totalPredMuAccStatUp_LL");
    LLStatMuAccDown_Hist=LL_file.Get("Prediction_data/totalPredMuAccStatDown_LL")
    LLStatElecIsoUp_Hist=LL_file.Get("Prediction_data/totalPredElecIsoStatUp_LL");
    LLStatElecIsoDown_Hist=LL_file.Get("Prediction_data/totalPredElecIsoStatDown_LL");
    LLStatElecRecoUp_Hist=LL_file.Get("Prediction_data/totalPredElecRecoStatUp_LL");
    LLStatElecRecoDown_Hist=LL_file.Get("Prediction_data/totalPredElecRecoStatDown_LL")
    LLStatElecAccUp_Hist=LL_file.Get("Prediction_data/totalPredElecAccStatUp_LL");
    LLStatElecAccDown_Hist=LL_file.Get("Prediction_data/totalPredElecAccStatDown_LL")

    #systematics
    LLSysIsoTrackUp_Hist=LL_file.Get("Prediction_data/totalPredIsoTrackSysUp_LL")
    LLSysIsoTrackDown_Hist=LL_file.Get("Prediction_data/totalPredIsoTrackSysDown_LL")
    LLSysMTUp_Hist=LL_file.Get("Prediction_data/totalPredMTWSysUp_LL");
    LLSysMTDown_Hist=LL_file.Get("Prediction_data/totalPredMTWSysDown_LL");
    LLSysPurUp_Hist=LL_file.Get("Prediction_data/totalPredPuritySysUp_LL");    
    LLSysPurDown_Hist=LL_file.Get("Prediction_data/totalPredPuritySysDown_LL");
    LLSysSinglePurUp_Hist=LL_file.Get("Prediction_data/totalPredSingleLepPuritySysUp_LL");
    LLSysSinglePurDown_Hist=LL_file.Get("Prediction_data/totalPredSingleLepPuritySysDown_LL");
    LLSysDiLepPurUp_Hist=LL_file.Get("Prediction_data/totalPredDiLepFoundSysUp_LL")
    LLSysDiLepPurDown_Hist=LL_file.Get("Prediction_data/totalPredDiLepFoundSysDown_LL")
    LLSysMuIsoUp_Hist=LL_file.Get("Prediction_data/totalPredMuIsoSysUp_LL");
    LLSysMuIsoDown_Hist=LL_file.Get("Prediction_data/totalPredMuIsoSysDown_LL");
    LLSysMuRecoUp_Hist=LL_file.Get("Prediction_data/totalPredMuRecoSysUp_LL");
    LLSysMuRecoDown_Hist=LL_file.Get("Prediction_data/totalPredMuRecoSysDown_LL")
    LLSysMuAccUp_Hist=LL_file.Get("Prediction_data/totalPredMuAccSysUp_LL");
    LLSysMuAccDown_Hist=LL_file.Get("Prediction_data/totalPredMuAccSysDown_LL")
    LLSysElecIsoUp_Hist=LL_file.Get("Prediction_data/totalPredElecIsoSysUp_LL");
    LLSysElecIsoDown_Hist=LL_file.Get("Prediction_data/totalPredElecIsoSysDown_LL");
    LLSysElecRecoUp_Hist=LL_file.Get("Prediction_data/totalPredElecRecoSysUp_LL");
    LLSysElecRecoDown_Hist=LL_file.Get("Prediction_data/totalPredElecRecoSysDown_LL")
    LLSysElecAccUp_Hist=LL_file.Get("Prediction_data/totalPredElecAccSysUp_LL");
    LLSysElecAccDown_Hist=LL_file.Get("Prediction_data/totalPredElecAccSysDown_LL")
    LLSysNCUp_Hist=LL_file.Get("Prediction_data/totalPredNonClosureUp_LL")
    LLSysNCDown_Hist=LL_file.Get("Prediction_data/totalPredNonClosureDown_LL")

    LLSysElecQSquareUp_Hist=LL_file.Get("Prediction_data/totalPredElecAccQsquareSysUp_LL");
    LLSysElecQSquareDown_Hist=LL_file.Get("Prediction_data/totalPredElecAccQsquareSysDown_LL")
    LLSysMuQSquareUp_Hist=LL_file.Get("Prediction_data/totalPredMuAccQsquareSysUp_LL");
    LLSysMuQSquareDown_Hist=LL_file.Get("Prediction_data/totalPredMuAccQsquareSysDown_LL")

    signalRegion_LLList = binsToList( LLPrediction_Hist );
    signalRegion_WeightList=binsToList(LLWeight_Hist);
    signalRegion_MCWeightList=binsToList(LLMCWeight_Hist);
    signalRegion_CSList=binsToList(LLCS_Hist)
    LLSysElecQSquareUp=binsToList(LLSysElecQSquareUp_Hist)
    LLSysElecQSquareDown=binsToList(LLSysElecQSquareDown_Hist)

    LLSysMuQSquareUp=binsToList(LLSysMuQSquareUp_Hist)
    LLSysMuQSquareDown=binsToList(LLSysMuQSquareDown_Hist)
    
    LLStatIsoTrackUp=binsToList(LLStatIsoTrackUp_Hist)
    LLStatIsoTrackDown=binsToList(LLStatIsoTrackDown_Hist)
    LLStatMTUp=binsToList(LLStatMTUp_Hist)    
    LLStatMTDown=binsToList(LLStatMTDown_Hist)    
    LLStatPurUp=binsToList(LLStatPurUp_Hist)
    LLStatPurDown=binsToList(LLStatPurDown_Hist)
    LLStatSinglePurUp=binsToList(LLStatSinglePurUp_Hist)
    LLStatSinglePurDown=binsToList(LLStatSinglePurDown_Hist)
    LLStatPurDown=binsToList(LLStatSinglePurDown_Hist)
    LLStatDiLepPurUp=binsToList(LLStatDiLepPurUp_Hist)
    LLStatDiLepPurDown=binsToList(LLStatDiLepPurDown_Hist)
    LLStatMuIsoUp=binsToList(LLStatMuIsoUp_Hist)
    LLStatMuIsoDown=binsToList(LLStatMuIsoDown_Hist)
    LLStatMuRecoUp=binsToList(LLStatMuRecoUp_Hist)
    LLStatMuRecoDown=binsToList(LLStatMuRecoDown_Hist)
    LLStatMuAccUp=binsToList(LLStatMuAccUp_Hist)
    LLStatMuAccDown=binsToList(LLStatMuAccDown_Hist)
    LLStatElecIsoUp=binsToList(LLStatElecIsoUp_Hist)
    LLStatElecIsoDown=binsToList(LLStatElecIsoDown_Hist)
    LLStatElecRecoUp=binsToList(LLStatElecRecoUp_Hist)
    LLStatElecRecoDown=binsToList(LLStatElecRecoDown_Hist)
    LLStatElecAccUp=binsToList(LLStatElecAccUp_Hist)
    LLStatElecAccDown=binsToList(LLStatElecAccDown_Hist)

    LLSysIsoTrackUp=binsToList(LLSysIsoTrackUp_Hist)
    LLSysIsoTrackDown=binsToList(LLSysIsoTrackDown_Hist)
    LLSysMTUp=binsToList(LLSysMTUp_Hist)    
    LLSysMTDown=binsToList(LLSysMTDown_Hist)    
    LLSysPurUp=binsToList(LLSysPurUp_Hist)
    LLSysPurDown=binsToList(LLSysPurDown_Hist)
    LLSysSinglePurUp=binsToList(LLSysSinglePurUp_Hist)
    LLSysSinglePurDown=binsToList(LLSysSinglePurDown_Hist)
    LLSysPurDown=binsToList(LLSysSinglePurDown_Hist)
    LLSysDiLepPurUp=binsToList(LLSysDiLepPurUp_Hist)
    LLSysDiLepPurDown=binsToList(LLSysDiLepPurDown_Hist)
    LLSysMuIsoUp=binsToList(LLSysMuIsoUp_Hist)
    LLSysMuIsoDown=binsToList(LLSysMuIsoDown_Hist)
    LLSysMuRecoUp=binsToList(LLSysMuRecoUp_Hist)
    LLSysMuRecoDown=binsToList(LLSysMuRecoDown_Hist)
    LLSysMuAccUp=binsToList(LLSysMuAccUp_Hist)
    LLSysMuAccDown=binsToList(LLSysMuAccDown_Hist)
    LLSysElecIsoUp=binsToList(LLSysElecIsoUp_Hist)
    LLSysElecIsoDown=binsToList(LLSysElecIsoDown_Hist)
    LLSysElecRecoUp=binsToList(LLSysElecRecoUp_Hist)
    LLSysElecRecoDown=binsToList(LLSysElecRecoDown_Hist)
    LLSysElecAccUp=binsToList(LLSysElecAccUp_Hist)
    LLSysElecAccDown=binsToList(LLSysElecAccDown_Hist)
    LLSysNCUp=binsToList(LLSysNCUp_Hist)
    LLSysNCDown=binsToList(LLSysNCDown_Hist)

    for i in range(len(LLSysNCUp)):
        if(LLSysMTUp[i]<-99 or signalRegion_CSList[i]<2): LLSysMTUp[i]=1.0;
        if(LLSysMTDown[i]<-99 or signalRegion_CSList[i]<2 ): LLSysMTDown[i]=1.0;
        if(LLSysIsoTrackUp[i]<-99 or signalRegion_CSList[i]<2):LLSysIsoTrackUp[i]=1.0
        if(LLSysIsoTrackDown[i]<-99 or signalRegion_CSList[i]<2):LLSysIsoTrackDown[i]=1.0
        if(LLSysPurUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysPurUp[i]=1.0;
        if(LLSysPurDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysPurDown[i]=1.0;
        if(LLSysSinglePurUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysSinglePurUp[i]=1.0;
        if(LLSysSinglePurDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysSinglePurDown[i]=1.0;
        if(LLSysDiLepPurUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysDiLepPurUp[i]=1.0;
        if(LLSysDiLepPurDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysDiLepPurDown[i]=1.0;
        if(LLSysMuIsoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuIsoUp[i]=1.0;
        if(LLSysMuIsoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuIsoDown[i]=1.0;
        if(LLSysMuRecoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuRecoUp[i]=1.0;
        if(LLSysMuRecoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuRecoDown[i]=1.0;
        if(LLSysMuAccUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuAccUp[i]=1.0;
        if(LLSysMuAccDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysMuAccDown[i]=1.0;
        if(LLSysElecIsoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecIsoUp[i]=1.0;
        if(LLSysElecIsoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecIsoDown[i]=1.0;
        if(LLSysElecRecoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecRecoUp[i]=1.0;
        if(LLSysElecRecoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecRecoDown[i]=1.0;
        if(LLSysElecAccUp[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecAccUp[i]=1.0;
        if(LLSysElecAccDown[i]<-99 or signalRegion_CSList[i]<2 ):LLSysElecAccDown[i]=1.0;
    
    
        if(LLStatMTUp[i]<-99 or signalRegion_CSList[i]<2): LLStatMTUp[i]=1.0;
        if(LLStatMTDown[i]<-99 or signalRegion_CSList[i]<2 ): LLStatMTDown[i]=1.0;
        if(LLStatIsoTrackUp[i]<-99 or signalRegion_CSList[i]<2):LLStatIsoTrackUp[i]=1.0
        if(LLStatIsoTrackDown[i]<-99 or signalRegion_CSList[i]<2):LLStatIsoTrackDown[i]=1.0
        if(LLStatPurUp[i]<-99 or signalRegion_CSList[i]<2 ):LLStatPurUp[i]=1.0;
        if(LLStatPurDown[i]<-99 or signalRegion_CSList[i]<2 ):LLStatPurDown[i]=1.0;
        if(LLStatSinglePurUp[i]<-99 or signalRegion_CSList[i]<2 ):LLStatSinglePurUp[i]=1.0;
        if(LLStatSinglePurDown[i]<-99 or signalRegion_CSList[i]<2 ):LLStatSinglePurDown[i]=1.0;
        if(LLStatDiLepPurUp[i]<-99 or signalRegion_CSList[i]<2 ):LLStatDiLepPurUp[i]=1.0;
        if(LLStatDiLepPurDown[i]<-99 or signalRegion_CSList[i]<2 ):LLStatDiLepPurDown[i]=1.0;
        if(LLStatMuIsoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLStatMuIsoUp[i]=1.0;
        if(LLStatMuIsoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLStatMuIsoDown[i]=1.0;
        if(LLStatMuRecoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLStatMuRecoUp[i]=1.0;
        if(LLStatMuRecoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLStatMuRecoDown[i]=1.0;
        if(LLStatMuAccUp[i]<-99 or signalRegion_CSList[i]<2 ):LLStatMuAccUp[i]=1.0;
        if(LLStatMuAccDown[i]<-99 or signalRegion_CSList[i]<2 ):LLStatMuAccDown[i]=1.0;
        if(LLStatElecIsoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLStatElecIsoUp[i]=1.0;
        if(LLStatElecIsoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLStatElecIsoDown[i]=1.0;
        if(LLStatElecRecoUp[i]<-99 or signalRegion_CSList[i]<2 ):LLStatElecRecoUp[i]=1.0;
        if(LLStatElecRecoDown[i]<-99 or signalRegion_CSList[i]<2 ):LLStatElecRecoDown[i]=1.0;
        if(LLStatElecAccUp[i]<-99 or signalRegion_CSList[i]<2 ):LLStatElecAccUp[i]=1.0;
        if(LLStatElecAccDown[i]<-99 or signalRegion_CSList[i]<2 ):LLStatElecAccDown[i]=1.0;
    
    #Also Get Sumw2 errors
    LLSumW2errors=[]
    for i in range(1,LLPrediction_Hist.GetNbinsX()+1):
        if(LLPrediction_Hist.GetBinError(i)>0.000000001):
            multError=LLPrediction_Hist.GetBinError(i)/(LLPrediction_Hist.GetBinContent(i))
            LLSumW2errors.append(1.0+multError);

        else: LLSumW2errors.append(1.0)

    # --------------------------------------------
    # hadronic tau
    HadTau_file = TFile(idir+"/HadTauEstimation_data.root");
    HadTauPrediction_Hist=HadTau_file.Get("searchBin_nominal")
    #HadTauSqrtSumw2_Hist=HadTauSumw_file.Get("SqrtSumW2")
    HadTauBMistagUp_Hist=HadTau_file.Get("searchBin_BMistagUp")    
    HadTauBMistagDown_Hist=HadTau_file.Get("searchBin_BMistagDn")
    HadTauSysNC_Hist=HadTau_file.Get("searchBin_closureUncertainty")
    signalRegion_tauList=binsToList(HadTauPrediction_Hist)
    tauNonClosure=binsToList(HadTauSysNC_Hist)
    tauBMistagUp=binsToList(HadTauBMistagUp_Hist)
    tauBMistagDown=binsToList(HadTauBMistagDown_Hist)    
    HadTauMuonCorrUncUpHist=HadTau_file.Get("searchBin_MuRecoSysUp")
    HadTauMuonCorrUncDnHist=HadTau_file.Get("searchBin_MuRecoSysDn")    
    HadTauMuonIsoRecoStatUncUpHist=HadTau_file.Get("searchBin_MuRecoIsoUp")
    HadTauMuonIsoRecoStatUncDnHist=HadTau_file.Get("searchBin_MuRecoIsoDn")
    HadTauMuonCorrIsoUncUpHist=HadTau_file.Get("searchBin_MuIsoSysUp")
    HadTauMuonCorrIsoUncDnHist=HadTau_file.Get("searchBin_MuIsoSysDn")
    HadTauStatUncertainties=HadTau_file.Get("searchBin_StatUncertainties")
    
    HadTauJECUncertUpHist=HadTau_file.Get("searchBin_JECSysUp")
    HadTauJECUncertDownHist=HadTau_file.Get("searchBin_JECSysDn")    

    HadTauMTSysUpHist=HadTau_file.Get("searchBin_MTSysUp")
    HadTauMTSysDownHist=HadTau_file.Get("searchBin_MTSysDn")
    HadTauMTEffHist=HadTau_file.Get("seaerchBin_MtEffStat")
    HadTauIsoTkEffHistStatHist=HadTau_file.Get("seaerchBin_IsoTrkVetoEffUncertaintyStat")
    HadTauIsoTkEffHistSysHist=HadTau_file.Get("seaerchBin_IsoTrkVetoEffUncertaintySys")
    HadTauAccStatHist=HadTau_file.Get("seaerchBin_AccStat")
    HadTauMuFromTauStatHist=HadTau_file.Get("seaerchBin_MuFromTauStat")
    HadTauMuDiLeptonHist=HadTau_file.Get("searchBin_DileptonUncertainty")
    HadTauMuAccSysPDFUpHist=HadTau_file.Get("seaerchBin_AccSysPDFUp")
    HadTauMuAccSysPDFDnHist=HadTau_file.Get("seaerchBin_AccSysPDFDn")
    HadTauMuAccSysScaleUpHist=HadTau_file.Get("seaerchBin_AccSysScaleUp")
    HadTauMuAccSysScaleDnHist=HadTau_file.Get("seaerchBin_AccSysScaleDn")
    HadTauMuonCorrUncUp=binsToList(HadTauMuonCorrUncUpHist)
    HadTauMuonCorrUncDn=binsToList(HadTauMuonCorrUncDnHist)
    HadTauMuonIsoRecoStatUncUp=binsToList(HadTauMuonIsoRecoStatUncUpHist)
    HadTauMuonIsoRecoStatUncDn=binsToList(HadTauMuonIsoRecoStatUncDnHist)
    HadTauMuonIsoUncUp=binsToList(HadTauMuonCorrIsoUncUpHist)
    HadTauMuonIsoUncDn=binsToList(HadTauMuonCorrIsoUncDnHist)
    HadTauJECUncertUp=binsToList(HadTauJECUncertUpHist)
    HadTauJECUncertDn=binsToList(HadTauJECUncertDownHist)    
    HadTauMTSysDn=binsToList(HadTauMTSysDownHist)    
    HadTauMTSysUp=binsToList(HadTauMTSysUpHist)    
    HadTauMTEff=binsToList(HadTauMTEffHist)
    HadTauAccStat=binsToList(HadTauAccStatHist)

    HadTauMuAccSysPDFUp=binsToList(HadTauMuAccSysPDFUpHist)
    HadTauMuAccSysPDFDn=binsToList(HadTauMuAccSysPDFDnHist)
    HadTauMuAccSysScaleUp=binsToList(HadTauMuAccSysScaleUpHist)
    HadTauMuAccSysScaleDn=binsToList(HadTauMuAccSysScaleDnHist)

    HadTauIsoTkEffHistStat =binsToList(HadTauIsoTkEffHistStatHist)
    HadTauIsoTkEffHistSys=binsToList(HadTauIsoTkEffHistSysHist)
    HadTauMuFromTauStat=binsToList(HadTauMuFromTauStatHist)
    HadTauMuDiLepton=binsToList(HadTauMuDiLeptonHist)
    HadTauMTEffDn=[]
    HadTauMuDiLeptonDn=[]
    HadTauAccStatDn=[]
    HadTauIsoTkEffSysDn=[]
    tauSqrtSumW2=binsToList(HadTauStatUncertainties)
    for i in range(len(tauSqrtSumW2)):
        if signalRegion_tauList[i]>0.0: tauSqrtSumW2[i]=tauSqrtSumW2[i]/signalRegion_tauList[i]
        HadTauMTEffDn.append(1.0/HadTauMTEff[i])
        HadTauMuDiLeptonDn.append(1.0/HadTauMuDiLepton[i])
        HadTauAccStatDn.append(1.0/HadTauAccStat[i])
        HadTauIsoTkEffSysDn.append(1.0/HadTauIsoTkEffHistSys[i])
    # --------------------------------------------
    # QCD, low delta phi

    ratesForSignalRegion_QCDList = [];
    NSRForSignalRegion_QCDList = textToList(idir+"/qcd-bg-combine-input.txt",6);
    ratesForLowdphiRegion_QCDList = [];
    NCRForLowdphiRegion_QCDList = textToList(idir+"/qcd-bg-combine-input.txt",2);
    obsForLowdphiRegion_QCDList = [];
    ratiosForLowdphiRegion = textToList(idir+"/qcd-bg-combine-input.txt",5);
    ContaminForLowdphiRegion = textToList(idir+"/qcd-bg-combine-input.txt",3);
    tagsForLowDPhiRegion = tagsForSignalRegion[:]
    QCDcontributionsPerBin = [];
    for i in range(len(tagsForLowDPhiRegion)): 
        QCDcontributionsPerBin.append( [ 'sig','qcd','contam' ] );
        if(NCRForLowdphiRegion_QCDList[i]>0.0):
            #BkgRateSubtracted=NCRForLowdphiRegion_QCDList[i]-ContaminForLowdphiRegion[i]
            BkgRateSubtracted=NCRForLowdphiRegion_QCDList[i]
            if BkgRateSubtracted>1:
                ratesForLowdphiRegion_QCDList.append(BkgRateSubtracted)
                ratesForSignalRegion_QCDList.append(NSRForSignalRegion_QCDList[i])            
            else:
                ratesForLowdphiRegion_QCDList.append(1.0)
                ratesForSignalRegion_QCDList.append(ratiosForLowdphiRegion[i]);
        else:
            ratesForLowdphiRegion_QCDList.append(1.0)
            ratesForSignalRegion_QCDList.append(ratiosForLowdphiRegion[i]);
        obsForLowdphiRegion_QCDList.append( NCRForLowdphiRegion_QCDList[i] );

    ######################################################################
    ######################################################################
    ## 2. Build the control regions and the signal regions
    ######################################################################
    ######################################################################

    # --------------------------------------------
    # QCD, low delta phi
    LowdphiControlRegion = searchRegion('Lowdphi', QCDcontributionsPerBin, tagsForLowDPhiRegion);    
    qcdcontrolRegion_Rates = [];
    qcdcontrollRegion_Observed = [];
    for i in range(LowdphiControlRegion._nBins):
        curobsC = 0;
        curobsC += obsForLowdphiRegion_QCDList[i]
        currateC = [];
        currateC.append( 0. );
        currateC.append( ratesForLowdphiRegion_QCDList[i] );
        currateC.append( ContaminForLowdphiRegion[i]);    
        #currateC.append(0.0)
        qcdcontrolRegion_Rates.append(currateC);
        qcdcontrollRegion_Observed.append(curobsC);    

    LowdphiControlRegion.fillRates(qcdcontrolRegion_Rates);
    LowdphiControlRegion.setObservedManually(qcdcontrollRegion_Observed);
    LowdphiControlRegion.writeRates();

    # --------------------------------------------
    # single photon control regions

    GJet_Obs    = binsToList( DYinputfile.Get("hgJNobs") )
    ZgRatio_List    = binsToList( DYinputfile.Get("hgJZgR") )
    GJetPur_List    = binsToList(DYinputfile.Get("hgJPur"))
    ZgRdataMC_List  = binsToList( DYinputfile.Get("hgJZgRdataMC") );


    ZgRatioErr_List      = binsToList( DYinputfile.Get("hgJZgRerr") )
    GJetPurErr_List      = binsToList(DYinputfile.Get("hgJPurErr"))
    ZgRdataMCErrUp_List  = binsToList( DYinputfile.Get("hgJZgRdataMCerrUp") );
    ZgRdataMCErrDn_List  = binsToList( DYinputfile.Get("hgJZgRdataMCerrLow") );

    sphotonObserved=[]
    RzgVals=[]
    PurVals=[]
    RzgErrsAbs=[]
    PurErrsAbs=[]

    ZgRdataMC = [];
    ZgRdataMCErrUp = [];
    ZgRdataMCErrDn = [];

    for i in range(len(GJet_Obs)):
        if(GJet_Obs[i]>-1):sphotonObserved.append(GJet_Obs[i])
        if(ZgRatio_List[i]>-1):RzgVals.append(ZgRatio_List[i])
        if(GJetPur_List[i]>-1):PurVals.append(GJetPur_List[i])
        if(GJetPurErr_List[i]>-1):PurErrsAbs.append(GJetPurErr_List[i])
        if(ZgRatioErr_List[i]>-1):RzgErrsAbs.append(ZgRatioErr_List[i])    
        if (ZgRdataMC_List[i] > -1): ZgRdataMC.append( ZgRdataMC_List[i] )
        if (ZgRdataMCErrUp_List[i] > -1): ZgRdataMCErrUp.append( 1.+ZgRdataMCErrUp_List[i] )
        if (ZgRdataMCErrDn_List[i] > -1): ZgRdataMCErrDn.append( 1.-ZgRdataMCErrDn_List[i] )
    
    RzgErrs = [];
    PurErrs = [];
    for i in range(len(RzgVals)): RzgErrs.append( 1+RzgErrsAbs[i] );
    for i in range(len(PurVals)): PurErrs.append( 1+PurErrsAbs[i]);

    PhoRatios = [];
    for i in range(len(RzgVals)): PhoRatios.append( 1./RzgVals[i]/PurVals[i]/ZgRdataMC[i] );

    phoRegion_sigHist = sphotonRegion_file.Get("RA2bin_SMSbbbb1000") # this is just for the right bin labels for the 18 bins
    tagsForSinglePhoton = binLabelsToList(phoRegion_sigHist)
    contributionsPerBin = [];
    for i in range(len(tagsForSinglePhoton)): contributionsPerBin.append(['sig','zvv']);
    sphotonRegion = searchRegion('sphoton', contributionsPerBin, tagsForSinglePhoton);          
    phoRegion_sigList = binsToList(phoRegion_sigHist);
    phoRegion_Rates = [];
    for i in range(sphotonRegion._nBins):
            tmpList = [];
            #tmpList.append(phoRegion_sigList[i]);
            tmpList.append(0.000001);
            if sphotonObserved[i] > 0: tmpList.append(sphotonObserved[i]);
            else: tmpList.append(PhoRatios[i]);
            phoRegion_Rates.append( tmpList );
    sphotonRegion.fillRates( phoRegion_Rates );
    sphotonRegion.setObservedManually(sphotonObserved);
       #compute the Zvv actual yields to be put in the observed lines
    sphotonObservedExt = [];
    RzgValsExt = [];
    PurValsExt = [];
    ZgRdataMCExt = [];

    for i in range(4):
            sphotonObservedExt.extend(sphotonObserved[0:6]); RzgValsExt.extend(RzgVals[0:6]); PurValsExt.extend(PurVals[0:6]); ZgRdataMCExt.extend(ZgRdataMC[0:6]);
    for i in range(4):
            sphotonObservedExt.extend(sphotonObserved[6:12]); RzgValsExt.extend(RzgVals[6:12]); PurValsExt.extend(PurVals[6:12]); ZgRdataMCExt.extend(ZgRdataMC[6:12]);
    for i in range(4):
            sphotonObservedExt.extend(sphotonObserved[12:18]); RzgValsExt.extend(RzgVals[12:18]); PurValsExt.extend(PurVals[12:18]); ZgRdataMCExt.extend(ZgRdataMC[12:18]);

    ZvvYieldsInSignalRegion = [sphotonObservedExt[i]*RzgValsExt[i]*PurValsExt[i]*signalRegion_zvvList[i]*ZgRdataMCExt[i] for i in range(len(sphotonObservedExt))]
    ZvvRatesInSignalRegion = [];

    for i in range(len(sphotonObservedExt)):
            if sphotonObservedExt[i] > 0: ZvvRatesInSignalRegion.append( ZvvYieldsInSignalRegion[i] );
            else: ZvvRatesInSignalRegion.append(signalRegion_zvvList[i]);

    # --------------------------------------------
    # lost lepton and had tau control regions

    tagsForSLControlRegion=[]    
    tagsForHadControlRegion=[]
    SLcontrolContributionsPerBin = [];
    addControl=[]
    for i in range(len(tagsForSignalRegion)): 
        #if(signalRegion_CSList[i]<2):
        tmpcontributionsSL = [];
        tmpcontributionsSL.append( 'sig' );
        if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly): tmpcontributionsSL.append( 'WTopSL' );
        if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly): tmpcontributionsSL.append( 'WTopSLHighW' );
        if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpcontributionsSL.append( 'WTopHad' );
        if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpcontributionsSL.append( 'WTopHadHighW' );            
        if options.llpOnly and not (options.tauOnly and  options.llpOnly):
            addControl.append(i);
            SLcontrolContributionsPerBin.append( tmpcontributionsSL );
            tagsForSLControlRegion.append(tagsForSignalRegion[i]);
        if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly):
            addControl.append(i); 
            SLcontrolContributionsPerBin.append( tmpcontributionsSL );
            tagsForSLControlRegion.append(tagsForSignalRegion[i]);            
    SLcontrolRegion = searchRegion('SLControl', SLcontrolContributionsPerBin, tagsForSLControlRegion)
    SLcontrolRegion_Obs = [];
    SLcontrolRegion_Rates = [];
    HadcontrolRegion_Obs = [];
    HadcontrolRegion_Rates = [];
    for i in range(len(addControl)):
        tmpList=[]
        tmpList.append(0);
        if options.llpOnly and not options.tauOnly and not options.allBkgs: 
                tmpList.append(0.);            
                #if(signalRegion_CSList[i]<=1): 
                tmpList.append(1.0); 
                #else: tmpList.append(0.0); 
        if options.allBkgs or (options.tauOnly and options.llpOnly):
                tmpList.append(0.);
                tmpList.append(0.0);
        if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpList.append(0.0);
        if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpList.append(1.);
        SLcontrolRegion_Obs.append(0.0);
        SLcontrolRegion_Rates.append(tmpList);
    #print len(SLcontrolRegion_Rates), len(SLcontrolRegion_Obs)
    SLcontrolRegion.fillRates(SLcontrolRegion_Rates);
    SLcontrolRegion.setObservedManually(SLcontrolRegion_Obs);

    # --------------------------------------------
    # signal regions

    contributionsPerBin = [];
    for i in range(len(tagsForSignalRegion)): 
        tmpcontributions = [];
        tmpcontributions.append('sig');
        if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly): tmpcontributions.append('WTopSL');
        if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly): tmpcontributions.append('WTopSLHighW');
        if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpcontributions.append('WTopHad');
        if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): tmpcontributions.append('WTopHadHighW');
        if options.allBkgs or options.zvvOnly: tmpcontributions.append('zvv');
        if options.allBkgs or options.qcdOnly: tmpcontributions.append('qcd');
        contributionsPerBin.append(tmpcontributions);

    signalRegion = searchRegion('signal', contributionsPerBin, tagsForSignalRegion)

    signalRegion_Rates = [];
    signalRegion_Obs = [];
    controlRegion_Rates=[];
    f = TFile(odir+'yields.root', 'recreate')
    data = TH1F( 'data', 'data', 72, 0, 72 )
    qcd = TH1F( 'QCD', 'QCD', 72, 0, 72 )
    zvv = TH1F( 'Zvv', 'Zvv', 72, 0, 72 )
    ll = TH1F( 'LL', 'LL', 72, 0, 72 )
    tau = TH1F( 'tau', 'tau', 72, 0, 72 )
    DataHist_In=TFile("inputHistograms/histograms_%1.1ffb/RA2bin_signalUnblind.root" %lumi)
    Data_Hist=DataHist_In.Get("RA2bin_data")
    Data_List=binsToList(Data_Hist)
    for i in range(signalRegion._nBins):
        srobs = 0;
        srobs += signalRegion_sigList[i]*signalmu;
        if options.allBkgs or options.qcdOnly: srobs += NSRForSignalRegion_QCDList[i];
        if options.allBkgs or options.zvvOnly: srobs += ZvvYieldsInSignalRegion[i];
        if options.allBkgs or options.llpOnly: srobs += signalRegion_LLList[i];
        if options.allBkgs or options.tauOnly: srobs += signalRegion_tauList[i];
        if options.realData: srobs = Data_List[i];
        signalRegion_Obs.append( srobs );

        data.Fill(i+.5, Data_List[i])
        qcd.Fill(i+.5, NSRForSignalRegion_QCDList[i])
        zvv.Fill(i+.5, ZvvYieldsInSignalRegion[i])
        ll.Fill(i+.5, signalRegion_LLList[i])
        tau.Fill(i+.5, signalRegion_tauList[i])    


        print "bin {0:2}: {1:6.2f} {2:6.2f} ||| {3:6.2f} {4:6.2f} {5:6.2f} {6:6.2f}".format(i,signalRegion_sigList[i]*signalmu,srobs-signalRegion_sigList[i]*signalmu,NSRForSignalRegion_QCDList[i],ZvvYieldsInSignalRegion[i],signalRegion_LLList[i],signalRegion_tauList[i]),
        print " ---", tagsForSignalRegion[i]

        tmpList = [];
        if options.fastsim and ('T1t' in model or 'T5qqqqVV' in model) :
            signalContamLL_file=TFile("inputHistograms/SignalContamin/LLContamination_%s.root" %model)
            signalContamTau_file=TFile("inputHistograms/SignalContamin/Signal%sHtauContamin.root" %model)
            TauContamHist =signalContamTau_file.Get("SearchH_b/"+signaltag)
            TauContamHist.Scale(lumi/3.0)
            LLContamHist=signalContamLL_file.Get("SignalContamination/mGluino_%s_mLSP_%s" %(options.mGo, options.mLSP))
        #    LLContamHist.Scale(lumi/3.0)    
            LLContamList=binsToList(LLContamHist)
            HadtauContamList=binsToList(TauContamHist)  
            tmpList.append(signalRegion_sigList[i]-LLContamList[i]-HadtauContamList[i]);
        else:
            tmpList.append(signalRegion_sigList[i])
        # LL rate
        
        if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly):        
            # addControl=[]    
            #if(signalRegion_CSList[i]>=2):
            tmpList.append(signalRegion_LLList[i]);
            #else:
            #tmpList.append(0.0)
            #if(signalRegion_CSList[i]>=2):
            #    tmpList.append(0.0)
            #if(signalRegion_CSList[i]==1):
            #print signalRegion_MCWeightList
            tmpList.append(signalRegion_MCWeightList[i]*1.0)
            #if(signalRegion_CSList[i]<1):
                #tmpList.append(signalRegion_MCWeightList[i]*1.0)
        # Had Tau rate
        if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly): 
                tmpList.append(signalRegion_tauList[i])
                tmpList.append(0.25);
        if options.allBkgs or options.zvvOnly: tmpList.append( ZvvRatesInSignalRegion[i]) ;
        if options.allBkgs or options.qcdOnly: tmpList.append( ratesForSignalRegion_QCDList[i] );
        signalRegion_Rates.append( tmpList );
    
    signalRegion.fillRates( signalRegion_Rates );
    signalRegion.setObservedManually(signalRegion_Obs)

    SLcontrolRegion.writeRates();
    sphotonRegion.writeRates();
    signalRegion.writeRates();
    f.Write()
    f.Close()
    ######################################################################
    ######################################################################
    # 3. Add all the systematics!
    ######################################################################
    ######################################################################


    # ['SMSqqqq1000','SMSqqqq1400','SMStttt1200','SMStttt1500','SMSbbbb1000','SMSbbbb1500']
    pdf=1.1
    ISR=1.01
    if(sms=='SMSqqqq1400' or sms=='SMStttt1200' or sms=='SMSbbbb1000'):
        ISR=1.08
        pdf=1.20
    if ('T1t' in model or 'T5qqqqVV' in model or 'T2tt' in model) :
        signalRegion.addSingleSystematic('IsoTrackSigEff','lnN',['sig'],1.02);
    signalRegion.addSingleSystematic('lumi','lnN',['sig'],1.046);
    #signalRegion.addSingleSystematic('EvtFilters','lnN',['sig'],1.03);
    if options.fastsim: signalRegion.addSingleSystematic('JetIDUnc','lnN',['sig'],1.01);
    #signalRegion.addSingleSystematic('ISR','lnN',['sig'],ISR);
#    signalRegion.addSingleSystematic('JERUnc', 'lnN', ['sig'], 1.02);

    #signalRegion.addSingleSystematic('PDFUnc','lnN',['sig'],pdf);

    for i in range(signalRegion.GetNbins()):
        if( signalRegion_sigList[i]>0.000001): 
            
            signalRegion.addAsymSystematic('CTagSFunc', 'lnN', ['sig'], signalRegion_sigListCharmSFUp[i]/signalRegion_sigList[i], signalRegion_sigListCharmSFDown[i]/signalRegion_sigList[i], '', i)
            signalRegion.addAsymSystematic('MisTagSFunc', 'lnN', ['sig'], signalRegion_sigListMisSFUp[i]/signalRegion_sigList[i], signalRegion_sigListMisSFDown[i]/signalRegion_sigList[i], '', i)
            signalRegion.addAsymSystematic('BTagSFUnc','lnN', ['sig'], (signalRegion_sigListSFUp[i]/signalRegion_sigList[i]),signalRegion_sigListSFDown[i]/signalRegion_sigList[i],'', i)

            signalRegion.addAsymSystematic('TrigSystunc','lnN', ['sig'], signalRegion_sigListTrigSystUp[i]/signalRegion_sigList[i], signalRegion_sigListTrigSystDown[i]/signalRegion_sigList[i], '', i)
            signalRegion.addAsymSystematic('TrigStatUnc','lnN', ['sig'], (signalRegion_sigListTrigStatUp[i]/signalRegion_sigList[i]),signalRegion_sigListTrigStatDown[i]/signalRegion_sigList[i],'', i)
            if signalRegion_sigListJECUp[i]>0.0 and signalRegion_sigListJECDown[i]>0.0:
                if signalRegion_sigListJECUp[i]/signalRegion_sigList[i]>2.0:
                    signalRegion.addAsymSystematic('JECUnc','lnN', ['sig'], 2.0,0.5,'', i)
                else:
                    signalRegion.addAsymSystematic('JECUnc','lnN', ['sig'], (signalRegion_sigListJECUp[i]/signalRegion_sigList[i]),signalRegion_sigListJECDown[i]/signalRegion_sigList[i],'', i)
            if signalRegion_sigListJECUp[i]>0.0 and signalRegion_sigListJECDown[i]<0.00001:
                if signalRegion_sigListJECUp[i]/signalRegion_sigList[i]>2.0:
                    signalRegion.addAsymSystematic('JECUnc','lnN', ['sig'], 2.0,0.5,'', i)
                else:
                    signalRegion.addAsymSystematic('JECUnc','lnN', ['sig'], (signalRegion_sigListJECUp[i]/signalRegion_sigList[i]),signalRegion_sigList[i]/signalRegion_sigListJECUp[i],'', i)
            if signalRegion_sigListJECUp[i]<0.0001 and signalRegion_sigListJECDown[i]>0.0:
                if signalRegion_sigList[i]/signalRegion_sigListJECDown[i]>2.0:
                    signalRegion.addAsymSystematic('JECUnc','lnN', ['sig'], 2.0,0.5,'', i)
                else:
                    signalRegion.addAsymSystematic('JECUnc','lnN', ['sig'], (signalRegion_sigList[i]/signalRegion_sigListJECDown[i]),signalRegion_sigListJECDown[i]/signalRegion_sigList[i],'', i)
            signalRegion.addAsymSystematic('PileupUnc','lnN', ['sig'], (signalRegion_sigListPUUp[i]/signalRegion_sigList[i]),signalRegion_sigListPUDown[i]/signalRegion_sigList[i],'', i)
            signalRegion.addAsymSystematic('ISRSystem','lnN', ['sig'],signalRegion_sigListISRUp[i]/signalRegion_sigList[i], signalRegion_sigListISRDown[i]/signalRegion_sigList[i], '',i)
            # if signalRegion_sigListPDFDown[i] > 0.00001:
            #      signalRegion.addAsymSystematic('PDFUnc','lnN', ['sig'], (signalRegion_sigListPDFUp[i]/signalRegion_sigList[i]),signalRegion_sigListPDFDown[i]/signalRegion_sigList[i],'', i)
            # else:
            #      signalRegion.addAsymSystematic('PDFUnc','lnN', ['sig'], (signalRegion_sigListPDFUp[i]/signalRegion_sigList[i]),signalRegion_sigList[i]/signalRegion_sigListPDFUp[i],'', i)
              if signalRegion_sigListScaleDown[i] > 0.00001:
                 signalRegion.addAsymSystematic('ScaleUnc','lnN', ['sig'], (signalRegion_sigListScaleUp[i]/signalRegion_sigList[i]),signalRegion_sigListScaleDown[i]/signalRegion_sigList[i],'', i)
            else: 
                 signalRegion.addAsymSystematic('ScaleUnc','lnN', ['sig'], (signalRegion_sigListScaleUp[i]/signalRegion_sigList[i]),signalRegion_sigList[i]/signalRegion_sigListScaleUp[i],'', i)    
               
            if options.fastsim:
                signalRegion.addAsymSystematic('btagCFunc', 'lnN', ['sig'], signalRegion_sigListbtagCFuncUp[i]/signalRegion_sigList[i], signalRegion_sigListbtagCFuncDown[i]/signalRegion_sigList[i], '', i)
                signalRegion.addAsymSystematic('ctagCFUnc','lnN', ['sig'], (signalRegion_sigListctagCFuncUp[i]/signalRegion_sigList[i]),signalRegion_sigListctagCFuncDown[i]/signalRegion_sigList[i],'', i)
                signalRegion.addAsymSystematic('mistagCFUnc','lnN', ['sig'], (signalRegion_sigListmistagCFuncUp[i]/signalRegion_sigList[i]),signalRegion_sigListmistagCFuncDown[i]/signalRegion_sigList[i],'', i)

            signalRegion_sigListMCstatErr[i] = signalRegion_sigListMCstatErr[i]/signalRegion_sigList[i] + 1.;
            signalRegion.addSingleSystematic('SignalMCStatErr','lnN', ['sig'], signalRegion_sigListMCstatErr, '', i)


    # signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 1.0, 'MHT0_HT0');
    # signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 0.95, 'MHT0_HT1');
    # signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 1.1, 'MHT0_HT2');
    # signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 0.95, 'MHT1_HT3');
    # signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 0.95, 'MHT1_HT4');
    # signalRegion.addSingleSystematic('JESUnc', 'lnN', ['sig'], 1.1, 'MHT2_HT5');

    ### Zvv uncertainties ------------------------------------------------------------------------------
    if options.allBkgs or options.zvvOnly:

        # connect the single photon CR to the signal region
        singlePhotonBins = ["NJets0_BTags._MHT0_HT0","NJets0_BTags._MHT0_HT1","NJets0_BTags._MHT0_HT2","NJets0_BTags._MHT1_HT3","NJets0_BTags._MHT1_HT4","NJets0_BTags._MHT2_HT5",
                            "NJets1_BTags._MHT0_HT0","NJets1_BTags._MHT0_HT1","NJets1_BTags._MHT0_HT2","NJets1_BTags._MHT1_HT3","NJets1_BTags._MHT1_HT4","NJets1_BTags._MHT2_HT5",
                            "NJets2_BTags._MHT0_HT0","NJets2_BTags._MHT0_HT1","NJets2_BTags._MHT0_HT2","NJets2_BTags._MHT1_HT3","NJets2_BTags._MHT1_HT4","NJets2_BTags._MHT2_HT5"];

        ZgRatioErrUp_List    = binsToList( DYinputfile.Get("hgJZgRerrUp") )
        ZgRatioErrDown_List  = binsToList( DYinputfile.Get("hgJZgRerrLow") )
        DYStatErr_List       = binsToList( DYinputfile.Get("hDYstat") )
        DYMCStatErr_List     = binsToList( DYinputfile.Get("hDYMCstat") );
        DYPurErr_List    = binsToList( DYinputfile.Get("hDYsysPur") )
        DYsysKin_List    = binsToList( DYinputfile.Get("hDYsysKin") )

        #PhoCSZgRatio=[]
        PhoCSZgRatioUp=[]    
        PhoCSZgRatioDown=[]
        for i in range(signalRegion.GetNbins()):
            #if(ZgRatio_List[i]>-1):PhoCSZgRatio.append(ZgRatioErr_List[i])
            if(ZgRatioErrUp_List[i]>-1):PhoCSZgRatioUp.append(ZgRatioErrUp_List[i])
            if(ZgRatioErrDown_List[i]>-1):PhoCSZgRatioDown.append(ZgRatioErrDown_List[i])
            DYStatErr_List[i]=1+DYStatErr_List[i]
            DYMCStatErr_List[i]=1+DYMCStatErr_List[i]
            DYPurErr_List[i]=1+DYPurErr_List[i]
            DYsysKin_List[i]=1+DYsysKin_List[i]
            signalRegion.addSingleSystematic('DYsysKin'+str(i),'lnN',['zvv'], DYsysKin_List,'', i);
            #DYPurErr_List[i]=1+DYPurErr_List[i]
        signalRegion.addSingleSystematic("DYstat"+"_BTag1", 'lnN', ['zvv'], DYStatErr_List, 'BTags1')
        signalRegion.addSingleSystematic("DYstat"+"_BTag2", 'lnN', ['zvv'], DYStatErr_List, 'BTags2')            
        signalRegion.addSingleSystematic("DYstat"+"_BTag3", 'lnN', ['zvv'], DYStatErr_List, 'BTags3')

        signalRegion.addSingleSystematic("DYMCstat_Nj1_Btag1", 'lnN', ['zvv'], DYMCStatErr_List, 'NJets1_BTags1')
        signalRegion.addSingleSystematic("DYMCstat_Nj1_Btag2", 'lnN', ['zvv'], DYMCStatErr_List, 'NJets1_BTags2')
        signalRegion.addSingleSystematic("DYMCstat_Nj1_Btag3", 'lnN', ['zvv'], DYMCStatErr_List, 'NJets1_BTags3')
        signalRegion.addSingleSystematic("DYMCstat_Nj2_Btag1", 'lnN', ['zvv'], DYMCStatErr_List, 'NJets2_BTags1')
        signalRegion.addSingleSystematic("DYMCstat_Nj2_Btag2", 'lnN', ['zvv'], DYMCStatErr_List, 'NJets2_BTags2')
        signalRegion.addSingleSystematic("DYMCstat_Nj2_Btag3", 'lnN', ['zvv'], DYMCStatErr_List, 'NJets2_BTags3')

        signalRegion.addSingleSystematic("DYPur"+"_BTag1", 'lnN', ['zvv'], DYPurErr_List, "BTags1")
        signalRegion.addSingleSystematic("DYPur"+"_BTag1Plus", 'lnN', ['zvv'], DYPurErr_List, "BTags2")
        signalRegion.addSingleSystematic("DYPur"+"_BTag1Plus", 'lnN', ['zvv'], DYPurErr_List, "BTags3")
        
        for i in range(len(singlePhotonBins)):
            signalRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],10000,singlePhotonBins[i]);
            sphotonRegion.addSingleSystematic('SPhoCR'+str(i),'lnU',['zvv'],10000,singlePhotonBins[i]);
            
            # WTF,are these double counting
            # sphotonRegion.addAsymSystematic('PhoRzgAndDblRatioAsymUnc'+str(i), 'lnN', ['zvv'], 1.0+PhoCSZgRatioUp[i],1.0-PhoCSZgRatioDown[i],'',i)
            sphotonRegion.addAsymSystematic('PhoRzgAndDblRatioAsymUnc'+str(i), 'lnN', ['zvv'], 1.0+PhoCSZgRatioUp[i],1.0-PhoCSZgRatioDown[i],'',i)
            sphotonRegion.addSingleSystematic('ZgRatioErr'+str(i),'lnN',['zvv'],RzgErrs[i],'',i);    # different per bin
            # sphotonRegion.addSingleSystematic('PhoPurUnc','lnN',['zvv'],PurErrs[i],'',i);     # this is getting split up now
            # sphotonRegion.addAsymSystematic('PhoRZgDblRatio'+str(i),'lnN',['zvv'],ZgRdataMCErrUp,ZgRdataMCErrDn, '',i); #### this is now merged with ZGratio uncertainty

        sphotonRegion.addSingleSystematic('PhoPurUncMHT0','lnN',['zvv'],PurErrs[i],'MHT0');    
        sphotonRegion.addSingleSystematic('PhoPurUncMHT1','lnN',['zvv'],PurErrs[i],'MHT1');    
        sphotonRegion.addSingleSystematic('PhoPurUncMHT2','lnN',['zvv'],PurErrs[i],'MHT2');    

        signalRegion.addAsymSystematicFromList('DYsysNj','lnN',['zvv'], binsToList(DYinputfile.Get("hDYsysNjUp")), binsToList(DYinputfile.Get("hDYsysNjLow")));

    ### LL uncertainties ------------------------------------------------------------------------------
    if options.allBkgs or options.llpOnly or (options.tauOnly and  options.llpOnly):
        for i in range(signalRegion.GetNbins()):
            if(signalRegion_CSList[i]>0):
                signalRegion.addAsymSystematic("LLSysNonClosSys"+tagsForSignalRegion[i],'lnN',['WTopSL'],(LLSysNCUp[i]), (LLSysNCDown[i]),'', i)                
            signalRegion.addAsymSystematic("LLStatMuReco",'lnN',['WTopSL'],(LLStatMuRecoUp[i]), (LLStatMuRecoDown[i]),'', i)
            signalRegion.addAsymSystematic("LLStatEleIso",'lnN',['WTopSL'],(LLStatElecIsoUp[i]), (LLStatElecIsoDown[i]),'', i)
            signalRegion.addAsymSystematic("LLStatEleReco",'lnN',['WTopSL'],(LLStatElecRecoUp[i]), (LLStatElecRecoDown[i]),'', i)

            if options.llpOnly: signalRegion.addAsymSystematic("LLSysMuIso",'lnN',['WTopSL'],(LLSysMuIsoUp[i]), (LLSysMuIsoDown[i]),'', i)
            else: signalRegion.addCorrelSystematicAsym("LLSysMuIso",'lnN',['WTopSL','WTopHad'],LLSysMuIsoUp[i], LLSysMuIsoDown[i],HadTauMuonIsoUncUp[i], HadTauMuonIsoUncDn[i],'', i)
             if options.llpOnly: signalRegion.addAsymSystematic("LLSysMuReco",'lnN',['WTopSL'],(LLSysMuRecoUp[i]), (LLSysMuRecoDown[i]),'', i)
            else: 
                signalRegion.addCorrelSystematicAsym("LLSysMuIso",'lnN',['WTopSL','WTopHad'],LLSysMuRecoUp[i], LLSysMuRecoDown[i],HadTauMuonCorrUncUp[i], HadTauMuonCorrUncDn[i],'', i)
                signalRegion.addCorrelSystematicAsym("LLStatMuIso",'lnN',['WTopSL','WTopHad'],(LLStatMuIsoUp[i]), (LLStatMuIsoDown[i]),HadTauMuonIsoRecoStatUncUp[i], HadTauMuonIsoRecoStatUncDn[i],'', i)

            signalRegion.addAsymSystematic("LLSysEleIso",'lnN',['WTopSL'],(LLSysElecIsoUp[i]), (LLSysElecIsoDown[i]),'', i)
            signalRegion.addAsymSystematic("LLSysEleReco",'lnN',['WTopSL'],(LLSysElecRecoUp[i]), (LLSysElecRecoDown[i]),'', i)    

        if options.llpOnly:
            signalRegion.addAsymSystematic("LLSysMTW_NJet0",'lnN',['WTopSL'],LLSysMTUp, LLSysMTDown,'NJets0')
            signalRegion.addAsymSystematic("LLSysMTW_NJet1",'lnN',['WTopSL'],LLSysMTUp, LLSysMTDown,'NJets1')
            signalRegion.addAsymSystematic("LLSysMTW_NJet2",'lnN',['WTopSL'],LLSysMTUp, LLSysMTDown,'NJets2')
            signalRegion.addAsymSystematic("LLStatMTW_NJet0",'lnN',['WTopSL'],LLStatMTUp, LLStatMTDown,'NJets0')
            signalRegion.addAsymSystematic("LLStatMTW_NJet1",'lnN',['WTopSL'],LLStatMTUp, LLStatMTDown,'NJets1')
            signalRegion.addAsymSystematic("LLStatMTW_NJet2",'lnN',['WTopSL'],LLStatMTUp, LLStatMTDown,'NJets2')
            signalRegion.addAsymSystematic("LLSysDiLepPurity_NJet0",'lnN',['WTopSL'],LLSysDiLepPurUp, LLSysDiLepPurDown,'NJets0')
            signalRegion.addAsymSystematic("LLSysDiLepPurity_NJet1",'lnN',['WTopSL'],LLSysDiLepPurUp, LLSysDiLepPurDown,'NJets1')
            signalRegion.addAsymSystematic("LLSysDiLepPurity_NJet2",'lnN',['WTopSL'],LLSysDiLepPurUp, LLSysDiLepPurDown,'NJets2')
            #if(signalRegion_CSList[i]==1):
                #signalRegion.addSingleSystematic('LLSysavgWUnc'+tagsForSignalRegion[i],'lnN',['WTopSLHighW'], 2.0,'',i); 
            
        else:
            signalRegion.addCorrelSystematicAsym("LLSysMTW_NJet0",'lnN',['WTopSL','WTopHad'],LLSysMTUp, LLSysMTDown,HadTauMTSysUp,HadTauMTSysDn,'NJets0')
            signalRegion.addCorrelSystematicAsym("LLSysMTW_NJet1",'lnN',['WTopSL','WTopHad'],LLSysMTUp, LLSysMTDown,HadTauMTSysUp,HadTauMTSysDn,'NJets1')
            signalRegion.addCorrelSystematicAsym("LLSysMTW_NJet2",'lnN',['WTopSL','WTopHad'],LLSysMTUp, LLSysMTDown,HadTauMTSysUp,HadTauMTSysDn,'NJets2')
            signalRegion.addCorrelSystematicAsym("LLStatMTW_NJet0",'lnN',['WTopSL','WTopHad'],LLStatMTUp, LLStatMTDown,HadTauMTEff,HadTauMTEffDn,'NJets0')
            signalRegion.addCorrelSystematicAsym("LLStatMTW_NJet1",'lnN',['WTopSL','WTopHad'],LLStatMTUp, LLStatMTDown,HadTauMTEff,HadTauMTEffDn,'NJets1')
            signalRegion.addCorrelSystematicAsym("LLStatMTW_NJet2",'lnN',['WTopSL','WTopHad'],LLStatMTUp, LLStatMTDown,HadTauMTEff,HadTauMTEffDn,'NJets2')
            signalRegion.addCorrelSystematicAsym("LLSysDiLepPurity_NJet0",'lnN',['WTopSL','WTopHad'],LLSysDiLepPurUp, LLSysDiLepPurDown,HadTauMuDiLepton,HadTauMuDiLeptonDn,'NJets0')
            signalRegion.addCorrelSystematicAsym("LLSysDiLepPurity_NJet1",'lnN',['WTopSL','WTopHad'],LLSysDiLepPurUp, LLSysDiLepPurDown,HadTauMuDiLepton,HadTauMuDiLeptonDn,'NJets1')
            signalRegion.addCorrelSystematicAsym("LLSysDiLepPurity_NJet2",'lnN',['WTopSL','WTopHad'],LLSysDiLepPurUp, LLSysDiLepPurDown,HadTauMuDiLepton,HadTauMuDiLeptonDn,'NJets2')

        
        signalRegion.addAsymSystematic("LLStatDiLepPurity_NJet0",'lnN',['WTopSL'],LLStatDiLepPurUp, LLStatDiLepPurDown,'NJets0')
        signalRegion.addAsymSystematic("LLStatDiLepPurity_NJet1",'lnN',['WTopSL'],LLStatDiLepPurUp, LLStatDiLepPurDown,'NJets1')
        signalRegion.addAsymSystematic("LLStatDiLepPurity_NJet2",'lnN',['WTopSL'],LLStatDiLepPurUp, LLStatDiLepPurDown,'NJets2')    


        signalRegion.addAsymSystematic("LLSysSingleLepPurity_NJet0",'lnN',['WTopSL'],LLSysPurUp, LLSysPurDown,'NJets0')
        signalRegion.addAsymSystematic("LLSysSingleLepPurity_NJet1",'lnN',['WTopSL'],LLSysPurUp, LLSysPurDown,'NJets1')
        signalRegion.addAsymSystematic("LLSysSingleLepPurity_NJet2",'lnN',['WTopSL'],LLSysPurUp, LLSysPurDown,'NJets2')    
        signalRegion.addAsymSystematic("LLStatSingleLepPurity_NJet0",'lnN',['WTopSL'],LLStatPurUp, LLStatPurDown,'NJets0')
        signalRegion.addAsymSystematic("LLStatSingleLepPurity_NJet1",'lnN',['WTopSL'],LLStatPurUp, LLStatPurDown,'NJets1')
        signalRegion.addAsymSystematic("LLStatSingleLepPurity_NJet2",'lnN',['WTopSL'],LLStatPurUp, LLStatPurDown,'NJets2')

        NJbinsLL=['NJets1', 'NJets2']
        MHTHTBinsLL=['MHT0_HT0','MHT0_HT1','MHT0_HT2', 'MHT1_HT3','MHT1_HT4','MHT2_HT5']
        for h in range(len(MHTHTBinsLL)):
            signalRegion.addAsymSystematic("LLSysIsoTrackNJets0_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysIsoTrackUp), (LLSysIsoTrackDown),'NJets0_BTags._'+str(MHTHTBinsLL[h]))
            
            signalRegion.addAsymSystematic("MuAccSysNJets0_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysMuAccUp), (LLSysMuAccDown),'NJets0_BTags._'+str(MHTHTBinsLL[h]))
            signalRegion.addAsymSystematic("ElecAccSysNJets0_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysElecAccUp), (LLSysElecAccDown),'NJets0_BTags._'+str(MHTHTBinsLL[h]))
                
            if options.llpOnly:signalRegion.addAsymSystematic("LLStatIsoTrackNJets0_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLStatIsoTrackUp), (LLStatIsoTrackDown),'NJets0_BTags._'+str(MHTHTBinsLL[h]))
            else: signalRegion.addCorrelSystematicAsym("LLStatIsoTrackNJets0_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL','WTopHad'],(LLStatIsoTrackUp), (LLStatIsoTrackDown),HadTauIsoTkEffHistSys, HadTauIsoTkEffSysDn,'NJets0_BTags._'+str(MHTHTBinsLL[h]))

            signalRegion.addAsymSystematic("MuAccStatNJets0_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLStatMuAccUp), (LLStatMuAccDown),'NJets0_BTags._'+str(MHTHTBinsLL[h]))
            signalRegion.addAsymSystematic("ElecAccStatNJets0_"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLStatElecAccUp), (LLStatElecAccDown),'NJets0_BTags._'+str(MHTHTBinsLL[h]))    
        for j in range(len(NJbinsLL)): #print NJbinsLL[j]
            for h in range(len(MHTHTBinsLL)):    
                if options.llpOnly: signalRegion.addAsymSystematic("LLSysIsoTrack7Jets"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysIsoTrackUp), (LLSysIsoTrackDown),str(NJbinsLL[j])+"_BTags._"+str(MHTHTBinsLL[h]))
                else: signalRegion.addCorrelSystematicAsym("LLSysIsoTrack7Jets"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysIsoTrackUp), (LLSysIsoTrackDown), HadTauIsoTkEffHistSys, HadTauIsoTkEffSysDn, str(NJbinsLL[j])+"_BTags._"+str(MHTHTBinsLL[h]))
                signalRegion.addAsymSystematic("LLStatIsoTrack7Jets"+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLStatIsoTrackUp), (LLStatIsoTrackDown),str(NJbinsLL[j])+"_BTags._"+str(MHTHTBinsLL[h]))
        NJbinsLLPur=['NJets0', 'NJets1', 'NJets2']

        MHTBins=['MHT0', 'MHT1', 'MHT2']
        for j in range(len(NJbinsLLPur)):
            for m in range(len(MHTBins)):
               signalRegion.addAsymSystematic("LLPuritySys_"+str(MHTBins[m])+"_"+str(NJbinsLLPur[j]),'lnN',['WTopSL'],LLSysPurUp,LLSysPurDown,str(NJbinsLLPur[j])+"_BTags._"+str(MHTBins[m])+"_HT.")
               signalRegion.addAsymSystematic("LLPurityStat_"+str(MHTBins[m])+"_"+str(NJbinsLLPur[j]),'lnN',['WTopSL'],LLStatPurUp,LLStatPurDown,str(NJbinsLLPur[j])+"_BTags._"+str(MHTBins[m])+"_HT.")
            for mh in range(len(MHTHTBinsLL)):
               if options.llpOnly:signalRegion.addAsymSystematic("MuAccSys"+str(NJbinsLLPur[j])+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysMuAccUp), (LLSysMuAccDown),str(NJbinsLLPur[j])+'_BTags._'+str(MHTHTBinsLL[h]))
               else: signalRegion.addCorrelSystematicAsym("MuAccSys"+str(NJbinsLLPur[j])+str(MHTHTBinsLL[h]),'lnN', ['WTopSL','WtopHad'], (LLSysMuAccUp), (LLSysMuAccDown),HadTauMuAccSysPDFUp, HadTauMuAccSysPDFDn, str(NJbinsLLPur[j])+'_BTags._'+str(MHTHTBinsLL[h]))

               signalRegion.addAsymSystematic("ElecAccSys"+str(NJbinsLLPur[j])+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysElecAccUp), (LLSysElecAccDown),str(NJbinsLLPur[j])+'_BTags._'+str(MHTHTBinsLL[h]))
               if options.llpOnly: signalRegion.addAsymSystematic("MuAccStat"+str(NJbinsLLPur[j])+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLStatMuAccUp), (LLStatMuAccDown),str(NJbinsLLPur[j])+'_BTags._'+str(MHTHTBinsLL[h]))
               else: signalRegion.addCorrelSystematicAsym("MuAccStat"+str(NJbinsLLPur[j])+str(MHTHTBinsLL[h]),'lnN', ['WTopSL','WtopHad'], (LLStatMuAccUp), (LLStatMuAccDown), HadTauAccStat, HadTauAccStatDn, str(NJbinsLLPur[j])+'_BTags._'+str(MHTHTBinsLL[h]))
               signalRegion.addAsymSystematic("ElecAccStat"+str(NJbinsLLPur[j])+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLStatElecAccUp), (LLStatElecAccDown),str(NJbinsLLPur[j])+'_BTags._'+str(MHTHTBinsLL[h]))        

               if options.llpOnly:signalRegion.addAsymSystematic("MuQSquareAccSys"+str(NJbinsLLPur[j])+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysMuQSquareUp), (LLSysMuQSquareDown),str(NJbinsLLPur[j])+'_BTags._'+str(MHTHTBinsLL[h]))
               else:  signalRegion.addCorrelSystematicAsym("MuQSquareAccSys"+str(NJbinsLLPur[j])+str(MHTHTBinsLL[h]),'lnN', ['WTopSL','WtopHad'], (LLSysMuQSquareUp), (LLSysMuQSquareDown), HadTauMuAccSysScaleUp, HadTauMuAccSysScaleDn,str(NJbinsLLPur[j])+'_BTags._'+str(MHTHTBinsLL[h]))
               signalRegion.addAsymSystematic("ElecQSquareAccSys"+str(NJbinsLLPur[j])+str(MHTHTBinsLL[h]),'lnN',['WTopSL'],(LLSysElecQSquareUp), (LLSysElecQSquareDown),str(NJbinsLLPur[j])+'_BTags._'+str(MHTHTBinsLL[h]))
    
    if options.allBkgs or options.tauOnly or options.llpOnly or (options.tauOnly and  options.llpOnly):
        for i in range(signalRegion.GetNbins()):
            #if(signalRegion_CSList[i]<2):
            if options.allBkgs or (options.tauOnly and  options.llpOnly): 
                    #signalRegion.addSingleSystematic('LLSCSR'+tagsForSignalRegion[i],'lnU',['WTopSLHighW'],100,'',i);
                signalRegion.addSingleSystematic('LLSCSR'+tagsForSignalRegion[i],'lnU',['WTopHadHighW','WTopSLHighW'],10000,'',i);
            if options.tauOnly and not (options.tauOnly and  options.llpOnly): signalRegion.addSingleSystematic('TAUSCSR'+tagsForSignalRegion[i],'lnU',['WTopHadHighW'],10000,'',i);
            if options.llpOnly and not (options.tauOnly and  options.llpOnly): signalRegion.addSingleSystematic('LLSCSR'+tagsForSignalRegion[i],'lnU',['WTopSLHighW'],10000,'',i);
            if options.allBkgs:
                if(signalRegion_CSList[i]>=2):signalRegion.addCorrelSystematic('LLHadTauCorrelError'+tagsForSignalRegion[i], 'lnN', ['WTopSL','WTopHad'], LLSumW2errors[i], 1+(tauSqrtSumW2[i]), '',i)            
                if(signalRegion_CSList[i]==1):signalRegion.addCorrelSystematic('LLHadTauCorrelError'+tagsForSignalRegion[i], 'lnN', ['WTopSL','WTopHad'], 2.0, 2.0, '',i)
            
            if options.llpOnly and not (options.tauOnly and  options.llpOnly):
                signalRegion.addSingleSystematic('LLSumWError'+tagsForSignalRegion[i], 'lnN', ['WTopSL'], LLSumW2errors[i], '',i)        

        for i in range(SLcontrolRegion.GetNbins()):
            if options.allBkgs or (options.tauOnly and  options.llpOnly): 
                #if(signalRegion_CSList[i]<2): 
                SLcontrolRegion.addSingleSystematic('LLSCSR'+tagsForSLControlRegion[i],'lnU',['WTopHadHighW'],10000,'',i);
            if options.tauOnly and not (options.tauOnly and  options.llpOnly):
                SLcontrolRegion.addSingleSystematic('TAUSCSR'+tagsForSLControlRegion[i],'lnU',['WTopHadHighW'],10000,'',i);
            if options.llpOnly and not (options.tauOnly and  options.llpOnly):
                SLcontrolRegion.addSingleSystematic('LLSCSR'+tagsForSLControlRegion[i],'lnU',['WTopSLHighW'],10000,'',i);        

    ### hadtau uncertainties ------------------------------------------------------------------------------
    if options.allBkgs or options.tauOnly or (options.tauOnly and  options.llpOnly):
        for i in range(signalRegion.GetNbins()):
            #tauBMistagUp[i]=1.0+tauBMistagUp[i];
            #tauBMistagDown[i]=1.0+tauBMistagDown[i];
            tauNonClosure[i]=max(tauNonClosure[i],1+tauSqrtSumW2[i])
            #if(tauNonClosure[i]<-99):tauNonClosure[i]=1.0;
            #else: tauNonClosure[i]=1.0+tauNonClosure[i]
            signalRegion.addSingleSystematic('HadTauClosure'+tagsForSignalRegion[i],'lnN',['WTopHad'],tauNonClosure[i],'',i);
            #signalRegion.addSingleSystematic('HadTauMuStat'+tagsForSignalRegion[i],'lnN',['WTopHad'],HadTauMuFromTauStat[i],'',i);
        signalRegion.addAsymSystematic('HadTauBTagShape','lnN',['WTopHad'],tauBMistagUp,tauBMistagDown);
        signalRegion.addAsymSystematic('HadTauEnergyScale','lnN',['WTopHad'],HadTauJECUncertUp,HadTauJECUncertDn);    
        #signalRegion.addAsymSystematic('HadTauMuEff', 'lnN', ['WTopHad'], HadTauMuonCorrUncDown[i], HadTauMuonCorrUncUp[i]);    
        #signalRegion.addAsymSystematic('HadTauMTStat', 'lnN', ['WTopHad'], HadTauMuonCorrUncDown[i], HadTauMuonCorrUncUp[i]);

    ### QCD uncertainties ------------------------------------------------------------------------------
    if options.allBkgs or options.qcdOnly:    

        ListOfQCDSysK1 = textToListStr(idir+"/qcd-bg-combine-input.txt",7)
        ListOfQCDSysK2 = textToListStr(idir+"/qcd-bg-combine-input.txt",8)
        ListOfQCDSysK3 = textToListStr(idir+"/qcd-bg-combine-input.txt",9)
        ListOfQCDSysK4 = textToListStr(idir+"/qcd-bg-combine-input.txt",10)
        ListOfQCDSysK5 = textToListStr(idir+"/qcd-bg-combine-input.txt",11)
        ListOfQCDSysK6 = textToListStr(idir+"/qcd-bg-combine-input.txt",12)
        ListOfQCDSysK7 = textToListStr(idir+"/qcd-bg-combine-input.txt",13)
        ListOfQCDSysK8 = textToListStr(idir+"/qcd-bg-combine-input.txt",14)    

        ListOfQCDSysK9 = textToListStr(idir+"/qcd-bg-combine-input.txt",15)
        ListOfQCDSysK10 = textToListStr(idir+"/qcd-bg-combine-input.txt",16)
        ContaminUncForLowdphiRegion = textToList(idir+"/qcd-bg-combine-input.txt",4);
        for i in range(len(tagsForSignalRegion)):
            signalRegion.addSingleSystematic("ldpCR"+str(i),'lnU','qcd',10000,'',i);
            LowdphiControlRegion.addSingleSystematic("ldpCR"+str(i),'lnU','qcd',10000,'',i);    
            if(ContaminForLowdphiRegion[i]>0.000001):LowdphiControlRegion.addSingleSystematic("contamUnc"+str(i), 'lnN','contam',1+(ContaminUncForLowdphiRegion[i]/ContaminForLowdphiRegion[i]),'',i)
        for i in range(len(ListOfQCDSysK1)):
            if(ListOfQCDSysK1[i]!='-'):signalRegion.addSingleSystematic("KQCDHT1",'lnN','qcd',float(ListOfQCDSysK1[i]),'',i);
            if(ListOfQCDSysK2[i]!='-'):signalRegion.addSingleSystematic("KQCDHT2",'lnN','qcd',float(ListOfQCDSysK2[i]),'',i);
            if(ListOfQCDSysK3[i]!='-'):signalRegion.addSingleSystematic("KQCDHT3",'lnN','qcd',float(ListOfQCDSysK3[i]),'',i);
            if(ListOfQCDSysK4[i]!='-'):signalRegion.addSingleSystematic("KQCDMHT2",'lnN','qcd',float(ListOfQCDSysK4[i]),'',i);
            if(ListOfQCDSysK5[i]!='-'):signalRegion.addSingleSystematic("KQCDMHT3",'lnN','qcd',float(ListOfQCDSysK5[i]),'',i);
            if(ListOfQCDSysK6[i]!='-'):signalRegion.addSingleSystematic("KQCDMHT4",'lnN','qcd',float(ListOfQCDSysK6[i]),'',i);
            if(ListOfQCDSysK7[i]!='-'):signalRegion.addSingleSystematic("KQCDNJ2",'lnN','qcd',float(ListOfQCDSysK7[i]),'',i);
            if(ListOfQCDSysK8[i]!='-'):signalRegion.addSingleSystematic("KQCDNJ3",'lnN','qcd',float(ListOfQCDSysK8[i]),'',i);
            if(ListOfQCDSysK9[i]!='-'):signalRegion.addSingleSystematic("KQCDNJ4",'lnN','qcd',float(ListOfQCDSysK9[i]),'',i);
            if(ListOfQCDSysK10[i]!='-'):signalRegion.addSingleSystematic("KQCDNJ5",'lnN','qcd',float(ListOfQCDSysK10[i]),'',i);

    ######################################################################
    ######################################################################
    # 4. Write Cards
    ######################################################################
    ######################################################################    

    signalRegion.writeCards( odir );
    if options.allBkgs or options.llpOnly or  (options.tauOnly and  options.llpOnly) or options.tauOnly: SLcontrolRegion.writeCards( odir );
    # if options.allBkgs or options.tauOnly: HadcontrolRegion.writeCards( odir );
    if options.allBkgs or options.zvvOnly: sphotonRegion.writeCards( odir );
    if options.allBkgs or options.qcdOnly: LowdphiControlRegion.writeCards( odir );

