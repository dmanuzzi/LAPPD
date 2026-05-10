import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputFile', type = str, dest = 'inputFile')
parser.add_argument('-o','--outFile', type = str, dest = 'outFile', default = 'output_positionPlots.root')
parser.add_argument('-d','--dir', type = str, dest = 'dir', default = './')
parser.add_argument('-vv','--variables', nargs='+', dest = 'variables', default = ['xp','yp','xt','yt','max3','max2','max1','max0'])
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

f_root = ROOT.TFile.Open(nfin_root, 'recreate')
tin = ROOT.TTree('tin', 'tin')
tin.ReadFile(nfin_dat, ':'.join(args.variables))
f_root.WriteTObject(tin, 'T')
f_root.Close()

xcenter = -8.5
ycenter = -13.0
xmin = xcenter-12.5
xmax = xcenter+12.5
ymin = ycenter-12.5
ymax = ycenter+12.5


fout = ROOT.TFile.Open(nfout, 'recreate')
rdf = ROOT.RDataFrame('T', nfin_root)
rdf = rdf.Define('dx', 'xp-xt').Define('dy', 'yp-yt').Define('dr', 'sqrt(dx*dx+dy*dy)')
rdf_baseline = rdf.Filter(f'abs(xt-({xcenter}))<12.5 && abs(yt-({ycenter}))<12.5', 'baseline')
rdf_baselineX = rdf.Filter(f'abs(xt-({xcenter}))<12.5', 'baselineX')
rdf_baselineY = rdf.Filter(f'abs(yt-({ycenter}))<12.5', 'baselineY')
rdf_reduced = rdf.Filter(f'abs(xt-({xcenter}))<7 && abs(yt-({ycenter}))<7', 'reduced')
rdf_reducedX = rdf.Filter(f'abs(xt-({xcenter}))<7', 'reducedX')
rdf_reducedY = rdf.Filter(f'abs(yt-({ycenter}))<7', 'reducedY')


v_h_res_x = [rdf.Histo1D(('h_res_x', 'h_res_x;x(predicted)-x(dwc2) [mm];Candidates', 100, -25, 25), 'dx'),
             rdf_baseline.Histo1D(('h_res_x_baseline', 'h_res_x_baseline;x(predicted)-x(dwc2) [mm];Candidates', 100, -25, 25), 'dx'),
             rdf_baselineX.Histo1D(('h_res_x_baselineX', 'h_res_x_baselineX;x(predicted)-x(dwc2) [mm];Candidates', 100, -25, 25), 'dx'),
             rdf_reduced.Histo1D(('h_res_x_reduced', 'h_res_x_reduced;x(predicted)-x(dwc2) [mm];Candidates', 100, -25, 25), 'dx'),
             rdf_reducedX.Histo1D(('h_res_x_reducedX', 'h_res_x_reducedX;x(predicted)-x(dwc2) [mm];Candidates', 100, -25, 25), 'dx')]
            
v_h_res_y = [rdf.Histo1D(('h_res_y', 'h_res_y;y(predicted)-y(dwc2) [mm];Candidates', 100, -25, 25), 'dy'),
             rdf_baseline.Histo1D(('h_res_y_baseline', 'h_res_y_baseline;y(predicted)-y(dwc2) [mm];Candidates', 100, -25, 25), 'dy'),
             rdf_baselineY.Histo1D(('h_res_y_baseliney', 'h_res_y_baseliney;y(predicted)-y(dwc2) [mm];Candidates', 100, -25, 25), 'dy'),
             rdf_reduced.Histo1D(('h_res_y_reduced', 'h_res_y_reduced;y(predicted)-y(dwc2) [mm];Candidates', 100, -25, 25), 'dy'),
             rdf_reducedY.Histo1D(('h_res_y_reducedy', 'h_res_y_reducedy;y(predicted)-y(dwc2) [mm];Candidates', 100, -25, 25), 'dy')]

h_dr = rdf.Histo1D(('h_dr', 'h_dr; dr [mm];Candidates', 100, 0, 25), 'dr')
v_h_xtyt = [rdf.Histo2D(('h_xtyt', 'h_xtyt; x(dwc2) [mm];y(dwc2) [mm];Candidates', 100,xmin-12.5, xmax+12.5, 100,ymin-12.5,ymax+12.5), 'xt', 'yt'),
            rdf_baseline.Histo2D(('h_xtyt_baseline', 'h_xtyt_baseline; x(dwc2) [mm];y(dwc2) [mm];Candidates', 100,xmin-12.5, xmax+12.5, 100,ymin-12.5,ymax+12.5), 'xt', 'yt'),
            rdf_baselineX.Histo2D(('h_xtyt_baselineX', 'h_xtyt_baselineX; x(dwc2) [mm];y(dwc2) [mm];Candidates', 100,xmin-12.5, xmax+12.5, 100,ymin-12.5,ymax+12.5), 'xt', 'yt'),
            rdf_baselineY.Histo2D(('h_xtyt_baselineY', 'h_xtyt_baselineY; x(dwc2) [mm];y(dwc2) [mm];Candidates', 100,xmin-12.5, xmax+12.5, 100,ymin-12.5,ymax+12.5), 'xt', 'yt'),
            rdf_reduced.Histo2D(('h_xtyt_reduced', 'h_xtyt_reduced; x(dwc2) [mm];y(dwc2) [mm];Candidates', 100,xmin-12.5, xmax+12.5, 100,ymin-12.5,ymax+12.5), 'xt', 'yt'),
            rdf_reducedX.Histo2D(('h_xtyt_reducedX', 'h_xtyt_reducedX; x(dwc2) [mm];y(dwc2) [mm];Candidates', 100,xmin-12.5, xmax+12.5, 100,ymin-12.5,ymax+12.5), 'xt', 'yt'),
            rdf_reducedY.Histo2D(('h_xtyt_reducedY', 'h_xtyt_reducedY; x(dwc2) [mm];y(dwc2) [mm];Candidates', 100,xmin-12.5, xmax+12.5, 100,ymin-12.5,ymax+12.5), 'xt', 'yt'),
]
h_xpyp = rdf.Histo2D(('h_xpyp', 'h_xpyp; x(predicted) [mm];y(predicted) [mm];Candidates', 100,xmin-12.5, xmax+12.5, 100,ymin-12.5,ymax+12.5), 'xp', 'yp')
delta=0
if 'wideRange' in args.inputFile:
    delta=12.5
h_xpxt = rdf.Histo2D(('h_xpxt', 'h_xpxt; x(predicted) [mm];x(dwc2) [mm];Candidates', 100,xmin-delta, xmax+delta, 100,xmin-delta, xmax+delta), 'xp', 'xt')
h_xtxp = rdf.Histo2D(('h_xtxp', 'h_xtxp; x(dwc2) [mm];x(predicted) [mm];Candidates', 100,xmin-delta, xmax+delta, 100,xmin-delta, xmax+delta), 'xt', 'xp')
h_xtdx = rdf.Histo2D(('h_xtdx', 'h_xtdx; x(dwc2) [mm];x(predicted)-x(dwc2) [mm];Candidates', 100,xmin-delta, xmax+delta, 100,-25, 25), 'xt', 'dx')
h_xpdx = rdf.Histo2D(('h_xpdx', 'h_xpdx; x(predicted) [mm];x(predicted)-x(dwc2) [mm];Candidates', 100,xmin-delta, xmax+delta, 100,-25, 25), 'xp', 'dx')

h_ypyt = rdf.Histo2D(('h_ypyt', 'h_ypyt; y(predicted) [mm];y(dwc2) [mm];Candidates', 100,ymin-delta,ymax+delta, 100,ymin-delta,ymax+delta), 'yp', 'yt')
h_ytyp = rdf.Histo2D(('h_ytyp', 'h_ytyp; y(dwc2) [mm];y(predicted) [mm];Candidates', 100,ymin-delta,ymax+delta, 100,ymin-delta,ymax+delta), 'yt', 'yp')
h_ytdy = rdf.Histo2D(('h_ytdy', 'h_ytdy; y(dwc2) [mm];y(predicted)-y(dwc2) [mm];Candidates', 100,ymin-delta,ymax+delta, 100,-25, 25), 'yt', 'dy')
h_ypdy = rdf.Histo2D(('h_ypdy', 'h_ypdy; y(predicted) [mm];y(predicted)-y(dwc2) [mm];Candidates', 100,ymin-delta,ymax+delta, 100,-25, 25), 'yp', 'dy')
v_prof2_xtytmax = [
    rdf.Profile2D(('hpf2_max0', 'hpf2_max0; x(dwc2) [mm];y(dwc2) [mm]; <A(G4)> [a.u.]', 100, xmin-delta, xmax+delta, 100, ymin-delta, ymax+delta), 'xt', 'yt', 'max0'),
    rdf.Profile2D(('hpf2_max1', 'hpf2_max1; x(dwc2) [mm];y(dwc2) [mm]; <A(G5)> [a.u.]', 100, xmin-delta, xmax+delta, 100, ymin-delta, ymax+delta), 'xt', 'yt', 'max1'),
    rdf.Profile2D(('hpf2_max2', 'hpf2_max2; x(dwc2) [mm];y(dwc2) [mm]; <A(H4)> [a.u.]', 100, xmin-delta, xmax+delta, 100, ymin-delta, ymax+delta), 'xt', 'yt', 'max2'),
    rdf.Profile2D(('hpf2_max3', 'hpf2_max3; x(dwc2) [mm];y(dwc2) [mm]; <A(H5)> [a.u.]', 100, xmin-delta, xmax+delta, 100, ymin-delta, ymax+delta), 'xt', 'yt', 'max3'),
]

import math
def fitGausAndDraw(ncanv, h, drawopt, 
                   h_lineColor=ROOT.kBlack, h_lineWidth=2, h_markerColor=ROOT.kBlack, h_markerStyle=20, 
                   f_lineColor=ROOT.kRed, f_lineWidth=1):
    canv = ROOT.TCanvas(ncanv, ncanv)
    canv.cd()
    h.Fit('gaus', '0')
    func = h.GetFunction('gaus')
    func.SetName('gaus_fit_'+h.GetName())
    mu = func.GetParameter(1)
    sigma = func.GetParameter(2)
    muErr = func.GetParError(1)
    sigmaErr = func.GetParError(2)
    
    h.SetLineColor(h_lineColor)
    h.SetLineWidth(h_lineWidth)
    h.SetMarkerColor(h_markerColor)
    h.SetMarkerStyle(h_markerStyle)
    
    func.SetLineColor(f_lineColor)
    func.SetLineWidth(f_lineWidth)
    fout.WriteTObject(h, h.GetName())
    fout.WriteTObject(func, func.GetName())
    
    binwidth = h.GetXaxis().GetBinWidth(1)
    # h.Scale(1.0/binwidth)
    # h.GetYaxis().SetTitle(f'Candidates / {binwidth} [ns] ')
    if 'norm' in drawopt:
        h.Scale(1.0/binwidth/h.Integral())
        func.SetParameter(0,1.0/(2*math.pi*sigma**2)**0.5)
        drawopt = drawopt.replace('norm', '')
        h.GetYaxis().SetTitle(f'Norm. Candidates / {binwidth} [ns] ')
    h.Draw(drawopt)
    func.Draw('lsame')
    canv.Draw()
    canv.SaveAs(f'{outDir}/{canv.GetName()}.pdf')    
    fout.WriteTObject(canv, canv.GetName())
    return mu, muErr, sigma, sigmaErr

d_resXY = {'config' : args.inputFile}
for h_pointer in v_h_res_x+v_h_res_y:
    h = h_pointer.GetValue()
    ncanv = h.GetName().replace('h_', 'c_')
    mu, muErr, sigma, sigmaErr = fitGausAndDraw(ncanv, h, 'pe1')
    nvar = h.GetName().replace('h_res_', '')
    d_resXY[f'mu_{nvar}'] = [mu]
    d_resXY[f'mu_err_{nvar}'] = [muErr]
    d_resXY[f'sigma_{nvar}'] = [sigma]
    d_resXY[f'sigma_err_{nvar}'] = [sigmaErr]
    
import pickle
with open(outDir+'/resXY.pickle', 'wb') as handle:
    pickle.dump(d_resXY, handle, protocol=pickle.HIGHEST_PROTOCOL)
import json
with open(outDir+'/resXY.json', 'w') as handle:
    json.dump(d_resXY, handle, indent=2)
    
for h_pointer in v_h_xtyt+[h_dr]+v_prof2_xtytmax:
    h = h_pointer.GetValue()
    ncanv = h.GetName().replace('h_', 'c_')
    canv = ROOT.TCanvas(ncanv, ncanv)
    canv.cd()
    if 'hpf2_max' in h.GetName():
        h.SetMinimum(0)
        h.SetMaximum(0.25)
    if h.GetName() == 'h_dr':
        h.Draw('pe1')
    else:
        h.SetStats(False)
        h.Draw('colz')
        canv.SetGridx()
        canv.SetGridy()
    canv.Draw()
    fout.WriteTObject(h, h.GetName())
    fout.WriteTObject(canv, canv.GetName())
    canv.SaveAs(f'{outDir}/{canv.GetName()}.pdf')    

for h_pointer in [h_xpxt, h_xtxp, h_xtdx, h_xpdx, h_ypyt, h_ytyp, h_ytdy, h_ypdy]:
    h = h_pointer.GetValue()
    ncanv = h.GetName().replace('h_', 'c_')
    canv = ROOT.TCanvas(ncanv, ncanv)
    canv.cd()
    h.SetStats(False)
    h.Draw('colz')
    hpfx = h.ProfileX()
    hpfx.SetLineColor(ROOT.kRed)
    hpfx.SetLineWidth(2)
    hpfx.SetMarkerSize(0)
    hpfx.Draw('pe same')
    canv.SetGridx()
    canv.SetGridy()
    canv.Draw()
    fout.WriteTObject(h, h.GetName())
    fout.WriteTObject(hpfx, hpfx.GetName())
    fout.WriteTObject(canv, canv.GetName())
    canv.SaveAs(f'{outDir}/{canv.GetName()}.pdf')    

fout.Close()