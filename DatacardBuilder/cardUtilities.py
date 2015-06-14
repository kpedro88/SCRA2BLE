from ROOT import *

import math
import sys
import re

# clones bins 1-18 to other bins
def hutil_clone0BtoNB(h_in,useFactors=True):

	translations = [
					['NJets0_BTags1',0.2470],
					['NJets0_BTags2',0.0479],
					['NJets0_BTags3',0.0045],
					['NJets1_BTags1',0.3955],
					['NJets1_BTags2',0.1326],
					['NJets1_BTags3',0.0238],
					['NJets2_BTags1',0.5083],
					['NJets2_BTags2',0.2269],
					['NJets2_BTags3',0.0569]
				   ]

	h_new = h_in.Clone();

	for i in range(h_new.GetNbinsX()):
		binlabel = h_new.GetXaxis().GetBinLabel(i+1);
		
		ref_binlabel = None;
		for trans in translations: 
			if trans[0] in binlabel:
				ref_binlabel = re.sub("BTags.","BTags0",binlabel)
				newBinContent = -99;
				if useFactors: newBinContent = getBinContentByLabel( h_in, ref_binlabel ) * trans[1];
				else: newBinContent = getBinContentByLabel( h_in, ref_binlabel );
				h_new.SetBinContent(i+1,newBinContent);

				# print binlabel,ref_binlabel;
				# print i, binlabel, ref_binlabel, h_in.GetBinContent(i+1) , " " , getBinContentByLabel( h_in, ref_binlabel ) ," ", newBinContent, " ", trans[1];

	return h_new;

def hutil_PhotonRatioFix(h_gjet,h_zvv):

	hout_gjet = h_gjet.Clone();
	hout_zvv = h_zvv.Clone();

	for i in range(h_gjet.GetNbinsX()):
		if h_gjet.GetBinContent(i+1) < 1: 
			hout_gjet.SetBinContent( i+1, 1. );
			hout_zvv.SetBinContent( i+1, h_zvv.GetBinContent(i+1) );
		else: 
			hout_gjet.SetBinContent( i+1, h_gjet.GetBinContent(i+1) );
			hout_zvv.SetBinContent( i+1, h_gjet.GetBinContent(i+1)*h_zvv.GetBinContent(i+1) );

	return [hout_gjet,hout_zvv];


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

def getBinContentByLabel(h_in,label):

	binContent = -99;
	for i in range(h_in.GetNbinsX()):
		binlabel = h_in.GetXaxis().GetBinLabel(i+1);
		if binlabel == label: 
			binContent = h_in.GetBinContent(i+1);
			break;
	return binContent;


def binsToList(h_in):

	olist = [];
	for i in range(h_in.GetNbinsX()): olist.append( h_in.GetBinContent(i+1) );
	return olist;

def binLabelsToList(h_in):

	olist = [];
	for i in range(h_in.GetNbinsX()): olist.append( h_in.GetXaxis().GetBinLabel(i+1) );
	return olist;

def textToList(fn,column):

	olist = [];
	f = open(fn,'r');
	for line in f:
		olist.append( float(line.strip().split()[column]) );
	return olist;



