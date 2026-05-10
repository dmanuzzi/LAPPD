import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputFile', type = str, dest = 'inputFile')
parser.add_argument('-o','--outFile', type = str, dest = 'outFile', default = 'output_getEff.root')
parser.add_argument('-d','--dir', type = str, dest = 'dir', default = './')
parser.add_argument('-vv','--variables', nargs='+', dest = 'variables', default = ['tt', 't', 'x', 'y', 'dt_mcp',
                                                                                   't0_5', 't1_5', 't2_5', 't3_5', 
                                                                                   'max0', 'max1', 'max2', 'max3'])
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
ROOT.gROOT.ProcessLine(".L /home/LHCB-T3/dmanuzzi/LAPPD/2023julySPS/src/lhcbStyle.C");
ROOT.gStyle.SetOptStat(0);
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

rdf = rdf.Define('dt_rf', 't-tt')
rdf = rdf.Define('x0', 'x+8.5').Define('y0', 'y+13.0')
rdf = rdf.Filter('x0>-12.5 && x0<12.5 && y0>-12.5 && y0<12.5')
rdf = rdf.Define('smax', 'max0+max1+max2+max3')
choose_t_cfd = '''
if      (x0<0 && y0>0) return t0_5; 
else if (x0>0 && y0>0) return t1_5; 
else if (x0<0 && y0<0) return t2_5; 
else return t3_5'''

choose_max = '''
if      (x0<0 && y0>0) return max0; 
else if (x0>0 && y0>0) return max1; 
else if (x0<0 && y0<0) return max2; 
else return max3'''

rdf = rdf.Define('t_cfd', choose_t_cfd)
rdf = rdf.Define('max', choose_max)
rdf = rdf.Define('dt_cfd_tmp', 't_cfd-tt')

cut_best = ' abs(dt_cfd_tmp)<2000'
rdf_best = rdf.Filter(cut_best)
mean_dt_cfd_tmp = rdf_best.Mean('dt_cfd_tmp')
rdf = rdf.Define('dt_cfd', 'dt_cfd_tmp-(%f)'%mean_dt_cfd_tmp.GetValue())
print('*************************', mean_dt_cfd_tmp.GetValue())


rdfG4_best = rdf.Filter('x0<0 && y0>0 &&'+cut_best)
rdfG5_best = rdf.Filter('x0>0 && y0>0 &&'+cut_best)
rdfH4_best = rdf.Filter('x0<0 && y0<0 &&'+cut_best)
rdfH5_best = rdf.Filter('x0>0 && y0<0 &&'+cut_best)

h_dt_cfd_G4 = rdfG4_best.Histo1D(('h_dt_cfd_G4', 'h_dt_cfd_G4', 100,-0.1,1), 'dt_cfd')
h_dt_cfd_G5 = rdfG5_best.Histo1D(('h_dt_cfd_G5', 'h_dt_cfd_G5', 100,-0.1,1), 'dt_cfd')
h_dt_cfd_H4 = rdfH4_best.Histo1D(('h_dt_cfd_H4', 'h_dt_cfd_H4', 100,-0.1,1), 'dt_cfd')
h_dt_cfd_H5 = rdfH5_best.Histo1D(('h_dt_cfd_H5', 'h_dt_cfd_H5', 100,-0.1,1), 'dt_cfd')

c_dt_cfd = ROOT.TCanvas('c_dt_cfd', 'c_dt_cfd')
h_dt_cfd_G4.SetLineColor(ROOT.kBlue)
h_dt_cfd_G5.SetLineColor(ROOT.kCyan)
h_dt_cfd_H4.SetLineColor(ROOT.kRed)
h_dt_cfd_H5.SetLineColor(ROOT.kMagenta)
tmp_max = max(h_dt_cfd_G4.GetValue().GetMaximum(), h_dt_cfd_G5.GetValue().GetMaximum(),
              h_dt_cfd_H4.GetValue().GetMaximum(), h_dt_cfd_H5.GetValue().GetMaximum())
for h in [h_dt_cfd_G4.GetValue(), h_dt_cfd_G5.GetValue(), h_dt_cfd_H4.GetValue(), h_dt_cfd_H5.GetValue()]:
    fout.WriteTObject(h, h.GetName())
    h.SetMaximum(tmp_max*1.05)
h_dt_cfd_G4.Draw('hist')
h_dt_cfd_G5.Draw('hist same')
h_dt_cfd_H4.Draw('hist same')
h_dt_cfd_H5.Draw('hist same')
c_dt_cfd.Draw()
c_dt_cfd.SaveAs(f'{outDir}/{c_dt_cfd.GetName()}.pdf')
fout.WriteTObject(c_dt_cfd, c_dt_cfd.GetName())
    

bias_dt_cfd_G4 = h_dt_cfd_G4.GetMean()
bias_dt_cfd_G5 = h_dt_cfd_G5.GetMean()
bias_dt_cfd_H4 = h_dt_cfd_H4.GetMean()
bias_dt_cfd_H5 = h_dt_cfd_H5.GetMean()

calib_dt_cfd = f'''
if      (x0<0 && y0>0) return dt_cfd-({bias_dt_cfd_G4}); 
else if (x0>0 && y0>0) return dt_cfd-({bias_dt_cfd_G5}); 
else if (x0<0 && y0<0) return dt_cfd-({bias_dt_cfd_H4}); 
else return dt_cfd-({bias_dt_cfd_H5})'''
rdf = rdf.Define('dt_cfd_calib', calib_dt_cfd)

h_resT_RF        = rdf.Histo1D(('h_resT_RF', 'h_resT_RF', 100, -0.3, 0.3), 'dt_rf')
h_resT_CFD       = rdf.Histo1D(('h_resT_CFD','h_resT_CFD', 100, -0.3, 0.3), 'dt_cfd_calib')
h_resT_MCP       = rdf.Histo1D(('h_resT_mcp','h_resT_mcp', 100, -0.15, 0.45), 'dt_mcp')
h_max            = rdf.Histo1D(('h_max', 'h_max',100,0,0.5), 'max')
h_max_zoom       = rdf.Histo1D(('h_max_zoom', 'h_max_zoom',100,0,0.15), 'max')
h_max_zooom      = rdf.Histo1D(('h_max_zooom', 'h_max_zooom',100,0,0.02), 'max')
h_xy             = rdf.Histo2D(('h_xy', 'h_xy', 50, -12.5,12.5,50,-12.5,12.5), 'x0', 'y0')

for h in [h_max, h_max_zoom, h_max_zooom, h_xy]:
    ncanv = h.GetName().replace('h_', 'c_')
    canv = ROOT.TCanvas(ncanv, ncanv)
    canv.cd()
    drawopt = 'hist'
    if h.GetName() == 'h_xy':
        drawopt = 'colz'
    else:
        h.SetLineWidth(2)
        h.SetLineColor(ROOT.kBlack)
    h.Draw(drawopt)
    canv.Draw()
    canv.SaveAs(f'{outDir}/{canv.GetName()}.pdf')
    fout.WriteTObject(canv, canv.GetName())
    fout.WriteTObject(h.GetValue(), h.GetValue().GetName())
    
    
import math
def fitGausAndDraw(ncanv, h, drawopt, 
                   h_lineColor=ROOT.kBlack, h_lineWidth=2, h_markerColor=ROOT.kBlack, h_markerStyle=20, 
                   f_lineColor=ROOT.kRed, f_lineWidth=1):
    canv = ROOT.TCanvas(ncanv, ncanv)
    canv.cd()
    h.Fit('gaus', '0')
    func = h.GetFunction('gaus')
    func.SetName('gaus_fit_'+h.GetName())
    entries = h.Integral()
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
    #h.SetStats(0)
    h.Draw(drawopt)
    func.Draw('lsame')
    text = ROOT.TPaveText(0.18,0.72,0.39, 0.92, "NDC")
    text.SetFillColor(0)
    text.SetTextAlign(12)
    text.AddText(f'Entries: {entries:.0f}')
    text.AddText(f'#mu = {mu*1000:.2f} #pm {muErr*1000:.2f} ps')
    text.AddText(f'#sigma = {sigma*1000:.2f} #pm {sigmaErr*1000:.2f} ps')
    text.Draw('same')
    canv.Draw()
    canv.SaveAs(f'{outDir}/{canv.GetName()}.pdf')    
    fout.WriteTObject(canv, canv.GetName())
    return mu, muErr, sigma, sigmaErr

mu_mcp, mu_mcp_err, sigma_mcp, sigma_mcp_err = fitGausAndDraw('c_resT_MCP', h_resT_MCP.GetValue(),'pe1')
mu_rf,  mu_rf_err,  sigma_rf,  sigma_rf_err  = fitGausAndDraw('c_resT_RF',  h_resT_RF.GetValue(), 'pe1')
mu_cfd, mu_cfd_err, sigma_cfd, sigma_cfd_err = fitGausAndDraw('c_resT_CFD', h_resT_CFD.GetValue(),'pe1')
print(f'sigma CFD: {sigma_cfd:.4f} +/- {sigma_cfd_err:.4f}')
print(f'sigma  RF: {sigma_rf:.4f} +/- {sigma_rf_err:.4f}')
print(f'sigma MCP: {sigma_mcp:.4f} +/- {sigma_mcp_err:.4f}')
resT_cfd = (sigma_cfd**2-0.25*sigma_mcp**2)**0.5
resT_rf = (sigma_rf**2-0.25*sigma_mcp**2)**0.5
resT_rf_err = ((sigma_rf*sigma_rf_err/resT_rf)**2+(sigma_mcp*sigma_mcp_err/(4*resT_rf))**2)**0.5
print(f'resT CFD: {resT_cfd:.4f}')
print(f'resT  RF: {resT_rf:.4f} +/- {resT_rf_err:.4f}')


sigma_cuts = ['1','2', '3', '5', '10']
max_cuts = ['0.000','0.0010', '0.0015', '0.0020', '0.0025', '0.0030', '0.0035', '0.0040', '0.0045', '0.0050', '0.0100', '0.0125', '0.1000']

#n_pos = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
#x_pos = [-9.375, -3.125, +3.125, +9.375, -9.375, -3.125, +3.125, +9.375, -9.375, -3.125, +3.125, +9.375, -9.375, -3.125, +3.125, +9.375]
#y_pos = [-9.375, -9.375, -9.375, -9.375, -3.125, -3.125, -3.125, -3.125, +3.125, +3.125, +3.125, +3.125, +9.375, +9.375, +9.375, +9.375]
#dx_pos = 16*[3.125]
#dy_pos = 16*[3.125]

dpos = 25/6
n_pos = [0,1,2,3,4,5,6,7,8]
x_pos = [-2*dpos,  0*dpos, +2*dpos, -2*dpos,  0*dpos, +2*dpos, -2*dpos,  0*dpos, +2*dpos]
y_pos = [-2*dpos, -2*dpos, -2*dpos,  0*dpos,  0*dpos,  0*dpos, +2*dpos, +2*dpos, +2*dpos]
dx_pos = 9*[dpos]
dy_pos = 9*[dpos]


h_resT_rf_pos_cuts = []
h_resT_mcp_pos_cuts = []

for n,x,y,dx,dy in zip(n_pos, x_pos, y_pos, dx_pos, dy_pos):
    pos_cut = f'abs(x0-({x}))<{dx} && abs(y0-({y}))<{dy}'
    rdf_tmp = rdf.Filter(pos_cut, str(n))
    h_rf  = rdf_tmp.Histo1D((f'h_resT_RF_pos_{n}', f'h_resT_RF_pos_{n}', 150, -0.3, 0.3), 'dt_rf')
    h_mcp = rdf_tmp.Histo1D((f'h_resT_mcp_pos_{n}', f'h_resT_mcp_pos_{n}', 150, -0.15, 0.45), 'dt_mcp')
    h_resT_rf_pos_cuts.append(h_rf)
    h_resT_mcp_pos_cuts.append(h_mcp)
    
        
Nrdf_sigma_rf = []
Nrdf_sigma_cfd = []
for sigma_cut in sigma_cuts:
    Nrdf_sigma_rf.append(rdf.Filter('abs(dt_rf)<%s*%f'%(sigma_cut,sigma_rf)).Count())
    Nrdf_sigma_cfd.append(rdf.Filter('abs(dt_cfd_calib)<%s*%f'%(sigma_cut,sigma_cfd)).Count())
h_resT_rf_max_cuts = []
Nrdf_max_cuts = []
for max_cut in max_cuts:
    max_cut2 = max_cut.replace('0.','')
    rdf_tmp = rdf.Filter('max>'+max_cut, 'max '+max_cut) 
    h_resT_rf_tmp = rdf_tmp.Histo1D((f'h_resT_RF_max_{max_cut2}', f'h_resT_RF_max_{max_cut}', 150, -0.3, 0.3), 'dt_rf')
    Nrdf_max_cuts.append(rdf_tmp.Count())
    h_resT_rf_max_cuts.append(h_resT_rf_tmp)

eff_den = rdf.Count().GetValue()

pos_rf_mu = []
pos_rf_mu_err = []
pos_rf_sigma = []
pos_rf_sigma_err = []
pos_mcp_mu = []
pos_mcp_mu_err = []
pos_mcp_sigma = []
pos_mcp_sigma_err = []
for h_rf,h_mcp in zip(h_resT_rf_pos_cuts, h_resT_mcp_pos_cuts):
    ncanv = h_rf.GetValue().GetName().replace('h_', 'c_')
    mu, mu_err, sigma, sigma_err = fitGausAndDraw(ncanv, h_rf.GetValue(), 'pe1')
    pos_rf_mu.append(mu)
    pos_rf_mu_err.append(mu_err)
    pos_rf_sigma.append(sigma)
    pos_rf_sigma_err.append(sigma_err)
    ncanv = h_mcp.GetValue().GetName().replace('h_', 'c_')
    mu, mu_err, sigma, sigma_err = fitGausAndDraw(ncanv, h_mcp.GetValue(), 'pe1')
    pos_mcp_mu.append(mu)
    pos_mcp_mu_err.append(mu_err)
    pos_mcp_sigma.append(sigma)
    pos_mcp_sigma_err.append(sigma_err)


N_sigma_rf = []
N_sigma_cfd = []
eff_rf = []
eff_cfd = []
for _N_rf, _N_cfd in zip(Nrdf_sigma_rf, Nrdf_sigma_cfd):    
    eff_rf_tmp = _N_rf.GetValue()/eff_den
    eff_cfd_tmp = _N_cfd.GetValue()/eff_den
    print(f' eff RF  {sigma_cut} sigma: {eff_rf_tmp:.3f}')
    print(f' eff CFD  {sigma_cut} sigma: {eff_cfd_tmp:.3f}')
    N_sigma_rf.append(_N_rf.GetValue())
    N_sigma_cfd.append(_N_cfd.GetValue())
    eff_rf.append(eff_rf_tmp)
    eff_cfd.append(eff_cfd_tmp)
    
N_max = []
eff_max = []
max_rf_mu = []
max_rf_mu_err = []
max_rf_sigma = []
max_rf_sigma_err = []
for Nrdf_tmp, h_tmp, max_cut in zip(Nrdf_max_cuts, h_resT_rf_max_cuts, max_cuts):
    _N = Nrdf_tmp.GetValue()
    _eff = _N/eff_den
    print(f' eff max  {max_cut}: {_eff:.3f}')
    N_max.append(_N)
    eff_max.append(_eff)
    ncanv = h_tmp.GetValue().GetName().replace('h_', 'c_')
    mu, mu_err, sigma, sigma_err = fitGausAndDraw(ncanv, h_tmp.GetValue(), 'pe1')
    max_rf_mu.append(mu)
    max_rf_mu_err.append(mu_err)
    max_rf_sigma.append(sigma)
    max_rf_sigma_err.append(sigma_err)
    
    

energy = args.inputFile.split('GeV')[0].split('_')[-1]

#############################
d_resT = {
    'energy' : [energy],
    'mu_rf' : [mu_rf],
    'mu_rf_err' : [mu_rf_err],
    'sigma_rf' : [sigma_rf],
    'sigma_rf_err' : [sigma_rf_err],
    'mu_cfd' : [mu_cfd],
    'mu_cfd_err' : [mu_cfd_err],
    'sigma_cfd' : [sigma_cfd],
    'sigma_cfd_err' : [sigma_cfd_err],
    'mu_mcp' : [mu_mcp],
    'mu_mcp_err' : [mu_mcp_err],
    'sigma_mcp' : [sigma_mcp],
    'sigma_mcp_err' : [sigma_mcp_err],
    'resT_rf' : [resT_rf],
    #'resT_rf_err' : [resT_rf_err],
    'resT_cfd' : [resT_cfd],
}
d_sigma = {
    'sigma_cuts' : sigma_cuts,
    'eff_rf' : eff_rf,
    'eff_cfd' : eff_cfd,
    'N_rf' : N_sigma_rf,
    'N_cfd' : N_sigma_cfd,
    'eff_den' : [eff_den]*len(sigma_cuts),
    'energy' : [energy]*len(sigma_cuts),
}

d_max = {
    'max_cuts' : max_cuts,
    'eff_max' : eff_max,
    'N_max' : N_max,
    'eff_den' : [eff_den]*len(max_cuts),
    'energy' : [energy]*len(max_cuts),
    'max_rf_mu' : max_rf_mu,
    'max_rf_mu_err' : max_rf_mu_err,
    'max_rf_sigma' : max_rf_sigma,
    'max_rf_sigma_err' : max_rf_sigma_err,
}

d_pos = {
    'n' : n_pos,
    'x' : x_pos,
    'y' : y_pos,
    'dx': dx_pos,
    'dy': dy_pos,
    'rf_mu' : pos_rf_mu,
    'rf_mu_err' : pos_rf_mu_err,
    'rf_sigma' : pos_rf_sigma,
    'rf_sigma_err' : pos_rf_sigma_err,
    'mcp_mu' : pos_mcp_mu,
    'mcp_mu_err' : pos_mcp_mu_err,
    'mcp_sigma' : pos_mcp_sigma,
    'mcp_sigma_err' : pos_mcp_sigma_err,
    'energy' : [energy]*len(n_pos)
}

import pickle
with open(outDir+'/resT.pickle', 'wb') as handle:
    pickle.dump(d_resT, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open(outDir+'/eff_resT.pickle', 'wb') as handle:
    pickle.dump(d_sigma, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open(outDir+'/eff_max.pickle', 'wb') as handle:
    pickle.dump(d_max, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open(outDir+'/resT_pos.pickle', 'wb') as handle:
    pickle.dump(d_pos, handle, protocol=pickle.HIGHEST_PROTOCOL)

import json
with open(outDir+'/resT.json', 'w') as handle:
    json.dump(d_resT, handle, indent=2)
with open(outDir+'/eff_resT.json', 'w') as handle:
    json.dump(d_sigma, handle, indent=2)
with open(outDir+'/eff_max.json', 'w') as handle:
    json.dump(d_max, handle, indent=2)
with open(outDir+'/resT_pos.json', 'w') as handle:
    json.dump(d_pos, handle, indent=2)
