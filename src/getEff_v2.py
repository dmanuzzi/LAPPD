import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputFile', type = str, dest = 'inputFile')
parser.add_argument('-o','--outFile', type = str, dest = 'outFile', default = 'output_getEff_v2.root')
parser.add_argument('-d','--dir', type = str, dest = 'dir', default = './')
parser.add_argument('-vv','--variables', nargs='+', dest = 'variables', default = ['run','x', 'y', 'max0', 'max1', 'max2', 'max3'])
args = parser.parse_args()

nfin_dat = args.inputFile+'.dat'
nfin_root = args.inputFile+'.root'
nfout = args.outFile
outDir = args.dir
if args.dir != './':
    nfin_dat = f'{outDir}/{nfin_dat}'
    nfin_root = f'{outDir}/{nfin_root}'
    nfout = f'{outDir}/{nfout}'
    
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine(".L /home/LHCB-T3/dmanuzzi/LAPPD/2022decemberDESY/src/lhcbStyle.C");
ROOT.EnableImplicitMT()
#---------------------------------------------------
tin = ROOT.TTree('tin', 'tin')
n_list_variables = ':'.join(args.variables)
tin.ReadFile(nfin_dat, n_list_variables)
f_root = ROOT.TFile.Open(nfin_root, 'RECREATE')
f_root.WriteTObject(tin)
f_root.Close()
#exit()
#---------------------------------------------------

fout = ROOT.TFile.Open(nfout, 'RECREATE')
rdf = ROOT.RDataFrame('tin', nfin_root)

rdf = rdf.Define('smax', 'max0+max1+max2+max3')
rdf = rdf.Define('x0', 'x+8.5').Define('y0', 'y+13')

h_smax           = rdf.Histo1D(('h_smax', 'h_smax',200,0,2), 'smax')
h_smax_zoom      = rdf.Histo1D(('h_smax_zoom', 'h_smax_zoom',100,0,0.15), 'smax')
h_smax_zooom     = rdf.Histo1D(('h_smax_zooom', 'h_smax_zooom',100,0,0.05), 'smax')
xmin = -8.5-12.5
xmax = -8.5+12.5
ymin = -13.0-12.5
ymax = -13.0+12.5
h_xy             = rdf.Histo2D(('h_xy_data', 'h_xy_data; x(dwc2) [mm];y(dwc2) [mm]; Candidates', 25, xmin,xmax,25,ymin,ymax), 'x', 'y')

for h in [h_smax, h_smax_zoom, h_smax_zooom, h_xy]:
    ncanv = h.GetName().replace('h_', 'c_')
    canv = ROOT.TCanvas(ncanv, ncanv)
    canv.cd()
    drawopt = 'hist'
    if h.GetName() == 'h_xy_data':
        drawopt = 'colz'
        h.SetStats(0)
    else:
        h.SetLineWidth(2)
        h.SetLineColor(ROOT.kBlack)
    h.Draw(drawopt)
    canv.Draw()
    canv.SaveAs(f'{outDir}/{canv.GetName()}.pdf')
    fout.WriteTObject(canv, canv.GetName())
    fout.WriteTObject(h.GetValue(), h.GetValue().GetName())
    
    
import math
smax_cuts = ['0.0140','0.0160','0.0180','0.0200','0.0220', '0.1000']

Nrdf_smax_cuts = []
h_pass_smax_cuts = []
for smax_cut in smax_cuts:
    rdf_tmp = rdf.Filter('smax>'+smax_cut, 'smax '+smax_cut)
    Nrdf_smax_cuts.append(rdf_tmp.Count())
    nh = 'h_xy_pass_smax_cut_'+smax_cut.replace('0.', '')
    h_pass_smax_cuts.append(rdf_tmp.Histo2D((nh, nh,  25, xmin,xmax,25,ymin,ymax), 'x', 'y'))
    
eff_den = rdf.Count().GetValue()

    
N_smax = []
eff_smax = []
for Nrdf_tmp, smax_cut, h_pass in zip(Nrdf_smax_cuts, smax_cuts, h_pass_smax_cuts):
    _N = Nrdf_tmp.GetValue()
    _eff = _N/eff_den
    print(f' eff smax  {smax_cut}: {_eff:.3f}')
    N_smax.append(_N)
    eff_smax.append(_eff)
    h = h_pass.GetValue()
    h.Sumw2()
    h.Divide(h_xy.GetValue())
    h.SetName(h.GetName().replace('h_xy_pass','h_xy_eff'))
    ncanv = h.GetName().replace('h_', 'c_')
    canv = ROOT.TCanvas(ncanv, ncanv)
    h.SetStats(0)
    h.SetMinimum(0.50)
    h.SetMaximum(1.00)
    h.Draw('colz')
    canv.Draw()
    canv.SaveAs(f'{outDir}/{canv.GetName()}.pdf')
    fout.WriteTObject(canv, canv.GetName())
    fout.WriteTObject(h, h.GetName())
    
    
energy = args.inputFile.split('GeV')[0].split('_')[-1]

#############################
d_smax = {
    'smax_cuts' : smax_cuts,
    'eff_smax' : eff_smax,
    'N_smax' : N_smax,
    'eff_den' : [eff_den]*len(smax_cuts),
    'energy' : [energy]*len(smax_cuts),
}

print(d_smax)
import pickle
with open(outDir+'/eff_smax.pickle', 'wb') as handle:
    pickle.dump(d_smax, handle, protocol=pickle.HIGHEST_PROTOCOL)
import json
with open(outDir+'/eff_smax.json', 'w') as handle:
    json.dump(d_smax, handle, indent=2)

fout.Close()