import pandas
import pickle
import numpy
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine(".L /home/LHCB-T3/dmanuzzi/LAPPD/2022decemberDESY/src/lhcbStyle.C");
list_df_resT = []
list_df_dt = []
list_df_smax = []
list_df_resT_pos = []
d_h = {}
fs_root = []
runs =  [
    'allRuns',
    'SPS2023allPos800V', 'SPS2023allPos825V', 
    # 'SPS2023center800V', 'SPS2023center825V',
    # 'SPS2023center875V', 'SPS2023center685V3mcp', 
    # 'SPS2023center685V3mcpLEDinhib500kHz', 
    # 'SPS2023center685V3mcpLEDinhib1MHz',
    # 'SPS2023center685V3mcpLEDinhib5MHz',
    # 'SPS2023center685V3mcpLEDinhib20MHz',
    #'SPS2023center685V3mcpLEDinhibAllRates'
]

def skipEnergy(runName, energy):
    if runName == 'allRuns3mcp' and (energy not in [1,3,5]): return True
    if runName == 'SPS2023center875V' and (energy != 20): return True
    if runName == 'SPS2023center685V3mcp' and (energy != 100): return True
    return False
            
#for list_df, feature in zip([list_df_resT, list_df_dt, list_df_smax, list_df_resT_pos],['resT', 'eff_resT', 'eff_smax', 'resT_pos']):   
for list_df, feature in zip([list_df_resT, list_df_resT_pos,list_df_smax],['resT', 'resT_pos', 'eff_smax']):   
    for run in runs:       
        energies = ([20,40,60,80,100] if (run!='allRuns') else [1,2,3,4,5,5.8])   
        for E in energies:
            if skipEnergy(run, E): continue
            dir = f'../out/{run}_{E}GeV_100_0_1_-1.0_sqrt_baseline'
            if 'allRuns' in run:
                dir = f'../../2022decemberDESY/out/{run}_{E}GeV_100_0_1_-1.0_sqrt_baseline'
            # dir = f'../out/{run}_{E}GeV_100_0_1_-1.0_sqrt_wideTrain'
            #dir = f'../out/{run}_{E}GeV_100_0_1_-1.0_sqrt_wideTrain_wideRadius'
            # dir = f'../out/{run}_{E}GeV_100_0_1_-1.0_sqrt_5risePoints'
            # dir = f'../out/{run}_{E}GeV_100_0_1_-1.0_sqrt_max70'
            # if run == 'SPS2023center685V3mcpAllRates':
            #     dir = f'../out/{run}_{E}GeV_100_0_1_-1.0_0_default'
            #print('----- ',dir)
            tmp_dict = {}        
            with open(f'{dir}/{feature}.pickle', 'rb') as handle:
                tmp_dict = pickle.load(handle)
            #print(tmp_dict)    
            tmp_df = pandas.DataFrame(tmp_dict)
            tmp_df = tmp_df.assign(runs = lambda x: run)
            print(tmp_df)
            list_df.append(tmp_df.copy())
            
df_resT = pandas.concat(list_df_resT, ignore_index=True)
# df_dt = pandas.concat(list_df_dt, ignore_index=True)
df_smax = pandas.concat(list_df_smax, ignore_index=True)
df_resT_pos = pandas.concat(list_df_resT_pos, ignore_index=True) 
import matplotlib
from matplotlib import pyplot as plt

df_resT = df_resT.astype({'energy' : 'float32'})
df_resT_pos = df_resT_pos.astype({'energy' : 'float32'})
df_smax = df_smax.astype({'smax_cuts':'str', 'energy':'float32'})


df_resT.eval('resT_rf_err  = ((sigma_rf*sigma_rf_err)**2+(0.25*sigma_mcp*sigma_mcp_err)**2)**0.5/resT_rf', inplace=True)
df_resT_pos.eval('resT_rf  = (rf_sigma**2-0.25*mcp_sigma**2)**0.5', inplace=True)
df_resT_pos.eval('resT_rf_err  = ((rf_sigma*rf_sigma_err)**2+(0.25*mcp_sigma*mcp_sigma_err)**2)**0.5/resT_rf', inplace=True)

#print(df_resT_pos)



##############################################################
##############################################################
##############################################################
##############################################################
'''
plt.figure()
for max_cut in max_cuts:
    tmp_df = df_max[df_max.max_cuts == max_cut]
    print(tmp_df)
    plt.plot(tmp_df.energy, tmp_df.resT_rf, label=f'max>{max_cut}', marker='o', linewidth=1)
    
plt.ylim(0,0.06)
plt.legend()
plt.xlabel('Energy [GeV]')
plt.ylabel('Efficiency')
plt.title('Amplitude-cut time resolution')
plt.grid(axis='both', linestyle='dotted')
plt.draw()

#energies = [1,2,3,4,5]
energies = [1,2,3,5]
plt.figure()
for energy in energies:
    tmp_df = df_dt[df_dt.energy == energy]
    tmp_df.sort_values(by=['sigma_cuts'])
    print(tmp_df)
    plt.plot(tmp_df.sigma_cuts, tmp_df.eff_rf, label=f'{energy} GeV', marker='o', linewidth=1)
    plt.plot(tmp_df.sigma_cuts, tmp_df.eff_cfd, marker='x',linestyle='dashed', linewidth=1, color=plt.gca().lines[-1].get_color())

plt.ylim(0.0,1.05)
plt.legend()
plt.xlabel('dt cut [N sigma]')
plt.ylabel('Efficiency')
plt.title('dt-cut efficiency')
plt.grid(axis='both', linestyle='dotted')
plt.draw()

plt.figure()
for energy in energies:
    tmp_df = df_max[df_max.energy == energy]
    tmp_df.sort_values(by=['max_cuts'])
    print(tmp_df)
    plt.plot(tmp_df.max_cuts, tmp_df.eff_max, label=f'{energy} GeV', marker='o', linewidth=1)
    
plt.ylim(0.0,1.05)
plt.legend()
plt.xlabel('amplitude cut [a.u]')
plt.ylabel('Efficiency')
plt.title('amplitude-cut efficiency')
plt.grid(axis='both', linestyle='dotted')
plt.draw()


plt.figure()
for energy in energies:
    tmp_df = df_max[df_max.energy == energy]
    tmp_df.sort_values(by=['max_cuts'])
    print(tmp_df)
    plt.plot(tmp_df.max_cuts, tmp_df.resT_rf, label=f'{energy} GeV', marker='o', linewidth=1)
    
plt.ylim(0,0.06)
plt.legend()
plt.xlabel('amplitude cut [a.u]')
plt.ylabel('Time Resolution [ns]')
plt.title('amplitude-cut time resolution')
plt.grid(axis='both', linestyle='dotted')
plt.draw()

# TIME RESOLUTION RF vs CFD
df_resT['resT_rf'] = (df_resT.sigma_rf**2-0.25*df_resT.sigma_mcp**2)**0.5
df_resT['resT_cfd'] = (df_resT.sigma_cfd**2-0.25*df_resT.sigma_mcp**2)**0.5
plt.figure()
df_resT.sort_values(by=['energy'])
plt.plot(df_resT.energy, df_resT.resT_rf, label='RF', marker='o', linewidth=1)
plt.plot(df_resT.energy, df_resT.resT_cfd, label='CFD', marker='x', linewidth=1)
plt.ylim(0,0.06)
plt.legend()
plt.xlabel('Energy [GeV]')
plt.ylabel('Time Resolution [ns]')
plt.title('Time Resolution: RF vs. CFD')
plt.grid(axis='both', linestyle='dotted')
plt.draw()  
plt.savefig('resT_RFvsCFD.pdf', format='pdf')
'''
# TIME RESOLUTION RF 
plt.figure()
df_resT_DESY = df_resT[df_resT.runs == 'allRuns']
df_resT_800V = df_resT[df_resT.runs == 'SPS2023allPos800V']
df_resT_800Vcenter = df_resT[df_resT.runs == 'SPS2023center800V']
df_resT_825V = df_resT[df_resT.runs == 'SPS2023allPos825V']
df_resT_825Vcenter = df_resT[df_resT.runs == 'SPS2023center825V']
df_resT_875V = df_resT[df_resT.runs == 'SPS2023center875V']
df_resT_3mcp = df_resT[df_resT.runs == 'SPS2023center685V3mcp']
# df_resT_3mcp500 = df_resT[df_resT.runs == 'SPS2023center685V3mcpLEDinhib500kHz']
# df_resT_3mcp1 = df_resT[df_resT.runs == 'SPS2023center685V3mcpLEDinhib1MHz']
# df_resT_3mcp5 = df_resT[df_resT.runs == 'SPS2023center685V3mcpLEDinhib5MHz']
# df_resT_3mcp20 = df_resT[df_resT.runs == 'SPS2023center685V3mcpLEDinhib20MHz']
#df_resT_3mcpAll = df_resT[df_resT.runs == 'SPS2023center685V3mcpLEDinhibAllRates']

#df_resT.sort_values(by=['energy'])
#print(df_resT_800V)
#print(df_resT_825V)
plt.errorbar(df_resT_DESY.energy, df_resT_DESY.resT_rf*1000, df_resT_DESY.resT_rf_err*1000, 
             label='2 MCPs, 875V', marker='o', markersize=3, linewidth=1, capsize=4, color='tab:blue')
plt.errorbar(df_resT_800V.energy, df_resT_800V.resT_rf*1000, df_resT_800V.resT_rf_err*1000, 
             label='2 MCPs, 800V', marker='o', markersize=3, linewidth=1, capsize=4, color='tab:orange')
# plt.errorbar(df_resT_800Vcenter.energy, df_resT_800Vcenter.resT_rf*1000, df_resT_800Vcenter.resT_rf_err*1000, 
#              label='2 MCPs, 800V, G4G5H4H5', marker='o', markersize=3, linewidth=1, capsize=4, color='tab:red')
plt.errorbar(df_resT_825V.energy, df_resT_825V.resT_rf*1000, df_resT_825V.resT_rf_err*1000, 
             label='2 MCPs, 825V', marker='o', markersize=3, linewidth=1, capsize=4, color='tab:green')
# plt.errorbar(df_resT_825Vcenter.energy, df_resT_825Vcenter.resT_rf*1000, df_resT_825Vcenter.resT_rf_err*1000, 
#              label='2 MCPs, 825V, G4G5H4H5', marker='o', markersize=3, linewidth=1, capsize=4, color='tab:cyan')
# plt.errorbar(df_resT_875V.energy, df_resT_875V.resT_rf*1000, df_resT_875V.resT_rf_err*1000, 
#              label='2 MCPs, 875V, G4G5H4H5', marker='o', markersize=6, linewidth=1, capsize=7, color='tab:green')
# plt.errorbar(df_resT_3mcp.energy, df_resT_3mcp.resT_rf*1000, df_resT_3mcp.resT_rf_err*1000, 
#              label='3 MCPs, 685V, G4G5H4H5', marker='o', markersize=6, linewidth=1, capsize=7, color='tab:purple')
# plt.errorbar(df_resT_3mcp500.energy, df_resT_3mcp500.resT_rf*1000, df_resT_3mcp500.resT_rf_err*1000, 
#              label='3 MCPs, 685 V, LED INHIBITED (0.5 MHz) ', marker='o', markersize=3, linewidth=1, capsize=4, color='tab:olive')
# plt.errorbar(df_resT_3mcp1.energy, df_resT_3mcp1.resT_rf*1000, df_resT_3mcp1.resT_rf_err*1000, 
#              label='3 MCPs, 685 V, LED INHIBITED (1 MHz) ', marker='o', markersize=3, linewidth=1, capsize=4, color='tab:pink')
# plt.errorbar(df_resT_3mcp5.energy, df_resT_3mcp5.resT_rf*1000, df_resT_3mcp5.resT_rf_err*1000, 
#              label='3 MCPs, 685 V, LED INHIBITED (5 MHz) ', marker='o', markersize=3, linewidth=1, capsize=4, color='tab:cyan')
# plt.errorbar(df_resT_3mcp20.energy, df_resT_3mcp20.resT_rf*1000, df_resT_3mcp20.resT_rf_err*1000, 
#              label='3 MCPs, 685 V, LED INHIBITED (20 MHz) ', marker='o', markersize=3, linewidth=1, capsize=4, color='tab:brown')
# plt.errorbar(df_resT_3mcpAll.energy, df_resT_3mcpAll.resT_rf*1000, df_resT_3mcpAll.resT_rf_err*1000, 
#              label='3 MCPs, 685 V, LED INHIBITED (all rates) ', marker='o', markersize=3, linewidth=1, capsize=4, color='tab:brown')

#plt.ylim(0,30)
plt.ylim(0,60)
plt.legend()
plt.xlabel('Energy [GeV]')
plt.ylabel('Time Resolution [ps]')
plt.title('Time Resolution with RF regressor')
plt.grid(axis='both', linestyle='dotted')
plt.draw()  
plt.savefig('../plots/resT_RF.pdf', format='pdf')
plt.xscale('log')
plt.draw()  
plt.savefig('../plots/resT_RF_logx.pdf', format='pdf')
exit(1)
# plt.show()


# Plot EFFICIENCY
plt.figure()
#max_cuts = ['0.001', '0.0015', '0.002', '0.0025', '0.003', '0.004', '0.010', '0.100']
#max_cuts = ['0.0140','0.0160','0.0180','0.0200','0.0220', '0.1000']
#max_cuts = ['0.0180','0.0160','0.0200']
#max_cuts = ['0.0150']
smax_cuts = ['0.0140']
for smax_cut in smax_cuts:
    tmp_df_800V = df_smax[(df_smax.smax_cuts == smax_cut) & (df_smax.runs == 'SPS2023allPos800V')]
    tmp_df_825V = df_smax[(df_smax.smax_cuts == smax_cut) & (df_smax.runs == 'SPS2023allPos825V')]
    tmp_df_800V = tmp_df_800V.sort_values(by=['energy'])
    tmp_df_825V = tmp_df_825V.sort_values(by=['energy'])
    plt.plot(tmp_df_800V.energy, tmp_df_800V.eff_smax, label=f'800 V', marker='o', linewidth=1)
    plt.plot(tmp_df_825V.energy, tmp_df_825V.eff_smax, label=f'825 V', marker='o', linewidth=1)
    
plt.ylim(0.95,1.05)
plt.legend(loc='best')
plt.xlabel('Energy [GeV]', ha='right', x=1)
plt.ylabel('Efficiency', ha='right', y=1)
plt.title('Amplitude-cut efficiency')
plt.minorticks_on()
plt.grid(axis='both', linestyle='dotted')
plt.draw()
plt.savefig('../plots/eff_smax.pdf', format='pdf')
# exit()

'''
energies = [1,2,3,4,5]
fout = ROOT.TFile.Open('../plots/stocazzo.root', 'recreate')
colors = [ROOT.kRed, ROOT.kOrange+2, ROOT.kGreen+2, ROOT.kCyan, ROOT.kBlue, ROOT.kViolet]
for run in ['allRuns', 'allRuns3mcp']:    
    for energy, color in zip(energies,colors):
        for n in [f'h_smax_{run}_{energy}', f'h_smax_zoom_{run}_{energy}', f'h_smax_zooom_{run}_{energy}']:
            if n not in d_h.keys(): continue
            h = d_h[n]
            h.Print('v')
            h.SetLineColor(color)
            h.SetLineWidth(2)
            h.SetStats(0)
    
        if f'h_smax_{run}_{energy}' not in d_h.keys(): continue
        _N = d_h[f'h_smax_{run}_{energy}'].Integral()
        d_h[f'h_smax_zoom_{run}_{energy}'].Scale(1.0/_N)
        d_h[f'h_smax_zooom_{run}_{energy}'].Scale(1.0/_N)
        d_h[f'h_smax_{run}_{energy}'].Scale(1.0/_N)
        
c_smax = ROOT.TCanvas('c_smax', 'c_smax')
c_smax.cd()
d_h['h_smax_allRuns_1'].Draw('hist')
d_h['h_smax_allRuns_2'].Draw('hist same')
d_h['h_smax_allRuns_3'].Draw('hist same')
d_h['h_smax_allRuns_4'].Draw('hist same')
d_h['h_smax_allRuns_5'].Draw('hist same')
d_h['h_smax_allRuns3mcp_1'].SetLineStyle(ROOT.kDotted)
d_h['h_smax_allRuns3mcp_3'].SetLineStyle(ROOT.kDotted)
d_h['h_smax_allRuns3mcp_5'].SetLineStyle(ROOT.kDotted)
d_h['h_smax_allRuns3mcp_1'].Draw('hist same')
d_h['h_smax_allRuns3mcp_3'].Draw('hist same')
d_h['h_smax_allRuns3mcp_5'].Draw('hist same')

c_smax.Draw()
c_smax.ls()
c_smax.SaveAs('../plots/c_smax.pdf')
fout.WriteTObject(c_smax, c_smax.GetName())

c_smax_zoom= ROOT.TCanvas('c_smax_zoom', 'c_smax_zoom')
c_smax_zoom.cd()
d_h['h_smax_zoom_allRuns_1'].Draw('hist')
d_h['h_smax_zoom_allRuns_2'].Draw('hist same')
d_h['h_smax_zoom_allRuns_3'].Draw('hist same')
d_h['h_smax_zoom_allRuns_4'].Draw('hist same')
d_h['h_smax_zoom_allRuns_5'].Draw('hist same')
d_h['h_smax_zoom_allRuns3mcp_1'].SetLineStyle(ROOT.kDotted)
d_h['h_smax_zoom_allRuns3mcp_3'].SetLineStyle(ROOT.kDotted)
d_h['h_smax_zoom_allRuns3mcp_5'].SetLineStyle(ROOT.kDotted)
d_h['h_smax_zoom_allRuns3mcp_1'].Draw('hist same')
d_h['h_smax_zoom_allRuns3mcp_3'].Draw('hist same')
d_h['h_smax_zoom_allRuns3mcp_5'].Draw('hist same')

c_smax_zoom.Draw()
c_smax_zoom.SaveAs('../plots/c_smax_zoom.pdf')
fout.WriteTObject(c_smax_zoom, c_smax_zoom.GetName())

c_smax_zooom = ROOT.TCanvas('c_smax_zooom', 'c_smax_zooom')
c_smax_zooom.cd()
d_h['h_smax_zooom_allRuns_1'].Draw('hist')
d_h['h_smax_zooom_allRuns_2'].Draw('hist same')
d_h['h_smax_zooom_allRuns_3'].Draw('hist same')
d_h['h_smax_zooom_allRuns_4'].Draw('hist same')
d_h['h_smax_zooom_allRuns_5'].Draw('hist same')
d_h['h_smax_zooom_allRuns3mcp_1'].SetLineStyle(ROOT.kDotted)
d_h['h_smax_zooom_allRuns3mcp_3'].SetLineStyle(ROOT.kDotted)
d_h['h_smax_zooom_allRuns3mcp_5'].SetLineStyle(ROOT.kDotted)
d_h['h_smax_zooom_allRuns3mcp_1'].Draw('hist same')
d_h['h_smax_zooom_allRuns3mcp_3'].Draw('hist same')
d_h['h_smax_zooom_allRuns3mcp_5'].Draw('hist same')
c_smax_zooom.Draw()
c_smax_zooom.SaveAs('../plots/c_smax_zooom.pdf')
fout.WriteTObject(c_smax_zooom, c_smax_zooom.GetName())
c_smax_zooom.Draw()
c_smax_zooom.SaveAs('../plots/c_smax_zooom_log.pdf')
'''

energies = [20,40,60,80,100]
x0 = -8.5
y0 = -13
for run in runs:
    for energy in energies:
        if skipEnergy(run,energy): continue
        df_tmp = df_resT_pos[(df_resT_pos.energy == energy) & (df_resT_pos.runs == run) ]
        print(df_tmp[['energy', 'x', 'y','resT_rf', 'resT_rf_err', 'runs']])
        plt.figure()
        hist_err, xbins_err, ybins_err, im_err  = plt.hist2d(df_tmp.x+x0, df_tmp.y+y0,bins=[3,3], range=[[-12.5+x0,12.5+x0],[-12.5+y0,12.5+y0]], weights=df_tmp.resT_rf_err*1000, vmin=0, vmax=50)
        hist, xbins, ybins, im  = plt.hist2d(df_tmp.x+x0, df_tmp.y+y0,bins=[3,3], range=[[-12.5+x0,12.5+x0],[-12.5+y0,12.5+y0]], weights=df_tmp.resT_rf*1000, vmin=10, vmax=25)
        plt.title(f'Energy: {energy} GeV')
        plt.colorbar()
        for i in range(len(ybins)-1):
            for j in range(len(xbins)-1):
                plt.text(xbins[j]+25/6, ybins[i]+25/6, f'${hist.T[i,j]:.1f} \pm {hist_err.T[i,j]:.1f}$', 
                        color="w", ha="center", va="center", fontweight="bold")
        plt.draw()
        plt.savefig(f'../plots/{run}_resT_pos_{energy}GeV.pdf', format='pdf')
        
        plt.figure()
        hist_err, xbins_err, ybins_err, im_err  = plt.hist2d(df_tmp.x+x0, df_tmp.y+y0,bins=[3,3], range=[[-12.5+x0,12.5+x0],[-12.5+y0,12.5+y0]], weights=df_tmp.rf_mu_err*1000, vmin=0, vmax=50)
        hist, xbins, ybins, im  = plt.hist2d(df_tmp.x+x0, df_tmp.y+y0,bins=[3,3], range=[[-12.5+x0,12.5+x0],[-12.5+y0,12.5+y0]], weights=df_tmp.rf_mu*1000, vmin=-5, vmax=5)
        plt.title(f'Energy: {energy} GeV')
        plt.colorbar()
        for i in range(len(ybins)-1):
            for j in range(len(xbins)-1):
                plt.text(xbins[j]+25/6, ybins[i]+25/6, f'${hist.T[i,j]:.1f} \pm {hist_err.T[i,j]:.1f}$', 
                        color="w", ha="center", va="center", fontweight="bold")
        plt.draw()
        plt.savefig(f'../plots/{run}_biasT_pos_{energy}GeV.pdf', format='pdf')


    pulls = []
    from itertools import chain
    for energy in energies:
        if skipEnergy(run,energy): continue
        print('energy', energy, df_resT[df_resT.energy == energy].resT_rf.values)
        avg_resT = df_resT[(df_resT.energy == energy) & (df_resT.runs == run)].resT_rf.values[0] 
        avg_resT_err = df_resT[(df_resT.energy == energy) & (df_resT.runs == run)].resT_rf_err.values[0] 
        df_tmp = df_resT_pos[(df_resT_pos.energy == energy) & (df_resT_pos.runs == run)]
        df_tmp.eval(f'n_sigmas = (resT_rf-{avg_resT})/(resT_rf_err**2-{avg_resT_err}**2)**0.5', inplace=True)
        plt.figure()
        hist, xbins, ybins, im  = plt.hist2d(df_tmp.x+x0, df_tmp.y+y0,bins=[3,3], range=[[-12.5+x0,12.5+x0],[-12.5+y0,12.5+y0]], weights=df_tmp.n_sigmas, 
                                            vmin=-5, vmax=5, cmap=matplotlib.cm.coolwarm)
        pulls += list(chain.from_iterable(hist))
        plt.title(f'Energy: {energy} GeV')
        plt.colorbar()
        for i in range(len(ybins)-1):
            for j in range(len(xbins)-1):
                plt.text(xbins[j]+25/6, ybins[i]+25/6, f'${hist.T[i,j]:.1f}$', 
                        color="w", ha="center", va="center", fontweight="bold")

        plt.draw()
        plt.savefig(f'../plots/{run}_sigma_resT_pos_{energy}GeV.pdf', format='pdf')

    plt.figure()

    # for n in df_resT_pos[(df_resT_pos.energy==100) & (df_resT_pos.runs==run)].n.values:
    #     df_tmp = df_resT_pos[(df_resT_pos.n == n) & (df_resT_pos.runs==run)]
    #     plt.errorbar(df_tmp.energy, df_tmp.resT_rf*1000,df_tmp.resT_rf_err*1000, capsize=2, label=n)

    # plt.ylim(10,25)
    # plt.legend()
    # plt.draw()

    # plt.figure()
    # plt.hist(pulls, bins=7, range=(-9,9))
    # plt.draw()
    #fout.Close()
    #plt.show()


