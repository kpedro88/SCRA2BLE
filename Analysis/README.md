# Analysis

## Skimming

[input\_selection.txt](input/input\_selection.txt) defines all the available selections, variations, and samples, as well as common global options.

To run interactively, applying the "signal" selection to the "T1tttt\_1500\_100" sample and writing output trees to a folder "tree\_test\_${SELECTION}":
```
root -b -q -l 'KSkimDriver.C+("input/input_selection.txt","T1tttt_1500_100","signal","root://cmseos.fnal.gov//store/user/awhitbe1/PHYS14productionV12","tree_test")'
```

To recompile the driver without running (preparing for batch submission):
```
root -b -q -l 'KSkimDriver.C++()'
```

To submit jobs to Condor:
```
./SKsub.sh
```

## Plotting

To plot yields vs. RA2 bin (where the binning can be defined in the input file) in the signal region and save the plot as an image:
```
root -l 'KPlotDriver.C+("root://cmseos.fnal.gov//store/user/pedrok/SUSY2015/Analysis/tree_signal","input/input_RA2bin.txt",1)'
```
Omitting the last argument will display the plot without saving it.

## Datacard creation

To save the individual histograms for each signal and background process to a ROOT file, for the creation of datacards for limit setting:
```
root -b -l -q MakeAllDC.C+
```
This macro calls the macro `KPlotDriverDC.C`, which is a modification of the macro from the previous section
that includes an extra input argument to specify the name of the output ROOT file.
These macros use modified input files that split up each background process (rather than stacking them together, as done for plotting).
The W+jets and ttbar processes are added together in the input file. The macro adds together the two single-lepton control region files
after they are generated.
