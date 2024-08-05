#include <TFile.h>
#include <TTree.h>

#include <string>
#include <iostream>
#include <fstream>
using namespace std;

void findMissing(const string& setname){
	string idfname = "root://cmseos.fnal.gov//store/user/lpcpmssm/SLHATrees/"+setname+".root";
	auto idfile = TFile::Open(idfname.c_str());
	auto idtree = (TTree*)idfile->Get("mcmc");

	string resfname = "root://cmseos.fnal.gov//store/user/lpcpmssm/Datacards/Run2ProductionV17_v1/results_"+setname+".root";
	auto resfile = TFile::Open(resfname.c_str());
	auto restree = (TTree*)resfile->Get("mcmc");
	restree->BuildIndex("chain_index","Niteration");

	int id1, id2;
	idtree->SetBranchAddress("chain_index",&id1);
	idtree->SetBranchAddress("iteration_index",&id2);

	ofstream ofile("missing_"+setname+".txt");
	int counter = 0;
	for(int ientry = 0; ientry < idtree->GetEntries(); ++ientry){
		idtree->GetEntry(ientry);
		auto jentry = restree->GetEntryNumberWithIndex(id1,id2);
		if(jentry==-1){
			ofile << id1 << " " << id2 << endl;
			++counter;
		}
	}
	ofile.close();
	cout << "Missing: " << counter << endl;
}
