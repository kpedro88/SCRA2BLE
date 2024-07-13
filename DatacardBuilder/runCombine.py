import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
import os
from common import get_options

def runCombine(options):
	# part 1: multidimfit to get likelihoods
	card = 'testCards-Moriond-%s-%1.1f/allcards.txt' % ( options.sms, options.lumi )
	cmd = [
		'combine',
		'--method MultiDimFit',
		'-d {}'.format(card),
		'--text2workspace --X-allow-no-signal',
		'--mass 125.0',
		'--algo grid',
		'--redefineSignalPOIs r',
		'--setParameterRanges r=0.0,1.5',
		'--points 4',
		'--alignEdges 1',
		'--saveNLL',
		'--cminDefaultMinimizerType Minuit2',
		'--cminDefaultMinimizerStrategy 0',
		'--cminDefaultMinimizerTolerance 0.1',
		'--cminFallbackAlgo "Minuit2,0:0.2"',
		'--name _{}_{}'.format(options.masses[0],options.masses[1]),
	]
	cmd = ' '.join(cmd)
	print(cmd)
	os.system(cmd)

	# part 2: extract relevant quantities
	# largely based on https://github.com/mmrowietz/CmsPmssm/blob/main/Combination/tools/statsharvestor.py
	cname = 'higgsCombine_{}_{}.MultiDimFit.mH125.root'.format(options.masses[0],options.masses[1])
	cfile = TFile.Open(cname)
	limit = cfile.Get('limit')

	# info for output tree
	analysis = 'cms_sus_19_006'
	ints = ['chain_index', 'Niteration']
	floats = ['llhd_{}_mu0p0f', 'Zsig_{}_mu0p5f', 'Zsig_{}_mu1p0f', 'Zsig_{}_mu1p5f', 'bf_{}_mu0p5f', 'bf_{}_mu1p0f', 'bf_{}_mu1p5f']
	floats = [f.format(analysis) for f in floats]
	if not 'quantile_t' in globals():
		gROOT.ProcessLine(
			"struct quantile_t { "+
			" ".join(["Int_t {};".format(qty) for qty in ints])+
			" ".join(["Double_t {};".format(qty) for qty in floats])+
			" };"
		)
	qobj = quantile_t()

	# create output tree
	oname = 'results_{}_{}.root'.format(options.masses[0],options.masses[1])
	ofile = TFile.Open(oname,'RECREATE')
	otree = TTree("mcmc","mcmc")
	for qty in ints:
		otree.Branch(qty, AddressOf(qobj,qty), '{}/I'.format(qty))
	for qty in floats:
		otree.Branch(qty, AddressOf(qobj,qty), '{}/D'.format(qty))

	# fill output tree
	qobj.chain_index = int(options.masses[0])
	qobj.Niteration = int(options.masses[1])

	limit.GetEntry(1)
	llhd0 = -2*limit.deltaNLL
	setattr(qobj, floats[0], llhd0)

	for i,entry in enumerate([2,3,4]):
		limit.GetEntry(entry)
		llhd = -2*limit.deltaNLL - llhd0
		setattr(qobj, floats[i+1], TMath.Sign(1,llhd)*TMath.Sqrt(2*abs(llhd)))
		setattr(qobj, floats[i+4], TMath.Exp(llhd))
	otree.Fill()
	ofile.cd()
	otree.Write()
	ofile.Close()

if __name__=="__main__":
	options = get_options(single=True,allow_unknown=True)
	runCombine(options)
