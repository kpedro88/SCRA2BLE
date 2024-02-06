from ROOT import *

#*AR-180418:Recipe:
#For given signal and given mass point(mGluino, mLSP), this code generates datacard for all 174 bins, which lists expected signal and various backgrounds along with their uncertainty. Then runs code combineCards.py to combine cards from 174 bins into single card allcards.txt. Then evaluates limit using allcards.txt and save into output root file. 




#*AR-180418:The os and sys modules provide numerous tools to deal with filenames, paths, directories. The os module contains two sub-modules os.sys (same as sys) and os.path that are dedicated to the system and directories; respectively.

#*AR-180426:Import in python is similar to #include header_file in C/C++.
#*AR-180426:When import is used, it searches for the module initially in the local scope by calling __import__() function. The value returned by the function are then reflected in the output of the initial code.
#import math
#print(math.pi)
#In the above code module math is imported, and its variables can be accessed by considering it to be a class and pi as its object.pi as whole can be imported into our intial code, rather than importing the whole module.
#from math import pi, print(pi)
import os
import math
import sys
from array import array
from searchRegion import *
from singleBin import *

#*AR-180418:source code:Lib/optparse.py. As it parses the command line, optparse sets attributes of the options object returned by parse_args() based on user-supplied command-line values. When parse_args() returns from parsing this command line,options.signal will be "SMSqqqq", options.fastsim will be "false" in default case.
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--signal", dest="signal", default = 'SMSqqqq',help="mass of LSP", metavar="signal")
parser.add_option("--mGo", dest="mGo", default='1000', help="Mass of Gluino", metavar="mGo")
parser.add_option("--mLSP", dest="mLSP", default='900', help="Mass of LSP", metavar="mLSP")
parser.add_option('--fastsim', action='store_true', dest='fastsim', default=False, help='use fastsim signal')
parser.add_option('--realData', action='store_true', dest='realData', default=False, help='use real data')
parser.add_option("--eos", dest="eos", default = "root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV17_v1/",help="EOS directory prefix", metavar="eos")
parser.add_option("--CombOpt", dest="CombOpt", default="AsymptoticUL", help="Combine option for the code: AsymptoticUL, MaxLiklihood, Significance, FitCovariance, ImpactsInitialFit",metavar="CombOpt")
(options, args) = parser.parse_args()


#########################################################################################################


#AR-180418:getFittedMu function is not used anywhere in the code
def getFittedMu(fn):
#AR-180418:variable = [].Now variable refers to an empty list*.*The default built-in Python type is called a list, not an array. It is an ordered container of arbitrary length that can hold a heterogenous collection of objects (their types do not matter and can be freely mixed). This should not be confused with the array module, which offers a type closer to the C array type; the contents must be homogenous (all of the same type), but the length is still dynamic.Ex. intarray = array('i')		output = [];
	output = [];

	tf = TFile(fn);
	tt = tf.Get("limit")
	tt.GetEntry(0);
	output.append( tt.limit );
	tt.GetEntry(1);
	output.append( output[0]-tt.limit );
	tt.GetEntry(2);
	output.append( tt.limit-output[0] );

	print "[output] ",output
	return output

def getLimit(fn):
	limits = []
	tf = TFile(fn); #AR-180418:Ex. file "higgsCombinetestCards-allBkgs-T1tttt_1500_100-35.9-mu0.0.Asymptotic.mH120.root"
	tt = tf.Get("limit") ;#AR-180418:generates a list of 6 values, the legal indices for items of a sequence of length 6.
	for i in range(6):
		tt.GetEntry(i);#AR-180418:Read all branches of entry and return total number of bytes read
		limits.append(tt.limit);
		if i is 5: limits.append(tt.limitErr)
	output = limits
	return output

#AR-180418:getSignif function is not used anywhere in the code
def getSignif(fn):

	tf = TFile(fn);
	tt = tf.Get("limit")
	tt.GetEntry(0);

	print "[getSignif], ", tt.limit
	return tt.limit;

#########################################################################################################
if __name__ == '__main__':

#AR-180418:In default case, options.signal=SMSqqqq, options.mGo=1000. Therefore, "options.signal+options.mGo" will be SMSqqqq1000.
	signalmodel=options.signal+options.mGo
	signals = [signalmodel]
	mus=[0.0]
	#lumis = [35.9];
	lumis = [137.4];
	#os.system("python SignalMergePeriods.py --signal=%s --mGo=%s --mLSP=%s" %(options.signal, options.mGo,options.mLSP))

	# identifier	= array( 'c', [ 'c' ] );
	#AR-180418:create an array with data type float and value list specified in its arguments
	mGo  = array( 'f', [ 0. ] );
	mLSP = array( 'f', [ 0. ] );
	limit_exp = array( 'f', [ 0. ] );
	limit_p1s = array( 'f', [ 0. ] );
	limit_p2s = array( 'f', [ 0. ] );
	limit_m1s = array( 'f', [ 0. ] );
	limit_m2s = array( 'f', [ 0. ] );
	limit_obs = array( 'f', [ 0. ] );
	limit_obsErr = array( 'f', [ 0. ] );
	significance = array( 'f', [ 0. ] );
	fittedMu = array( 'f', [ 0. ] );
	fittedMuErrPlus = array( 'f', [ 0. ] );
	fittedMuErrMinus = array( 'f', [ 0. ] );
#AR-180418:first for loop
	for lumi in lumis: #AR-180418:lumis array has only one element, 35.86

		print "=========>>> LUMI is ", lumi
#AR-180418:second for loop
		for sig in signals:#AR-180418:signals defined by their name and gluino mass. How can we input an array of signals here?
			print "sig: ", sig
#AR-180418:third for loop
			#for mu in mus:#AR-180418:What this loop over mus mean?
			job_postfix = "%s_%s_%s" % (options.signal,options.mGo,options.mLSP);
#AR-180418: Creates output file results_SMSqqqq_1000_900_mu0.0 in default case
			fout = TFile("results_%s.root" %job_postfix, "RECREATE");
			print "Creates results file "
			tout = TTree("results","results");
#AR-180418: create the branches and assign the fill-variables to them
			tout.Branch('mGo',mGo,'mGo/F');
			tout.Branch('mLSP',mLSP,'mLSP/F');
			tout.Branch("limit_exp",limit_exp,"limit_exp/F");
			tout.Branch("limit_p1s",limit_p1s,"limit_p1s/F");
			tout.Branch("limit_p2s",limit_p2s,"limit_p2s/F");
			tout.Branch("limit_m1s",limit_m1s,"limit_m1s/F");
			tout.Branch("limit_m2s",limit_m2s,"limit_m2s/F");
			tout.Branch("limit_obs",limit_obs,"limit_obs/F");
			tout.Branch("limit_obsErr",limit_obsErr,"limit_obsErr/F");
			tout.Branch("significance",significance,"significance/F");
			tout.Branch("fittedMu",fittedMu,"fittedMu/F");
			tout.Branch("fittedMuErrPlus",fittedMuErrPlus,"fittedMuErrPlus/F");
			tout.Branch("fittedMuErrMinus",fittedMuErrMinus,"fittedMuErrMinus/F");
			print "Now build cards"
			#AR-180418:python script buildCards-AllBkgsMassScan.py runs for every combination of [lumi,signal] combination
			#command = 'python buildCards-AllBkgsMassScan.py %s --signal %s --tag %s --lumi %0.1f --mu %0.1f --mGo=%s --mLSP=%s' % (combOpt,options.signal,vary,lumi,mu, options.mGo, options.mLSP); 
			command = 'python buildCards-AllBkgsMassScan.py --signal %s  --lumi %0.1f  --mGo=%s --mLSP=%s --sigDir %s' % (options.signal,lumi, options.mGo, options.mLSP,options.eos); 
			if options.fastsim: command += " --fastsim"
			if options.realData: command += " --realData"
			#if len(options.eos)>0: command += " --eos %s" % (options.eos)
			print command
			os.system(command); #AR-180418: We can execute system command by using os.system() function.
			print "buildCards-AllBkgsMassScan.py has run "
			#AR-180418:options.signal can be an array of signals with different signal name and gluino masses
			#AR-180418:signaltag is different if FastSim is true or not
			signaltag = "SMS%s%s" % (options.signal[2:],options.mGo);
			if options.fastsim: signaltag = "%s_%s_%s" % (options.signal, options.mGo, options.mLSP);
			#AR-180418:the_odir is different if FastSim is true or not
			the_odir = 'testCards-Moriond-%s-%1.1f' % (signaltag,lumi);
			if options.fastsim: the_odir = 'testCards-Moriond-%s_%s_%s-%1.1f' % (options.signal,options.mGo, options.mLSP, lumi);
			#AR-180418:Lists all cards in output directory the_odir
			allcardnames = os.listdir(the_odir);
			#AR-180427:combineCards.py file is located at /uscms_data/d3/arane/work/RA2bInterpretation/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/scripts. Where is location of file mentioned?
			#print "list cards" , allcardnames
			command = "combineCards.py ";
			#for cn in allcardnames
			for i in range(0,174):
				cn="card_signal%d.txt" %i
				command += " " + the_odir+'/'+cn;
				command += " > "+the_odir+'/allcards.txt'
			#AR-180418: executes combineCards.py
			os.system(command);
			print "combinecards command has run "
			combine_cmmd = "text2workspace.py --X-allow-no-signal --X-allow-no-background %s/allcards.txt -o %s/allcards.root" %(the_odir,the_odir);
			os.system(combine_cmmd);
			#options for combine code:
			if options.CombOpt=="AsymptoticUL":
				print " run asymptotic limit "
				#AR-180418: executes limit
				combine_cmmd = "combine -M Asymptotic %s/allcards.root -n %s" % (the_odir,the_odir);
			elif options.CombOpt=="MaxLiklihood":
				print " run Maxliklihood for post-fit yields"
				combine_cmmd = "combine -M FitDiagnostics %s/allcards.root -n %s --saveWithUncertainties --saveNormalizations --expectSignal=0" %(the_odir,the_odir);
			elif options.CombOpt=="FitCovariance":
				print " run Maxliklihood for pre-fit covariance matrix"
				combine_cmmd = "combine -M FitDiagnostics -n %s --saveWithUncertainties --saveNormalizations --saveShapes --numToysForShape=2000 --saveOverallShapes %s/allcards.root --preFitValue=0 " % (the_odir,the_odir);  
			elif options.CombOpt=="Significance":
				print "run Obs. significance"
				combine_cmmd=" combine  -M ProfileLikelihood  --uncapped 1 --significance --rMin -5 %s/allcards.root -n %s " %(the_odir,the_odir);
			elif options.CombOpt=="ImpactsInitialFit":
				#combine_cmmd = "combineTool.py -M Impacts -m 125  --doInitialFit --robustFit 1  -t -1 --expectSignal  0  --toysFrequentist -d %s/allcards.root -n %s --rMin=-5 --rMax=5" %(TotalPath,the_odir);		
				combine_cmmd = "combineTool.py -M Impacts -m 125  --doInitialFit --robustFit 1  -t -1 --expectSignal  0  --toysFrequentist -d %s/allcards.root --rMin=-5 --rMax=5" %(the_odir);		
			else: print "Not a combine option!!!!! "
			os.system(combine_cmmd);
			dicttag = "%s_%.1f" % (sig,lumi);

			identifier = dicttag;
			mGo[0] = float(options.mGo);
			mLSP[0] = float(options.mLSP);
			#####Dummy values
			limit_m2s[0] = -99.;
			limit_m1s[0] = -99.;
			limit_exp[0] = -99.;
			limit_p1s[0] = -99.;
			limit_p2s[0] = -99.;
			limit_obs[0] = -99.;
			limit_obsErr[0]= -99.
			fittedMu[0] = -99.;
			significance[0] = -99.;
			if options.CombOpt=="AsymptoticUL":
				olims = getLimit( "higgsCombine%s.Asymptotic.mH120.root" % (the_odir));
				limit_m2s[0] = olims[0];
				limit_m1s[0] = olims[1];
				limit_exp[0] = olims[2];
				limit_p1s[0] = olims[3];
				limit_p2s[0] = olims[4];
				limit_obs[0] = olims[5];
				limit_obsErr[0]= olims[6]
			elif options.CombOpt=="MaxLiklihood" or options.CombOpt=="FitCovariance":
				fittedMu[0] = getFittedMu( "higgsCombine%s.FitDiagnostics.mH120.root" %(the_odir) )[0];
				fittedMuErrMinus[0] = getFittedMu( "higgsCombine%s.FitDiagnostics.mH120.root" %(the_odir) )[1];
				fittedMuErrPlus[0] = getFittedMu( "higgsCombine%s.FitDiagnostics.mH120.root" %(the_odir) )[2];
				fitDiag=TFile("fitDiagnostics%s.root" %the_odir)
				keys=fitDiag.GetListOfKeys()
				for name in keys:fout.WriteObject(fitDiag.Get(name.GetName()),name.GetName())
			elif options.CombOpt=="Significance":
				significance[0]=getSignif( "higgsCombine%s.ProfileLikelihood.mH120.root" % (the_odir) ) ;
			tout.Fill();
			fout.cd();
#AR-180418:results tree is written
			tout.Write();
			fout.Close();
