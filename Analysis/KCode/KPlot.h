#ifndef KPLOT_H
#define KPLOT_H

//custom headers
#include "KMap.h"
#include "KLegend.h"
#include "KParser.h"

//ROOT headers
#include <TROOT.h>
#include <TLegend.h>
#include <TPaveText.h>
#include <TH1.h>
#include <TH1F.h>
#include <TProfile.h>
#include <TH2.h>
#include <TH2F.h>
#include <TCanvas.h>
#include <TPad.h>
#include <TLine.h>
#include <TLatex.h>
#include <TAxis.h>
#include <TExec.h>

//STL headers
#include <vector>
#include <string>
#include <sstream>
#include <iostream>

using namespace std;

//-----------------------------------------------------------
//class to store root drawing objects and do histo formatting
//also contains histo-specific options
class KPlot{
	public:
		//constructor
		KPlot() : name(""), localOpt(0), globalOpt(0), histo(0), ratio(0), exec(0), isInit(false), 
				  can(0), pad1(0), pad2(0), leg(0), paveCMS(0), paveExtra(0), paveLumi(0), line(0),
				  pad1W(0), pad1H(0), pad2W(0), pad2H(0)
		{
			//must always have local & global option maps
			if(localOpt==0) localOpt = new OptionMap();
			if(globalOpt==0) globalOpt = new OptionMap();
			
			SetStyle();
		}
		//universal size values set in initialization list
		KPlot(string name_, OptionMap* localOpt_, OptionMap* globalOpt_) : name(name_), localOpt(localOpt_), globalOpt(globalOpt_), histo(0), ratio(0), exec(0), isInit(false),
																	   can(0), pad1(0), pad2(0), leg(0), paveCMS(0), paveExtra(0), paveLumi(0), line(0),
																	   pad1W(0), pad1H(0), pad2W(0), pad2H(0)
		{
			//must always have local & global option maps
			if(localOpt==0) localOpt = new OptionMap();
			if(globalOpt==0) globalOpt = new OptionMap();
			
			//enable histo errors
			TH1::SetDefaultSumw2(kTRUE);
			
			SetStyle();
		}
		//initialization
		void SetStyle(){
			//canvas sizes
			canvasW = 700; globalOpt->Get("canvasW",canvasW);
			canvasH = 550; globalOpt->Get("canvasH",canvasH);
			canvasWextra = 4;
			canvasHextra = 28;
			
			//margins
			marginL = 95; globalOpt->Get("marginL",marginL);
			marginR = 35; globalOpt->Get("marginR",marginR);
			marginB = 75; globalOpt->Get("marginB",marginB);
			marginT = 35; globalOpt->Get("marginT",marginT);
			marginM1 = 15; globalOpt->Get("marginM1",marginM1);
			marginM2 = 10; globalOpt->Get("marginM2",marginM2);
			marginPal = 0; //only used in KPlot2D for palette axis
			
			//automatic calculation of ratio extension height
			//to ensure plot area on pad1 equal to non-ratio case, given 5/7 for pad1, 2/7 for pad2
			ratioH = canvasH*2./5.+(marginM1-marginB)*7./5.;
			
			//todo: make relative size of pad2 vs pad1 configurable
			
			//font sizes
			sizeT = 32; globalOpt->Get("sizeT",sizeT);
			sizeL = 28; globalOpt->Get("sizeL",sizeL);
			sizeP = 26; globalOpt->Get("sizeP",sizeP);
			sizeTick = 12; globalOpt->Get("sizeTick",sizeTick);
			sizeLoff = 5; globalOpt->Get("sizeLoff",sizeLoff);
			epsilon = 2; globalOpt->Get("epsilon",epsilon);
			
			//todo: font types
			
			//axis divisions
			NdivX = 507; globalOpt->Get("NdivX",NdivX);
			NdivYhisto = 510; globalOpt->Get("NdivYhisto",NdivYhisto);
			NdivYratio = 503; globalOpt->Get("NdivYratio",NdivYratio);
		}
		virtual void CreateHist(){
			//check for TProfile case
			vector<string> vars;
			KParser::process(name,'_',vars);
			
			//construct histogram		
			vector<double> xbins;
			int xnum;
			double xmin, xmax;
			if(localOpt->Get("xbins",xbins)){ //variable binning case
				if(vars.size()==2) histo = new TProfile(name.c_str(),"",xbins.size()-1,&xbins[0]);
				else histo = new TH1F(name.c_str(),"",xbins.size()-1,&xbins[0]);
				isInit = true;
			}
			else if(localOpt->Get("xnum",xnum) && localOpt->Get("xmin",xmin) && localOpt->Get("xmax",xmax)){ //standard binning case
				if(vars.size()==2) histo = new TProfile(name.c_str(),"",xnum,xmin,xmax);
				else histo = new TH1F(name.c_str(),"",xnum,xmin,xmax);
				isInit = true;
			}
			else { //no/incomplete binning information, build failed
				isInit = false;
				return;
			}
			string xtitle, ytitle;
			localOpt->Get("xtitle",xtitle);
			localOpt->Get("ytitle",ytitle);
			histo->GetXaxis()->SetTitle(xtitle.c_str());
			histo->GetYaxis()->SetTitle(ytitle.c_str());
			
			//assign bin labels if requested
			if(localOpt->Get("xbinlabel",false)){
				vector<string> labels;
				//check both option maps
				bool has_labels = localOpt->Get("xlabels",labels) || globalOpt->Get(vars[0]+"_labels",labels);
				if(has_labels){
					histo->LabelsOption("v","X");
					for(unsigned b = 0; b < labels.size(); b++){
						histo->GetXaxis()->SetBinLabel(b+1,labels[b].c_str());
					}
				}
			}
		}
		virtual bool Initialize(TH1* histo_=NULL){
			if(isInit) return isInit;
			
			histo = histo_;
			if(!histo) CreateHist();
			if(!histo) return isInit; //histo creation failed
			
			//plotting with ratio enabled by default
			if(localOpt->Get("ratio",true)) {
				
				canvasH += ratioH;
				//can = new TCanvas(histo->GetName(),histo->GetName(),700,700);
				//account for window frame: 2+2px width, 2+26px height
				can = new TCanvas(name.c_str(),name.c_str(),canvasW+canvasWextra,canvasH+canvasHextra);
				//500/(5/7) = 700

				//setup histo and ratio areas for canvas
				pad1 = new TPad("graph","",0,2./7.,1.0,1.0);
				pad1W = pad1->GetWw()*pad1->GetAbsWNDC();
				pad1H = pad1->GetWh()*pad1->GetAbsHNDC();
				pad1->SetMargin(marginL/pad1W,marginR/pad1W,marginM1/pad1H,marginT/pad1H);
				pad1->SetTicks(1,1);
				if(localOpt->Get("logy",true)) pad1->SetLogy(); //logy on by default (i.e. liny off by default)
				if(localOpt->Get("logx",false)) pad1->SetLogx(); //logx off by default (i.e. linx on by default)
				pad1->Draw();
			
				pad2 = new TPad("dmc","",0,0,1.0,2./7.);
				pad2W = pad2->GetWw()*pad2->GetAbsWNDC();
				pad2H = pad2->GetWh()*pad2->GetAbsHNDC();
				can->cd();
				pad2->SetMargin(marginL/pad2W,marginR/pad2W,marginB/pad2H,marginM2/pad2H);
				pad2->SetTicks(1,1);
				pad2->Draw();
			
				//format ratio histo
				ratio = (TH1F*)histo->Clone();
				ratio->SetMarkerStyle(20);
				ratio->SetMarkerColor(kBlack);
				ratio->SetLineColor(kBlack);
				FormatHist(pad2,ratio);
				ratio->GetYaxis()->SetRangeUser(0.45,1.55);
				
				string rationame = "Data/MC";
				globalOpt->Get<string>("rationame",rationame); //ratio name could be provided by user
				ratio->GetYaxis()->SetTitle(rationame.c_str());
				
				//note: axis titles are middle-aligned
				SetTitleOffset(pad2,ratio->GetXaxis());
				SetTitleOffset(pad2,ratio->GetYaxis());
				
				//special formatting for blank histo
				SetTitleOffset(pad1,histo->GetYaxis());
				FormatHist(pad1,histo);
				histo->GetXaxis()->SetLabelOffset(999);
				histo->GetXaxis()->SetTitle("");
				
				//make line
				pad2->cd();
				line = new TLine(ratio->GetXaxis()->GetXmin(),1,ratio->GetXaxis()->GetXmax(),1);
				line->SetLineStyle(2);
				line->SetLineWidth(2);
				line->SetLineColor(kRed);
			}
			else {
				//can = new TCanvas(histo->GetName(),histo->GetName(),700,550);
				//account for window frame: 2+2px width, 2+26px height
				can = new TCanvas(name.c_str(),name.c_str(),canvasW+canvasWextra,canvasH+canvasHextra);
			
				pad1 = new TPad("graph","",0,0,1,1);
				pad1W = pad1->GetWw()*pad1->GetAbsWNDC();
				pad1H = pad1->GetWh()*pad1->GetAbsHNDC();
				pad1->SetMargin(marginL/pad1W,marginR/pad1W,marginB/pad1H,marginT/pad1H);
				pad1->SetTicks(1,1);
				if(localOpt->Get("logy",true)) pad1->SetLogy(); //logy on by default (i.e. liny off by default)
				if(localOpt->Get("logx",false)) pad1->SetLogx(); //logx off by default (i.e. linx on by default)
				pad1->Draw();

				FormatHist(pad1,histo);
				SetTitleOffset(pad1,histo->GetXaxis());
				SetTitleOffset(pad1,histo->GetYaxis());
			}
			
			InitializePaves();
			
			//create legend
			leg = new KLegend(pad1,localOpt,globalOpt);
			
			return isInit;
		}
		void InitializePaves(){
			pad1->cd();
			
			//setup CMS text
			TLatex width_test_cms(0,0,"CMS");
			width_test_cms.SetTextSize(sizeP/pad1H);
			double posP = 1-(marginT-1)/pad1H;
			double uminCMS = marginL/pad1W;
			double umaxCMS = marginL/pad1W + width_test_cms.GetXsize();
			paveCMS = new TPaveText(uminCMS,posP,umaxCMS,1.0,"NDC");
			paveCMS->SetFillColor(0);
			paveCMS->SetBorderSize(0);
			paveCMS->SetTextFont(61);
			paveCMS->SetTextSize(sizeP/pad1H);
			paveCMS->AddText("CMS");
			
			//setup prelim text
			//todo: add option to enable/disable/change
			double sizePextra = sizeP - 3; //smaller
			string prelim_text = " Preliminary";
			globalOpt->Get("prelim_text",prelim_text);
			TLatex width_test_extra(0,0,prelim_text.c_str());
			width_test_extra.SetTextSize(sizePextra/pad1H);
			double uminExtra = umaxCMS;
			double umaxExtra = uminExtra + width_test_extra.GetXsize();
			paveExtra = new TPaveText(uminExtra,posP,umaxExtra,1.0,"NDC");
			paveExtra->SetFillColor(0);
			paveExtra->SetBorderSize(0);
			paveExtra->SetTextFont(52);
			paveExtra->SetTextSize(sizePextra/pad1H);
			paveExtra->AddText(prelim_text.c_str());
			
			//setup lumi text
			double intlumi = 0;
			globalOpt->Get<double>("luminorm",intlumi);
			stringstream fbname_;
			fbname_ << fixed << setprecision(1) << intlumi/1000 << " fb^{-1} (13 TeV)";
			string fbname = fbname_.str();
			globalOpt->Get("lumi_text",fbname);
			TLatex width_test_lumi(0,0,fbname.c_str());
			width_test_lumi.SetTextSize(sizeP/pad1H);
			double umaxLumi = 1-marginR/pad1W;
			double uminLumi = umaxLumi - width_test_lumi.GetXsize();
			paveLumi = new TPaveText(uminLumi,posP,umaxLumi,1.0,"NDC");
			paveLumi->SetFillColor(0);
			paveLumi->SetBorderSize(0);
			paveLumi->SetTextFont(42);
			paveLumi->SetTextSize(sizeP/pad1H);
			paveLumi->AddText(fbname.c_str());
		}
		
		//drawing
		virtual void DrawHist(){
			pad1->cd();
			//get y axis range of histo from KLegend
			if(leg->UseRange()) histo->GetYaxis()->SetRangeUser(leg->GetRange().first,leg->GetRange().second);
			histo->Draw("hist");
			//horizontal error bars for histograms are DISABLED by default
			//but auto-enabled for variable-binned histograms (per CMS style guidelines)
			//(note: TExec cannot be the first thing drawn on a pad)
			string execname = "exec_" + name;
			if(globalOpt->Get("horizerrbars",false) || histo->GetXaxis()->IsVariableBinSize()){
				exec = new TExec(execname.c_str(),"gStyle->SetErrorX(0.5);");
			}
			else exec = new TExec(execname.c_str(),"gStyle->SetErrorX(0);");
			exec->Draw();
		}
		void DrawText(){
			pad1->cd();
			pad1->Update();
			
			//draw cut lines BEFORE legend/text
			vector<double> xcuts, ycuts;
			vector<Color_t> xcut_colors, ycut_colors;
			
			//x cuts, use pad y-range
			double y1 = pad1->GetLogy() ? pow(10,pad1->GetUymin()) : pad1->GetUymin();
			double y2 = pad1->GetLogy() ? pow(10,pad1->GetUymax()) : pad1->GetUymax();
			localOpt->Get("xcuts",xcuts);
			localOpt->Get("xcut_colors",xcut_colors);
			bool use_xcut_colors = (xcuts.size()==xcut_colors.size());
			if(!use_xcut_colors && xcut_colors.size()>0){
				cout << "Input error: in histo " << name << ", vector lengths of xcuts and xcut_colors do not match!";
				cout << " xcut_colors will be ignored." << endl;
			}
			for(int c = 0; c < xcuts.size(); c++){
				TLine* tmp = new TLine(xcuts[c],y1,xcuts[c],y2);
				tmp->SetLineStyle(7);
				tmp->SetLineWidth(2);
				if(use_xcut_colors) tmp->SetLineColor(xcut_colors[c]);
				else tmp->SetLineColor(kBlack);
				tmp->Draw("same");
				xcut_lines.push_back(tmp);
			}
			
			//y cuts, use pad x-range
			double x1 = pad1->GetLogx() ? pow(10,pad1->GetUxmin()) : pad1->GetUxmin();
			double x2 = pad1->GetLogx() ? pow(10,pad1->GetUxmax()) : pad1->GetUxmax();
			localOpt->Get("ycuts",ycuts);
			localOpt->Get("ycut_colors",ycut_colors);
			bool use_ycut_colors = (ycuts.size()==ycut_colors.size());
			if(!use_ycut_colors && ycut_colors.size()>0){
				cout << "Input error: in histo " << name << ", vector lengths of ycuts and ycut_colors do not match!";
				cout << " ycut_colors will be ignored." << endl;
			}
			for(int c = 0; c < ycuts.size(); c++){
				TLine* tmp = new TLine(x1,ycuts[c],x2,ycuts[c]);
				tmp->SetLineStyle(7);
				tmp->SetLineWidth(2);
				if(use_ycut_colors) tmp->SetLineColor(ycut_colors[c]);
				else tmp->SetLineColor(kBlack);
				tmp->Draw("same");
				ycut_lines.push_back(tmp);
			}
			
			if(leg) leg->Draw();
			paveCMS->Draw("same");
			paveExtra->Draw("same");
			paveLumi->Draw("same");
		}
		void DrawRatio(){
			pad2->cd();
			ratio->Draw("hist");
			exec->Draw();
		}
		void DrawLine(){
			pad2->cd();
			pad2->Update();
			
			//copy x cuts, use pad y-range
			double y1 = pad2->GetLogy() ? pow(10,pad2->GetUymin()) : pad2->GetUymin();
			double y2 = pad2->GetLogy() ? pow(10,pad2->GetUymax()) : pad2->GetUymax();
			for(int c = 0; c < xcut_lines.size(); c++){
				TLine* tmp = (TLine*)xcut_lines[c]->Clone();
				tmp->SetY1(y1);
				tmp->SetY2(y2);
				tmp->Draw("same");
				xcut_ratio_lines.push_back(tmp);
			}
			
			line->Draw("same");
		}

		//helpers
		void SetTitleOffset(TPad* pad, TAxis* axis){
			double padW, padH;
			pad->cd();
			if(pad==pad1) { padW = pad1W; padH = pad1H; }
			else if(pad==pad2) { padW = pad2W; padH = pad2H; }
			
			TLatex height_test(0,0,axis->GetTitle());
			height_test.SetTextSize(sizeT/padH);
			double Theight = height_test.GetYsize();
			double Toff = 1;
			
			//note: axis titles are middle-aligned
			if(strcmp(axis->GetName(),"xaxis")==0){
				Toff = (marginB/padH - epsilon/padH - Theight/2.)/(1.6*sizeT/padH);
			}
			else if(strcmp(axis->GetName(),"yaxis")==0){
				//need to scale title height value from pad height to pad width for y axis
				Theight *= padH/padW;
				Toff = (marginL/padW - epsilon/padW - Theight/2.)/(1.6*sizeT/padH);
			}
			else if(strcmp(axis->GetName(),"zaxis")==0){
				//need to scale title height value from pad height to pad width for z palette axis
				//(acts like y axis)
				Theight *= padH/padW;
				Toff = ((marginR-marginPal)/padW - epsilon/padW - Theight/2.)/(1.6*sizeT/padH);
			}
			
			axis->SetTitleOffset(Toff);
		}
		virtual void FormatHist(TPad* pad, TH1* hist){
			double padW, padH;
			double tickScaleX, tickScaleY;
			pad->cd();
			if(pad==pad1) {
				padW = pad1W; padH = pad1H;
				if(pad2) tickScaleY = (padH - marginM1 - marginT)/padH*padW;
				else tickScaleY = (padH - marginB - marginT)/padH*padW;
			}
			else if(pad==pad2) { 
				padW = pad2W; padH = pad2H;
				tickScaleY = (padH - marginB - marginM2)/padH*padW;
			}
			tickScaleX = (padW - marginL - marginR)/padW*padH;

			hist->GetYaxis()->SetTitleSize(sizeT/padH);
			hist->GetYaxis()->SetLabelSize(sizeL/padH);
			hist->GetYaxis()->SetLabelOffset(sizeLoff/padW);
			hist->GetYaxis()->SetTickLength(sizeTick/tickScaleY);
			hist->GetXaxis()->SetTitleSize(sizeT/padH);
			hist->GetXaxis()->SetLabelSize(sizeL/padH);
			hist->GetXaxis()->SetLabelOffset(sizeLoff/padH);
			hist->GetXaxis()->SetTickLength(sizeTick/tickScaleX);
			hist->GetXaxis()->SetNdivisions(NdivX);
			if(hist==ratio) hist->GetYaxis()->SetNdivisions(NdivYratio);
			else if(hist==histo) hist->GetYaxis()->SetNdivisions(NdivYhisto);
			
			//format z axis just in case
			hist->GetZaxis()->SetTitleSize(sizeT/padH);
			hist->GetZaxis()->SetLabelSize(sizeL/padH);
			hist->GetZaxis()->SetLabelOffset(sizeLoff/padW);
			hist->GetZaxis()->SetTickLength(sizeTick/tickScaleY);
		}
		
		//accessors
		string GetName() { return name; }
		virtual string GetNameX() { return name; }
		virtual string GetNameY() { return ""; }
		bool IsInit() { return isInit; }
		void SetName(string name_) { name = name_; }
		TH1* GetHisto() { return histo; }
		TH1* GetRatio() { return ratio; }
		TCanvas* GetCanvas() { return can; }
		TPad* GetPad1() { return pad1; }
		TPad* GetPad2() { return pad2; }
		KLegend* GetLegend() { return leg; }
		void SetLegend(KLegend* leg_) { leg = leg_; }
		TPaveText* GetCMSText() { return paveCMS; }
		TPaveText* GetExtraText() { return paveExtra; }
		TPaveText* GetLumiText() { return paveLumi; }
		OptionMap* GetLocalOpt() { return localOpt; }
		void SetLocalOpt(OptionMap* opt) { localOpt = opt; if(localOpt==0) localOpt = new OptionMap(); } //must always have an option map
		OptionMap* GetGlobalOpt() { return globalOpt; }
		void SetGlobalOpt(OptionMap* opt) { globalOpt = opt; if(globalOpt==0) globalOpt = new OptionMap(); } //must always have an option map

	protected:
		//member variables
		string name;
		OptionMap* localOpt;
		OptionMap* globalOpt;
		TH1 *histo, *ratio;
		TExec *exec;
		bool isInit;
		TCanvas *can;
		TPad *pad1, *pad2;
		KLegend* leg;
		TPaveText* paveCMS;
		TPaveText* paveExtra;
		TPaveText* paveLumi;
		TLine* line;
		vector<TLine*> xcut_lines, ycut_lines, xcut_ratio_lines;
		double canvasW, canvasH, canvasWextra, canvasHextra, ratioH;
		double marginL, marginR, marginB, marginT, marginM1, marginM2, marginPal;
		double sizeT, sizeL, sizeP, sizeTick, sizeLoff, epsilon;
		double NdivX, NdivYhisto, NdivYratio;
		double pad1W, pad1H, pad2W, pad2H;
};

//-----------------------------------------------------------
//extension of KPlot for 2D histograms
//drawn with colz option -> one canvas for each set
class KPlot2D: public KPlot {
	public:
		//constructor
		KPlot2D() : KPlot(), setname("") {}
		KPlot2D(string name_, string setname_, OptionMap* localOpt_, OptionMap* globalOpt_) : KPlot(name_,localOpt_,globalOpt_), setname(setname_) {
			SetStyle();
		}
		//initialization
		void SetStyle(){
			//2D changes
			//extra space for z axis palette
			//palette width calc from THistPainter::PaintPalette(): mPal = 0.045*padW
			canvasW = 1./0.95*(canvasW + marginL - marginR);
			marginPal = 0.05*canvasW;
			marginR = marginL + marginPal;
		}
		virtual void CreateHist(){
			//construct histogram		
			vector<double> xbins, ybins;
			int xnum, ynum;
			double xmin, xmax, ymin, ymax;
			if(localOpt->Get("xbins",xbins)){ //variable x-binning case
				if(localOpt->Get("ybins",ybins)) { //variable y-binning case
					histo = new TH2F(name.c_str(),"",xbins.size()-1,&xbins[0],ybins.size()-1,&ybins[0]);	
					isInit = true;
				}
				else if(localOpt->Get("ynum",ynum) && localOpt->Get("ymin",ymin) && localOpt->Get("ymax",ymax)){ //standard y-binning case
					histo = new TH2F(name.c_str(),"",xbins.size()-1,&xbins[0],ynum,ymin,ymax);
					isInit = true;
				}
				else { //no/incomplete binning information, build failed
					isInit = false;
					return;
				}
			}
			else if(localOpt->Get("xnum",xnum) && localOpt->Get("xmin",xmin) && localOpt->Get("xmax",xmax)){ //standard x-binning case
				if(localOpt->Get("ybins",ybins)) { //variable y-binning case
					histo = new TH2F(name.c_str(),"",xnum,xmin,xmax,ybins.size()-1,&ybins[0]);	
					isInit = true;
				}
				else if(localOpt->Get("ynum",ynum) && localOpt->Get("ymin",ymin) && localOpt->Get("ymax",ymax)){ //standard y-binning case
					histo = new TH2F(name.c_str(),"",xnum,xmin,xmax,ynum,ymin,ymax);
					isInit = true;
				}
				else { //no/incomplete binning information, build failed
					isInit = false;
					return;
				}
			}
			else { //no/incomplete binning information, build failed
				isInit = false;
				return;
			}
			string xtitle, ytitle, ztitle;
			localOpt->Get("xtitle",xtitle);
			localOpt->Get("ytitle",ytitle);
			localOpt->Get("ztitle",ztitle);
			histo->GetXaxis()->SetTitle(xtitle.c_str());
			histo->GetYaxis()->SetTitle(ytitle.c_str());
			//include name of set in z title
			if(setname=="ratio"){
				string rationame2D = "";
				globalOpt->Get("rationame2D",rationame2D); //set in KManager
				histo->GetZaxis()->SetTitle(rationame2D.c_str());
			}
			else { //include name of set in z title
				histo->GetZaxis()->SetTitle((setname + ": " + ztitle).c_str());
			}
		}
		virtual bool Initialize(TH1* histo_=NULL){
			if(isInit) return isInit;
			
			histo = histo_;
			if(!histo) CreateHist();
			if(!histo) return isInit; //histo creation failed
			
			string cname = name;
			cname = cname + "_" + setname;
			can = new TCanvas(cname.c_str(),cname.c_str(),canvasW+canvasWextra,canvasH+canvasHextra);
		
			pad1 = new TPad("graph","",0,0,1,1);
			pad1W = pad1->GetWw()*pad1->GetAbsWNDC();
			pad1H = pad1->GetWh()*pad1->GetAbsHNDC();
			pad1->SetMargin(marginL/pad1W,marginR/pad1W,marginB/pad1H,marginT/pad1H);
			pad1->SetTicks(1,1);
			if(localOpt->Get("logz",true) && setname!="ratio") pad1->SetLogz(); //logz on by default (i.e. linz off by default); except for ratio, which never has logz
			if(localOpt->Get("logy",false)) pad1->SetLogy(); //logy off by default (i.e. liny on by default)
			if(localOpt->Get("logx",false)) pad1->SetLogx(); //logx off by default (i.e. linx on by default)
			pad1->Draw();

			FormatHist(pad1,histo);
			SetTitleOffset(pad1,histo->GetXaxis());
			SetTitleOffset(pad1,histo->GetYaxis());
			SetTitleOffset(pad1,histo->GetZaxis());
			
			InitializePaves();
			
			return isInit;
		}
		//drawing
		void DrawHist(){
			pad1->cd();
			histo->Draw("colz");
		}
		
		//accessors
		string GetSetName() { return setname; }
		
	protected:
		//member variables
		string setname;
};

#endif
