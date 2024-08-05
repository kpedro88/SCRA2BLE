# SCRA2BLE

The RA2 SCRA2BLE integration code is designed to perform the necessary steps to produce the results, diagnostics,and statistical 
interpretations by combining the latest version of the background estimates into a figure or into a likelihood model. The two folders in this repository split the code into these two main functions: plotting integration results  (PubPlots) and performing likelihood fitting or diagonostics (DatacardBuilder). 

The current version of the code is based on the legacy 13 TeV [RA2 analysis](https://arxiv.org/abs/1908.04722), which 
used 174 search bins with seperate background inputs for each Run era based on the data taking periods in 2016, 2017, 2018 
(further split by HEM affected runs). The analysis used the RA2 production from the [Treemaker](https://github.com/TreeMaker/TreeMaker/tree/Run2_2017) and the signal histograms from the V17 signal samples. 

## Setup 

This was the release used for the Legacy analysis:
```	
cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src 
```	
Include the Higgs combine tool code and compile:
```
git -b 81x-root606 clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v7.0.11
scramv1 b clean; scramv1 b  
```

Note that future versions of the analysis the combine tool recipe would be updated for new CMSSW releases like (e.g. 10X and beyond). Find the latest instructions on the [CombineToolTwiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit). 

Also in order to complete the full set of [pre-approval checks](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSPAGPreapprovalChecks) it is also necessary to use the [CombineHarvester](http://cms-analysis.github.io/CombineHarvester/) in order to compute the impact of each nuisance parameter.

```
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
```


```
git clone -b Run2LegacyPub  https://github.com/rpatelCERN/SCRA2BLE.git
```

## pMSSM instructions

The code is somewhat reorganized to handle the THnSparse format used to organize pMSSM signals.

The default approach is to run over an entire group of signals at once, resulting in a single output file that can be used to produce datacards for any signal in the group:
```bash
python processSignal.py --signal pMSSM --lumi 137.4 --set set1prompt1 --sigDir root://cmseos.fnal.gov//store/user/lpcpmssm/Datacards/Run2ProductionV17_v1
python makeDatacards.py --signal pMSSM --lumi 137.4 --params set1prompt1 355 11107 --sigDir . --realData
```

To validate this approach, a given signal model can first be projected out and then processed:
```bash
python makeProjection.py --params set1prompt1 355 11107
python processSignal.py --signal pMSSM --lumi 137.4 --masses 355 11107 --sigDir .
python makeDatacards.py --signal pMSSM --lumi 137.4 --masses 355 11107 --sigDir . --realData
```

These two approaches should produce the same output, modulo minor floating point differences.

Once a datacard is created, the next step is to run Combine, get the likelihood, and extract Z-scores and Bayes factors:
```bash
python runCombine.py --signal pMSSM --lumi 137.4 --params set1prompt1 355 11107
```

These two steps (making datacards and running Combine) can be done at once (choosing a different model point by changing the value of `--firstJob`):
```bash
python runJob.py --signal pMSSM --lumi 137.4 --realData --sigDir root://cmseos.fnal.gov//store/user/lpcpmssm/Datacards/Run2ProductionV17_v1 --params set1prompt1 -1 -1 --firstJob 0 --split 1
```

To submit Condor jobs for the entire set of signal models:
```bash
(cd batch; ./RCcheck.sh)
python submitCombine.py --signal pMSSM --set set1prompt1 --split 200
```
then `hadd` the results:
```bash
./batch/haddEOS.sh -i results_set1prompt1 -x root://cmseos.fnal.gov/ -d /store/user/lpcpmssm/Datacards/Run2ProductionV17_v1 -g _part -r
```

To find any missing models from the results:
```bash
root -b -l -q 'findMissing.C+("set1prompt1")'
```

To resubmit the missing models:
```bash
python submitCombine.py --signal pMSSM --set set1prompt1 --split 1 --missing missing_set1prompt1.txt
```


## Building DataCards for the Combine Tool

The python scripts in DatacardBuilder are designed to take the input bkg estimate histograms as well as an input SMS fastSIM signal point and create datacards for the combine tool.
The code is in analysisBuilderCondor.py, and includes various options to call methods in the Higgs Combine tool. The scripts also include plotting code for the 2D interpretations,
which include the cross-section UL, signal significance, and signal efficiency. An example command is shown below for a single signal point:

```
python analysisBuilderCondor.py --signal T1bbbb --mGo 1500 --mLSP 100 --fastsim --realData --CombOpt=AsymptoticUL
```

The options specified for the signal point: 

```
--signal T1bbbb --mGo 1500 --mLSP 100 
```

bool options below specify that the input signal is fastsim (as opposed to FullSIM) and to use the unblinded data for the observation (otherwise use the sum of the total bkg)

```
--fastsim --realData
```

The last option specifies which method to run in the combine code: 

```
--CombOpt=AsymptoticUL #(or MaxLiklihood, Significance, FitCovariance, ImpactsInitialFit)
```

The option for AsymptoticUL just runs the Asymptotic upper limits. The other options call different combine methods: 
- MaxLiklihood computes the post-fit background yields which are input to the plotting code in the next section
- Fit Covaraince performs the maxlikelihood fit and throws toys to compute the covariance matrix
- ImpactsInitialFit calls the Combine Harvester tool to fit the likelhood and nuisances (need this is the right format to compute the nuisance impacts)
- The Significance calls the ProfileLikelihood method to compute the observed significance

### Notes on buildCards-AllBkgsMassScan.py

The main part of the RA2 integration code is buildCards-AllBkgsMassScan.py, which is the code that defines the the background central values, the background uncertainities as nuisance parameters, the signal yields, and signal nuisance parameters. This code is called within  analysisBuilderCondor.py to create the list of datacards (one per RA2 bin) for the combine tool options. The code relies on a set of background inputs where the central value is binned in a 174 bin histogram, each uncertainty is also filled in a 174 bin histogram with the nuisance parameter name defined in the x-axis bin labels. The bin-labels then allow for creating correlations across the 4D search bins for the bkg systematics. 

The steps below walk through the main functions of the buildcards code. 

1. Merging Run periods: Since the code by default runs over 4 run eras (MC2016,MC2017,MC2018, MC2018HEM) the signal is merged accounting for the lumi of each run period in the function NominalSignal, which makes use of the functions in SignalMergePeriods.py. This step merges the signal for each run period, computes the genMHT systematic, and if there are leptons in the signal accounts for the signal degradation due to contamination in the lost-lepton control sample. TestNominal is a list containing the signal yield histogram and the gen MHT systematic (accounting for mismodeling in FastSIM). NOTE: This step can be modified to run over a single run period by passing a single run era and lumi to NominalSignal.
2. tagsForSignalRegion defines the name of the RA2 bins based on the bin labels (NJetsW_BTagsX_MHTY_HTZ) and the signal and background contributions, (signal, Zvv, Lost-lepton, QCD multijet). This defines the structure of the rate line in the data card and provides a label for uncorrelated signal systematics.
3. options.realData is the flag that is set to unblind the data stored in the input histogram for the search region, if it is false then the datacard observations will just contain the total background. The central value yields are stored in a TFile in the output directory (yields.root)
4.The names of the background systematics are defined in lists in lines 286-292. The lists are seperated according to the bkg contribution. The Zvv systematics are further split according to symmetric, asymmetric, and control stat yield histograms. The nuisance lines are then written for each bkg contribution in the functions: WriteZSystematics,WriteQCDSystematics,and WriteLostLeptonSystematics.
4. The final stage adds the signal systematics LN 298 adds the lnU for the MHT systematic (which was computed in the first step). The remaining systematics need to be properly merged according to whether or not they are correlated or uncorrelated across run periods. This is done in WriteSignalSystematics using the functions defined in SignalMergePeriods.py. 


### Preapproval Checks
A number of the [pre-approval checks](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSPAGPreapprovalChecks) can be done with the MaxLiklihood option using analysisBuilderCondor.py. (Use the modifications recommended in the page to toggle between the expectSignal=0, 1 hypotheses). The output results of the MaxLiklihood fit can be plotted and examined using 
```
python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py 
```
The above code provides either a table or a plot (specified by the options) can be used to test the behavior of certain nuisance parameters. We expect correlations in the background uncertainty to shrink the uncertainty on a nuisance parameter after the fit. 

The nuisance impacts can be computationally intensive due to the large number of nuisance parameters in the RA2 likelihood model. It is useful then to break up the impacts into jobs per background estimate or signal in the last step: QCD, Zvv, Lost-lepton, and signal. The procedure for computing Impacts is shown on this twiki:[Nuisance_parameter_impacts](https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWG/SWGuideNonStandardCombineUses#Nuisance_parameter_impacts)
The steps below show how to produce an impact plot for a subset of nuisances using the RA2 code:
1. Derive the initial fit to the likelihood using the command for analysisBuilderCondor.py --CombOpt=ImpactsInitialFit. This will produce a file: higgsCombine_initialFit_Test.MultiDimFit.mH125.root
This will be used for plotting the fitted mu and uncertainty and to find the fitted nuisance parameters
2. Fit each nuisance parameter as POI. It would take a long time to fit all of them, so in the script QuickNuisnce.py I show how you can run over subsets in batch jobs (the script uses the CU cluster with the Qsub command but it could be adapted to other clusters or the LPC).
3. Create a Json of all the fitted parameters and their uncertainties. 
4. Read in the JSON and produce the impacts plot

The full set of commands is shown for an example signal point here:

```
python analysisBuilderCondor.py --signal T1tttt --mGo 950 --mLSP 700 --fastsim --realData --eos root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/ --CombOpt=ImpactsInitialFit

combine -M MultiDimFit --robustFit 1 -t -1 --expectSignal 0 -n _paramFit_Test_zvvgJNobs_NJets4_MHT1_HT4 --rMin=-10 --rMax=10 --algo impact --redefineSignalPOIs r -P zvvgJNobs_NJets4_MHT1_HT4 --floatOtherPOIs 1 --saveInactivePOI 1 -m 125 -d testCards-Moriond-T1tttt_950_700-137.4/allcards.root
####Sumbit to batch as: python QuickNuisnce.py testCards-Moriond-T1tttt_950_700-137.4

combineTool.py -M Impacts -d testCards-Moriond-T1tttt_950_700-137.4/allcards.root -m 125 -o impacts.json
plotImpacts.py -i impacts.json -o impacts
```
The results in an impacts plot stored in impacts.pdf

### Covariance /Correlation Matrices
This matrix is generated using the FitCovariance option for analysisBuilderCondor.py which gives an output file like: fitDiagnosticstestCards-Moriond-XXXX.root (XXXX=output directory name)
The covariance matrix is already stored in shapes_prefit/overall_total_covar. 

The Covariance matrix can be checked and also used to create the correlation matrix using: plottingStuff/QuickCovarianceFormat.C . This code orders the covariance matrix according to bin number, cross-checks the diagonal against the known pre-fit uncertainties from the inputs (store these in PrefitUnc.root), and computes a correlation matrix. 
The matrices are plotted with plottingStuff/QuickCovariancePASPlot.C 

```
cd plottingStuff
root -b 'QuickCovarianceFormat.C(fname)'
root -b 'QuickCovariancePASPlot.C'  
```

### Submitting Jobs
A single python script is used to run a 2D scan for a signal sample for the two main cases: Upper Limits and significance
```
python launchSCRA2BLE.py --fastsim --model=T1tttt --keeptar --lpc --CombOpt AsymptoticUL --inDir /store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/ --outDir=/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/
```

The python script runs by default on the lpc but can be modified to run on other clusters. The flag --lpc uses the mode that submits jobs to LPC condor. 
The code tars the CMSSW area and creates a condor submission area in a new directory called tmp/. The option --keeptar keeps a tar file that is already made  for a new job for a new model set by --model. The remaining parameters define the input and output directories (in this example they are both on LPC eos).  

### Generating 2D Scan Histograms

The key 2D scans for signal for the RA2 analysis are the signal efficiency, observed significance and upper limit contours and obs limits. The scripts to create 2D smoothed histograms and contours are in DatacardBuilder/plottingStuff. 

For Signal efficiency is the simplest because it is plotted directly from the signal datacards and the efficiency is computed by dividing the cross-section out from the 
integral of the signal over the 174 search bins (gives N_passed/N_total). The script requires a list of files per model and an input list of cross sections (I made formatted .txt files from [SUSY Cross-Sections](https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections). 

An example scan:

```
cd plottingStuff/
python PlotMassContoursSmoothEfficiency.py --model=T1bbbb --xsec=LatestGluGluNNLO.txt --idir=/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/
```

This produces an output file MassScanT1bbbb.root containing a histogram of efficiencies in the 2D mass plane of the T1bbbb model. By default the signal efficiency for models with leptons is adjusted (by degraded the efficiency according to the 1-lepton signal contamination) and the efficiency is computed using the average of the reco MHT and gen MHT binning. The code is setup to run over 4 run eras 2016, 2017, 2018, 2018HEM, but can be modified to just do a single run period.

The significance scan is produced in a similar way using PlotMassContoursSmoothSignif.py where the arguments are the same but the list of files are the resultsYYYY.root (where YYYY are the files made using analysisBuilderCondor.py with the option Significance). 

```
cd plottingStuff/
ls /eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/Signif/results*T1bbbb*.root > listofFilesT1bbbb.txt
python PlotMassContoursSmoothSignif.py --model=T1bbbb --xsec=LatestGluGluNNLO.txt --idir=/eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/Signif/
 ```
This produces an output file MassScanT1bbbb.root which contains the observed significance in the 2D mass plane. 

Finally producing the Obs limit in the 2D plane along with the Expected, Observed contours is done in PlotMassContoursSmoothLimit.py

```
cd plottingStuff/
ls /eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/results*T1bbbb*.root > listofFilesT1bbbb.txt
python PlotMassContoursSmoothLimit.py --model=T1bbbb --xsec=LatestGluGluNNLO.txt --idir=/eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond2019/
```

This will output a file MassScanT1bbbb.root for the Obs and Exp limits in the 2D mass plane as well as the contours for the obs limit, the theory uncertainty, the expected limit (medium, +/- 1sigma, +/- 2sigma)

Just a few notes about the code:
-To create a smooth 2D histogram all of the above code uses TGraph2D where the size of the bins is hard coded in the scripts (this can be adjusted)
-T2qq is a model with 8-squarks but is also used to do the single 1 quark limit, by default in the script the contours drawn are for signal strength of 1.0,
but for the single quark this needs to be adjusted to be 1/8 of the total xsec, so this needs to be changed in the script when running over this model. 
-The significance needs additional smoothing when there are fluctations, this can be done by removing points in the TGraph2D and reinterpolating
-The contours of the limit also sometimes need additional smoothing, which can be done in root using the TGraphSmoothClass and SmoothSuper. 

### Plotting 2D scans
The code used to plot results for 2D SMS mass scans is based on the repository [PlotsSMS](https://github.com/CMS-SUS-XPAG/PlotsSMS) but is modified a bit for the RA2 analysis and the various 2D scans required for the publication and additional material. Each of the folders have the same method for plotting, but have titles, axis labels, and latex text adjusted accordingly. The PlotsSMSLimits/ and PlotsSMST2qqLimits/ folders contain the code to plot the limit contours and the observed limit in the 2D mass plane (The T2qq is a special case because there are two sets of contours for the single and 8-squark models). 

```
cd PlotsSMSLimits/
python python/makeSMSplots.py config/SUS12024/T1tttt_SUS12024.cfg OUTPUTFILENAME
```

The above code reads the histograms and TGraphs defined in T1tttt_SUS12024.cfg and makes a plot from the TFile in the config. The definitions of the signal model and plot ranges are configured in sms.py . New models and corresponding cfg files can be included. The above call is identical for the significance and signal efficiency, the only difference is that only the 2D histogram defined in the .cfg files is used. 

NOTE: 
-The arxiv number is hard coded to the legacy analysis but can be adjusted. 
-T2tt model for the legacy analysis is always blinded in the bottom left corned of the stop corridor, but this may change someday
-You must put the input histograms in the folder with the cfg file

