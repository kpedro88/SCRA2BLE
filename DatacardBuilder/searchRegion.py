import sys
import re
import collections
from singleBin import *
from math import log,exp,sqrt
#import pprint
from heapq import nlargest
from collections import OrderedDict

class searchRegion:

    def __init__( self ,name, binLabels, singleBinTags ) :

        self._regionName = name;
        self._binLabels = binLabels;
        self._singleBinTags = singleBinTags;

        self._nBins = len(singleBinTags);
        self._singleBins = [];
        for i in range(self._nBins):
            # print i, self._binLabels[i]
            self._singleBins.append( singleBin(self._regionName + str(i), self._singleBinTags[i], self._binLabels[i], i ) );

        # print "nbins = ", self._nBins;

    def fillRates(self, rateinputs, normalize=False):

        # if len(histograms) != len(self._binLabels): 
        #     raise Exception("There is a mismatch in histogram input")

        for i in range(self._nBins):
            self._singleBins[i].setRates( rateinputs[i], normalize );
            if len(rateinputs[i]) != len(self._binLabels[i]):
                print  len(rateinputs[i]),len(self._binLabels[i])
                raise Exception("There is a mismatch in this bin of this signal region between rates and n contributions");

        
    def addSingleSystematic(self,sysname,systype,channel,val,identifier='',index=None):
        
        #print "Looking for ",identifier;

        for i in range(self._nBins): 
            #if identifier in self._singleBins[i]._tag:
            if re.search(identifier, self._singleBins[i]._tag) or identifier == '':
                #print "Found! ",self._singleBins[i]._tag;
                if index == None or index == self._singleBins[i]._index:
                    #print identifier, " in ", self._singleBins[i]._tag;                
                    if isinstance(val,collections.Iterable): 
                        self._singleBins[i].addSystematic( sysname, systype, channel, val[i] );
                    else: 
                        self._singleBins[i].addSystematic( sysname, systype, channel, val );

    def addAsymSystematic(self,sysname,systype,channel,valup,valdown,identifier='',index=None):
            #print "Looking for ",identifier;
            for i in range(self._nBins):
                #if identifier in self._singleBins[i]._tag:
                if re.search(identifier, self._singleBins[i]._tag) or identifier == '':
                    #print "Found! ",self._singleBins[i]._tag;
                    if index == None or index == self._singleBins[i]._index:
                        if isinstance(valup,collections.Iterable) and isinstance(valdown,collections.Iterable):
                            self._singleBins[i].addAsymSystematic( sysname, systype, channel, valup[i],valdown[i] );
                        else: 
                            self._singleBins[i].addAsymSystematic( sysname, systype, channel, valup,valdown );

    def addCorrelSystematic(self,sysname,systype,channel,val1,val2,identifier='',index=None):    
            for i in range(self._nBins):
                    #if identifier in self._singleBins[i]._tag:
                    if re.search(identifier, self._singleBins[i]._tag) or identifier == '':
                            #print "Found! ",self._singleBins[i]._tag;
                            if index == None or index == self._singleBins[i]._index:
                                            self._singleBins[i].addCorrelSystematic( sysname, systype, channel, val1,val2 );
    def addCorrelSystematicAsym(self,sysname,systype,channel,val1up, val1down, val2up, val2down, identifier='',index=None):
            for i in range(self._nBins):
                    #if identifier in self._singleBins[i]._tag:
                    if re.search(identifier, self._singleBins[i]._tag) or identifier == '':
                            #print "Found! ",self._singleBins[i]._tag;
                            if index == None or index == self._singleBins[i]._index:
                                if isinstance(val1up,collections.Iterable) and isinstance(val1down,collections.Iterable):
                                     self._singleBins[i].addCorrelSystematicAsym( sysname, systype, channel, val1up[i],val1down[i],val2up[i], val2down[i] );
                                else:
                                     self._singleBins[i].addCorrelSystematicAsym( sysname, systype, channel, val1up,val1down,val2up, val2down );
    def addSystematicFromList(self,sysname,systype,channel,inputlist):

        if len(inputlist) != self._nBins: print "There is a problem mistaching in searchRegion:addSystematicFromList!!";
        for i in range(self._nBins): 
            if(inputlist[i]>-99):self._singleBins[i].addSystematic( sysname, systype, channel, 1+inputlist[i] );
            else: self._singleBins[i].addSystematic( sysname, systype, channel, 1 );
    def addAsymSystematicFromList(self,sysname,systype,channel,inputListUp,inputListDn):

        if len(inputListUp) != self._nBins: print "There is a problem mistaching in searchRegion:addSystematicFromList!!";
        for i in range(self._nBins): 
            #print inputListUp[i]
            #if(inputlistUp[i]>-99 and inputlistDn[i]>-99):
            self._singleBins[i].addAsymSystematic( sysname, systype, channel, 1+inputListUp[i], 1-inputListDn[i] );

        
    def setObservedManually(self,listObs):
        for i in range(self._nBins):
            self._singleBins[i]._observed = listObs[i];

    def writeRates(self):
        for i in range(self._nBins):
            self._singleBins[i].writeRates();

    def writeCards(self, odir):
        for i in range(self._nBins):
        # for i in range(4,18):
            # if i!=3 and i!=2: self._singleBins[i].writeCard( odir ); 
            self._singleBins[i].writeCard( odir ); 

    def GetNbins(self):
        return self._nBins;
        
    def systRange(self, odir, method):
        syst_minmax = OrderedDict()
        norm_Q = -1
        
        # find top ten bins for method 1
        all_Q = []
        for ibin in self._singleBins:
            # calculate bin sensitivity Q
            bkg_tot = sum(ibin._rates[1:])
            sig_tot = ibin._rates[0]
            Q = 2*(sqrt(sig_tot + bkg_tot) - sqrt(bkg_tot))
            all_Q.append(Q)
        topten = nlargest(10,all_Q)
        minten = min(topten)
        
        for ibin in self._singleBins:
            # calculate bin sensitivity Q
            bkg_tot = sum(ibin._rates[1:])
            sig_tot = ibin._rates[0]
            Q = 2*(sqrt(sig_tot + bkg_tot) - sqrt(bkg_tot))
            if method==0: Q = 1.0
            elif method==1:
                if Q < minten: continue
                else: Q = 1.0
            if norm_Q == -1 or norm_Q < Q: norm_Q = Q
            for isyst in ibin._allSysts:
                # only check signal systematics, assume not correlated with any bkgs
                if 'sig' not in isyst._bins: continue
                # get range of this syst
                irange = 0
                if len(isyst._vals[0])==1: irange = abs(1-isyst._vals[0][0])
                elif len(isyst._vals[0])==2: irange = max(abs(1-isyst._vals[0][0]),abs(1-isyst._vals[0][1]))
                # weight range based on Q (normalize later)
                irange *= Q
                # check min and max
                tmp_minmax = syst_minmax.get(isyst._name,[1e10, 0])
                syst_minmax[isyst._name] = [min( tmp_minmax[0], irange ), max( tmp_minmax[1], irange )]

        # normalize ranges and make %
        maxSystNameLength = 0
        for k, v in syst_minmax.iteritems():
            syst_minmax[k] = [v[0]/norm_Q*100, v[1]/norm_Q*100]
            if len(k) > maxSystNameLength: maxSystNameLength = len(k)

        # output results
        ofile = open(odir+'/syst_'+self._regionName+'_method'+str(method)+'.txt','w');
        myformat = "{:<"+str(maxSystNameLength+2)+"} {:10.6f} {:10.6f}"
        for k, v in syst_minmax.iteritems():
            ofile.write(myformat.format(k,v[0],v[1])+"\n")
        #pprint.pprint(syst_minmax,ofile)
        ofile.close()
