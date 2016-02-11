import sys
import collections

# helper class

class systLine:
    def __init__( self, name, type, bins, vals, correl=False ):
        self._name = name;
        self._type = type;
        self._bins = bins;
        self._vals = vals;
        self._correl = correl;
        
    def writeLine( self, binLabels, rates ):
        line = "";
        line += self._name + " " + self._type + " ";
        bin=0; # keeps track of correlations
        for i in range(len(binLabels)):
            if binLabels[i] in self._bins:
                if self._type == 'lnU' and rates[i] < 0.000001: line += str(val*1000) + " ";
                else:
                    if len(self._vals[bin])==1: # symmetric case
                        if self._vals[bin][0]>-99.: line += str(self._vals[bin][0]) + " ";
                        else: line += "- ";
                    elif len(self._vals[bin])==2: # asymmetric case
                        if self._vals[bin][0]>-99. and self._vals[bin][1]>-99.: line += str(self._vals[bin][0]) + "/" + str(self._vals[bin][1]) + " ";
                        else: line += "- ";
                    else:
                        line += "- ";
                if self._correl: bin+=1
            else: line += "- ";
        line += "\n";
        return line

class singleBin:

    def __init__( self , name, tag, binLabels, index ):

        self._name = name;
        self._tag  = tag;
        self._index  = index;
        self._binLabels = binLabels;
        self._rates = [];
        self._allLines = [];
        self._allSysts = [];

        # print "bin tag = ", tag, index

    def setRates( self, rates, normalize = False ):

        self._observed = float(sum(rates));
        
        # print self._index, self._observed, rates

        self._rates = [];
        if normalize: 
            if self._observed > 0: 
                self._rates = [x / self._observed for x in rates];
            else : self._rates = [1.]*len(rates);
        else: self._rates = rates;

    def writeRates( self ):

        #############################
        # yield part of the datacard
        line = "#the tag = %s \n" % (self._tag);
        self._allLines.append(line);
        
        line = "imax 1 #number of channels \n";
        self._allLines.append(line);
        line = "jmax %i #number of backgrounds \n" % (len(self._binLabels)-1);
        self._allLines.append(line);
        self._allLines.append("kmax * nuissance \n");
        self._allLines.append("shapes * * FAKE \n");
        self._allLines.append("------------ \n");

        line = "bin Bin"+self._name+"\n";
        self._allLines.append(line);
        
        line = "observation "+str(self._observed)+"\n";
        self._allLines.append(line);

        line = "bin ";
        for i in range(len(self._binLabels)): line += "Bin"+self._name + " ";
        line += "\n";
        self._allLines.append(line);

        line = "process ";
        for i in range(len(self._binLabels)): line += self._binLabels[i] + " ";
        line += "\n";
        self._allLines.append(line);

        line = "process ";
        for i in range(len(self._binLabels)): line += str(i) + " ";
        line += "\n";
        self._allLines.append(line);

        line = "rate ";
        zeroProxy = 0.0001;
        for rate in self._rates: 
            if rate < 0.000001: line += str(zeroProxy) + " ";
            else: line += "%.5f " % (rate);
        line += "\n";
        self._allLines.append(line);

        self._allLines.append("------------ \n");

    def addSystematic(self,sysname,systype,bins,val):
        systmp = systLine(sysname,systype,bins,[[val]])
        self._allSysts.append(systmp)

    def addCorrelSystematic(self,sysname,systype,bins,val1, val2):
        systmp = systLine(sysname,systype,bins,[[val1],[val2]],True)
        self._allSysts.append(systmp)

    def addCorrelSystematicAsym(self,sysname,systype,bins,val1up, val1dn, val2up,val2dn):
        systmp = systLine(sysname,systype,bins,[[val1dn,val1up],[val2dn,val2up]],True)
        self._allSysts.append(systmp)

    def addAsymSystematic(self,sysname,systype,bins,valup, valdown ):
        systmp = systLine(sysname,systype,bins,[[valdown,valup]])
        self._allSysts.append(systmp)

    def writeCard( self, odir ):
        
        ofile = open(odir+'/card_'+self._name+'.txt','w');
        for line in self._allLines: ofile.write(line);
        for syst in self._allSysts: ofile.write(syst.writeLine(self._binLabels,self._rates));
        ofile.close();
