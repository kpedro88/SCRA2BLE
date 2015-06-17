#ifndef KBUILDER_H
#define KBUILDER_H
#define TreeClass_cxx

//custom headers
#include "KMap.h"
#include "KMath.h"
#include "KParser.h"
#include "KBase.h"
#include "TreeClass.h"
#include "KSelection.h"

//custom headers for weighting
#include "../btag/GetBtagScale.C"

//ROOT headers
#include <TROOT.h>
#include <TFile.h>
#include <TH1.h>
#include <TProfile.h>
#include <TH2.h>
#include <TStyle.h>
#include <TLorentzVector.h>

//STL headers
#include <vector>
#include <string>
#include <iostream>
#include <map>

using namespace std;

void TreeClass::Loop() {}

//---------------------------------------------------------------
//histo builder class - loops over tree to fill histos for a base
class KBuilder : public TreeClass {
	public:
		//constructors
		KBuilder() : TreeClass(), MyBase(0), localOpt(0), globalOpt(0), MySelection(0) {
			//must always have local & global option maps
			if(localOpt==0) localOpt = new OptionMap();
			if(globalOpt==0) globalOpt = new OptionMap();
		}
		KBuilder(KBase* MyBase_, TTree* tree_, KSelection<KBuilder>* sel_) : TreeClass(tree_), MyBase(MyBase_), localOpt(MyBase->GetLocalOpt()), globalOpt(MyBase->GetGlobalOpt()), MySelection(sel_) {
			//must always have local & global option maps
			if(localOpt==0) localOpt = new OptionMap();
			if(globalOpt==0) globalOpt = new OptionMap();
			//pass self to selection; also sets looper for selectors, variation, variators
			MySelection->SetLooper(this); 
		}
		//destructor
		virtual ~KBuilder() {}

		//functions for histo creation
		virtual bool Cut() { //this implements the set of cuts common between data and MC
			bool goodEvent = true;
		
			return (goodEvent && MySelection->DoSelection());
		}
		virtual double Weight() { return 1.; }
		virtual void Loop() {
			if (fChain == 0) return;
			
			//initial loop to get histo variables
			int table_size = MyBase->GetTable().size();
			vars.clear(); vars.reserve(table_size);
			htmp.clear(); htmp.reserve(table_size);
			HMit sit;
			for(sit = MyBase->GetTable().begin(); sit != MyBase->GetTable().end(); sit++){
				//get histo name
				string stmp = sit->first;
				htmp.push_back(sit->second);
				//split up histo variable names
				vector<string> vars_tmp;
				KParser::process(stmp,'_',vars_tmp);
				vars.push_back(vars_tmp);
			}
			
			//check for branches to enable/disable
			vector<string> disable_branches;
			globalOpt->Get("disable_branches",disable_branches);
			for(unsigned b = 0; b < disable_branches.size(); ++b){
				fChain->SetBranchStatus(disable_branches[b].c_str(),0);
			}
			vector<string> enable_branches;
			globalOpt->Get("enable_branches",enable_branches);
			for(unsigned b = 0; b < enable_branches.size(); ++b){
				fChain->SetBranchStatus(enable_branches[b].c_str(),1);
			}
			
			//loop over ntuple tree
			Long64_t nentries = fChain->GetEntries();
			bool debugloop = globalOpt->Get("debugloop",false);
			Long64_t nbytes = 0, nb = 0;
			for (Long64_t jentry=0; jentry<nentries;jentry++) {
				Long64_t ientry = LoadTree(jentry);
				if (ientry < 0) break;
				nb = fChain->GetEntry(jentry);   nbytes += nb;
				if(debugloop && jentry % 10000 == 0) cout << MyBase->GetName() << " " << jentry << "/" << nentries << endl;
				
				Cut();
			}
			
			//final steps
			if(globalOpt->Get("debugcut",false)) MySelection->PrintEfficiency(MySelection->GetSelectorWidth(),nentries);
			
			if(globalOpt->Get("plotoverflow",false)){
				for(int h = 0; h < htmp.size(); h++){
					if(vars[h].size()==2) continue; //not implemented for 2D histos or profiles yet
					
					//temporary histo to calculate error correctly when adding overflow bin to last bin
					TH1* otmp = (TH1*)htmp[h]->Clone();
					otmp->Reset("ICEM");
					int ovbin = htmp[h]->GetNbinsX()+1;
					double err = 0.;
					otmp->SetBinContent(ovbin-1,htmp[h]->IntegralAndError(ovbin,ovbin,err));
					otmp->SetBinError(ovbin-1,err);
					
					//add overflow bin to last bin
					htmp[h]->Add(otmp);
					
					//remove overflow bin from htmp[h] (for consistent integral/yield)
					htmp[h]->SetBinContent(ovbin,0);
					htmp[h]->SetBinError(ovbin,0);
					
					delete otmp;
				}
			}
		}	

	public:
		//member variables
		KBase* MyBase;
		OptionMap* localOpt;
		OptionMap* globalOpt;
		KSelection<KBuilder>* MySelection;
		vector<vector<string> > vars;
		vector<TH1*> htmp;
};

void KBase::Build(){
	if(!isBuilt) {
		if(MyBuilder==0) MyBuilder = new KBuilder(this,tree,MySelection);
		MyBuilder->Loop(); //loop over tree to build histograms
		isBuilt = true;
	}
}

//---------------------------------------------------------
//extension of builder class for data - has blinding option
class KBuilderData : public KBuilder {
	public:
		//constructors
		KBuilderData() : KBuilder() { }
		KBuilderData(KBase* MyBase_, TTree* tree_, KSelection<KBuilder>* sel_) : KBuilder(MyBase_,tree_,sel_) {
			//get options
			blind = globalOpt->Get("blind",false);
		}
		//destructor
		virtual ~KBuilderData() {}
		
		//functions for histo creation
		bool Cut(){
			bool goodEvent = true;
			
			//special blinding option for data (disabled by default)
			if(blind){
				//do not look at signal region
				//could make this setting into a double value for variable blinding...
			}
			
			//KBuilder::Cut() comes *last* because it includes histo filling selector
			return (goodEvent && KBuilder::Cut());
		}
		
		//member variables
		bool blind;
};

void KBaseData::Build(){
	if(!isBuilt) {
		if(MyBuilder==0) MyBuilder = new KBuilderData(this,tree,MySelection);
		MyBuilder->Loop(); //loop over tree to build histograms
		isBuilt = true;
	}
}

//------------------------------------------------------------------------------------------------------------
//extension of builder class for MC - has weighting (corrections & normalization), extra cuts (fake tau, etc.)
class KBuilderMC : public KBuilder {
	public:
		//constructors
		KBuilderMC() : KBuilder() { }
		KBuilderMC(KBase* MyBase_, TTree* tree_, KSelection<KBuilder>* sel_) : KBuilder(MyBase_,tree_,sel_) { 
			//get options
			normtype = ""; localOpt->Get("normtype",normtype);
			nEventProc = 0; got_nEventProc = localOpt->Get("nEventProc",nEventProc);
			xsection = 0; got_xsection = localOpt->Get("xsection",xsection);
			norm = 0; got_luminorm = globalOpt->Get("luminorm",norm);
			
		}
		//destructor
		virtual ~KBuilderMC() {}
		
		//functions for histo creation
		bool Cut(){
			bool goodEvent = true;
			
			//check normalization type here
		
			//KBuilder::Cut() comes *last* because it includes histo filling selector
			return (goodEvent && KBuilder::Cut());
		}
		double Weight(){
			double w = 1.;
			
			//check option in case correction types are disabled globally
			//(enabled by default
			//(*disabled* until 2015 data is available)
			/*
			if(globalOpt->Get("pucorr",false)) {
				TH1F* puWeights;
				globalOpt->Get("puWeights",puWeights);
				w *= puWeights->GetBinContent(puWeights->GetXaxis()->FindBin(trueNInteraction));
			}
			
			if(globalOpt->Get("btagcorr",false)) {
				int bSF = 0;
				int mSF = 0;
				globalOpt->Get("btagSFunc",bSF);
				globalOpt->Get("mistagSFunc",mSF);
				//todo: add dependence on # btags
				w *= GetBtagScale(PFJetPt,PFJetEta,PFJetPartonFlavour,bSF,mSF);
			}
			*/
			
			//now do scaling: norm*xsection/nevents
			//should this be a separate function using Scale()?
			if(got_nEventProc && nEventProc>0 && got_xsection) w *= xsection/nEventProc;			
			
			//use lumi norm (default)
			if(got_luminorm) w *= norm;
			
			return w;
		}

		//member variables
		bool got_nEventProc, got_xsection, got_luminorm;
		string normtype;
		int nEventProc;
		double xsection, norm;
};

void KBaseMC::Build(){
	if(!isBuilt) {
		if(MyBuilder==0) MyBuilder = new KBuilderMC(this,tree,MySelection);
		MyBuilder->Loop(); //loop over tree to build histograms
		isBuilt = true;
	}
}

#endif
