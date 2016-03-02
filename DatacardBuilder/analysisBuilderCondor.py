from ROOT import *
import os
import math
import sys
from array import array
from searchRegion import *
from singleBin import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--signal", dest="signal", default = 'SMSqqqq',help="mass of LSP", metavar="signal")
parser.add_option("--tag", dest="tag", default = 'SinglePhoton1',help="mass of LSP", metavar="tag")
parser.add_option("--mGo", dest="mGo", default='1000', help="Mass of Gluino", metavar="mGo")
parser.add_option("--mLSP", dest="mLSP", default='900', help="Mass of LSP", metavar="mLSP")
parser.add_option('--fastsim', action='store_true', dest='fastsim', default=False, help='use fastsim signal')
parser.add_option('--realData', action='store_true', dest='realData', default=False, help='use real data')
parser.add_option("--eos", dest="eos", default = "",help="EOS directory prefix", metavar="eos")

(options, args) = parser.parse_args()


#########################################################################################################
def getFittedMu(fn):
    
    output = [];

    tf = TFile(fn);
    tt = tf.Get("limit")
    tt.GetEntry(0);
    output.append( tt.limit );
    tt.GetEntry(1);
    output.append( tt.limit );
    tt.GetEntry(2);
    output.append( tt.limit );

    print output
    return output

def getLimit(fn):
    limits = []
    tf = TFile(fn);
    tt = tf.Get("limit")
    for i in range(6):
        tt.GetEntry(i);
        limits.append(tt.limit);
        if i is 5: limits.append(tt.limitErr)
    output = limits
    return output

def getSignif(fn):
    
    tf = TFile(fn);
    tt = tf.Get("limit")
    tt.GetEntry(0);

    print "[getSignif], ", tt.limit
    return tt.limit;

#########################################################################################################
if __name__ == '__main__':
    

    signalmodel=options.signal+options.mGo
    signals = [signalmodel]
    mus=[0.0]
    lumis = [2.262];

    #variations = ['qcdOnly','zvvOnly','llpOnly','tauOnly']
    #variations = ['allNotau','llpOnly', 'tauOnly']
    # variations = ['allBkgs','allNoqcd','allNozvv','allNollp','allNotau']
    #variations=['allNoqcd','allNozvv','allNollp','allNotau']
    #variations = ['zvvOnly' ]
    #variations = ['allBkgs','tauOnly','llpOnly']
    #variations=['allNozvv']
    # variations=['onlyLep']
    #variations=['tauOnly']
    variations=['allBkgs']

    job_postfix = "%s_%s_%s" % (options.signal,options.mGo,options.mLSP);
    fout = TFile("results_%s.root" % (job_postfix), "RECREATE");
    tout = TTree("results","results");
    # identifier    = array( 'c', [ 'c' ] );
    mGo          = array( 'f', [ 0. ] ); 
    mLSP         = array( 'f', [ 0. ] ); 
    limit_exp        = array( 'f', [ 0. ] );
    limit_p1s        = array( 'f', [ 0. ] );
    limit_p2s        = array( 'f', [ 0. ] );
    limit_m1s        = array( 'f', [ 0. ] );
    limit_m2s        = array( 'f', [ 0. ] );
    limit_obs        = array( 'f', [ 0. ] );
    limit_obsErr        = array( 'f', [ 0. ] );
    significance = array( 'f', [ 0. ] );  
    fittedMu     = array( 'f', [ 0. ] );
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

    for lumi in lumis: 
        print "=========>>> LUMI is ", lumi
        for sig in signals:
            for mu in mus:
                for vary in variations: 
                    tag = options.tag;
                    combOpt = '';
                    if vary == 'allBkgs':  combOpt = '--allBkgs'
                    if vary == 'qcdOnly':  combOpt = '--qcdOnly'
                    if vary == 'zvvOnly':  combOpt = '--zvvOnly'
                    if vary == 'llpOnly':  combOpt = '--llpOnly'
                    if vary == 'tauOnly':  combOpt = '--tauOnly'
                    if vary == 'allNoqcd': combOpt = '--tauOnly --zvvOnly --llpOnly'
                    if vary == 'allNozvv': combOpt = '--tauOnly --qcdOnly --llpOnly'
                    if vary == 'allNollp': combOpt = '--tauOnly --zvvOnly --qcdOnly'
                    if vary == 'allNotau': combOpt = '--qcdOnly --zvvOnly --llpOnly'
                    if vary == 'allNolep': combOpt = '--qcdOnly --zvvOnly'
                    if vary == 'onlyLep':  combOpt = '--tauOnly --llpOnly'

                    command = 'python buildCards-AllBkgsMassScan.py -b %s --signal %s --tag %s --lumi %0.1f --mu %0.1f --mGo=%s --mLSP=%s' % (combOpt,options.signal,tag,lumi,mu, options.mGo, options.mLSP); 
                    if options.fastsim: command += " --fastsim"
                    if options.realData: command += " --realData"
                    if len(options.eos)>0: command += " --eos %s" % (options.eos)
                    os.system(command);
                    
                    signaltag = "SMS%s%s" % (options.signal[2:],options.mGo);
                    if options.fastsim: signaltag = "%s_%s_%s" % (options.signal, options.mGo, options.mLSP);

                    the_odir = 'testCards-%s-%s-%1.1f-mu%0.1f' % (tag,signaltag,lumi,mu);
                    if options.fastsim: the_odir = 'testCards-%s-%s_%s_%s-%1.1f-mu%0.1f' % (tag,options.signal,options.mGo, options.mLSP, lumi,mu);
                    allcardnames = os.listdir(the_odir);
                    command = 'combineCards.py';
                    for cn in allcardnames:
                        if 'card_' in cn: command += " " + the_odir+'/'+cn;
                    command += " > "+the_odir+'/allcards.txt'
                    os.system(command);
                    combine_cmmd = "text2workspace.py %s/allcards.txt -o %s/allcards.root" % (the_odir,the_odir);
                    os.system(combine_cmmd);
                    
                    # run significance
                    # combine_cmmd = "combine -M ProfileLikelihood --signif %s/allcards.root -n %s" % (the_odir,the_odir); 
                    # os.system(combine_cmmd);
                    # # run max likelihood fit
                    #combine_cmmd = "combine -M MaxLikelihoodFit %s/allcards.root -n %s --saveWithUncertainties --saveNormalizations " % (the_odir,the_odir); 
                    #print combine_cmmd;
                    #os.system(combine_cmmd);
                    # run asymptotic
                    combine_cmmd = "combine -M Asymptotic %s/allcards.root -n %s" % (the_odir,the_odir); 
                    os.system(combine_cmmd);

                    dicttag = "%s_%s_%.1f" % (tag,sig,lumi);

                    identifier = dicttag;
                    mGo[0] = float(options.mGo);
                    mLSP[0] = float(options.mLSP);
                    #fittedMu[0] = getFittedMu( "higgsCombinetestCards-%s-%s-%0.1f-mu%0.1f.MaxLikelihoodFit.mH120.root" % (tag,signaltag,lumi,mu) )[0];
                    #significance[0]=getSignif( "higgsCombinetestCards-%s-%s-%0.1f-mu%0.1f.ProfileLikelihood.mH120.root" % (tag,signaltag,lumi,mu) ) ;
                    olims = getLimit( "higgsCombine%s.Asymptotic.mH120.root" % (the_odir));
                    limit_m2s[0] = olims[0];
                    limit_m1s[0] = olims[1];
                    limit_exp[0] = olims[2];
                    limit_p1s[0] = olims[3];
                    limit_p2s[0] = olims[4];
                    limit_obs[0] = olims[5];
                    limit_obsErr[0]= olims[6]    
                    # fittedMu[0] = -99.;
                    #significance[0] = -99.;
                    # limit[0] = -99.;
                    
                    tout.Fill();
    fout.cd();
    tout.Write();
    fout.Close();







