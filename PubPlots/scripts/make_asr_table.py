## make a compilable latex table with yields in 12 aggregate search regions

from __future__ import print_function
import os
import errno
from bg_est import BGEst
from data_obs import DataObs
from utils import GetPred
from ROOT import TFile

def make_asr_table(output_file,  lostlept, znn, qcd, data_obs): #,


    with open("/".join(["output", output_file+".tex"]), 'w') as fout:
        ## open template file saved in output reference directory
        with open('output/reference/asr_table_template.tex', 'r') as ftemp:
            template = ftemp.read().split('\n')
            edit = False
            for line in template:
                if line.find('Bin') == 0:
                    edit = True
                    fout.write(line+'\n')
                    continue
                elif line.find('\\end') == 0:
                    edit = False
                if edit:
                    ibin = int(line[0:2])
                    lostlept_pred = GetPred(lostlept, ibin)
                    line = line.replace('$$', lostlept_pred, 1)
                    znn_pred = GetPred(znn, ibin)
                    line = line.replace('$$', znn_pred, 1)
                    qcd_pred = GetPred(qcd, ibin)
                    line = line.replace('$$', qcd_pred, 1)
                    sumBG_pred = GetPred(BGEst.sumBG( lostlept, znn, qcd), ibin)
                    line = line.replace('$$', sumBG_pred, 1)
                    nobs = int(data_obs.hist.GetBinContent(ibin))
                    line = line.replace('$$', str(nobs), 1)
                fout.write(line+'\n')

##        fout.write(preamble)
##        ## get table and write it
##        table = ResultsTable(data_obs,  lostlep, znn, qcd, 1, 12, \
##                              "Observed number of events and pre-fit background predictions in the aggregate search regions.", "tab:pre-fit-results-asrs")
##        fout.write(table.full+"\n")
##
##        fout.write("\\end{document}\n")

if __name__ == "__main__": # to run from command line, just give the name of the BG estimation files
    import sys
    output_file = sys.argv[1]
    f_lostlept = TFile.Open(sys.argv[3])
    lostlept = BGEst(f_lostlept.Get("ASR/hCV"), f_lostlept.Get("ASR/hStatUp"), f_lostlept.Get("ASR/hStatDown"), f_lostlept.Get("ASR/hSystUp"), f_lostlept.Get("ASR/hSystDown"))
    f_znn = TFile.Open(sys.argv[4])
    znn = BGEst(f_znn.Get("ASR/hCV"), f_znn.Get("ASR/hStatUp"), f_znn.Get("ASR/hStatDown"), f_znn.Get("ASR/hSystUp"), f_znn.Get("ASR/hSystDown"))
    f_qcd = TFile.Open(sys.argv[5])
    qcd = BGEst(f_qcd.Get("ASR/hCV"), f_qcd.Get("ASR/hStatUp"), f_qcd.Get("ASR/hStatDown"), f_qcd.Get("ASR/hSystUp"), f_qcd.Get("ASR/hSystDown"))
    f_data_obs = TFile.Open(sys.argv[6])
    data_obs = DataObs(f_data_obs.Get("ASR/hCV"))

    make_asr_table(output_file,  lostlept, znn, qcd, data_obs) # , sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
