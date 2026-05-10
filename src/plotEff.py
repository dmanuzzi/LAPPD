import os
import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

job_tag = 'test3'
#runs = [58,59,45,88,74]
nchannels = 4
#sigmaCuts = [1,2,3,5,20,50]
sigmaCuts = [1,2,3,5]
energy_run = {
    5 : [48,47,46,41,45,44,43,42,40],
    4 : [70,71,72,73,74,75,76,77,78],
    3 : [49,50,52,53,58,57,56,55,54],
    2 : [83,84,85,86,88,89,90,82,79],
    1 : [69,68,67,64,59,60,61,62,63],
    5.8 : [80]
}
ch_name = {
    0 : 'G4',
    1 : 'G5',
    2 : 'H4',
    3 : 'H5',
}

position_run = {
    'H4'       : [48,70,49,83,69],	
    'G4H4'     : [47,71,50,84,68],
    'G4'       : [46,72,52,85,67],
    'G4G5'     : [41,73,53,86,64],
    'G5'       : [45,74,58,88,59],
    'G5H5'     : [44,75,57,89,60],
    'H5'       : [43,76,56,90,61],
    'H4H5'     : [42,77,55,82,62],
    'G4G5H4H5' : [40,78,54,79,63,80],
}

df = pd.DataFrame(columns=['run', 'position', 'energy', 'nch', 'Ntot', 'Npass', 'sigmaCut', 'Nfinal'])
dfRes = pd.DataFrame(columns=['run', 'position', 'energy', 'nch',  'totEntries', 'selEntries', 'bias', 'resT',])
for position in position_run.keys():
    runs = position_run[position]
    for run in runs:
        myfile = open(f'../out_getEff/run{run}{job_tag}/output_getEff.txt')
        allInfo = myfile.read()
        effInfo = allInfo.split('totEntries')
        resLines = effInfo[0].split('\n')[:-1] 
        effLines = effInfo[1].split('\n')[:-1]
        Ntot = float(effLines[0].replace(' ', ''))
        Npass = float(effLines[1].split(' ')[1])
        nch = 0
        #position = str([i for i in position_run.keys() if run in position_run[i]][0])
        energy = float([i for i in energy_run.keys() if run in energy_run[i]][0])
        sigmaCut = 0
        Nfinal = 0 
        eff = 0
        for effLine in effLines:
            words = effLine.split(' ')
            if len(words) != 4: continue
            nch = int(words[0])
            sigmaCut = float(words[1])
            Nfinal = float(words[2])
            eff = float(words[3])
            new_row = [
                run, position, energy, nch, Ntot, Npass, sigmaCut, Nfinal
            ]    
            df.loc[len(df.index)] = new_row
        for resLine in resLines:
            words = resLine.split(' ')
            #print(words)
            if len(words) != 4: continue
            nch = int(words[1])
            bias = float(words[2])
            resT = float(words[3])
            new_row = [
                run, position, energy, nch, Ntot, Npass, bias, resT
            ]
            dfRes.loc[len(dfRes.index)] = new_row
        myfile.close()

print(dfRes)
print(df)
df.eval('effSel = Npass/Ntot', inplace=True)
df.eval('effFinal = Nfinal/Npass', inplace=True)
df.eval('effTot = Nfinal/Ntot', inplace=True)
dfRes.eval('resT_ps = resT*1000', inplace=True)
#for position in position_run.keys():
for position in ['G4', 'G4G5', 'G4G5H4H5']:
    # for sigmaCut in sigmaCuts:
    #     plt.figure()
    #     for n in list(range(0,nchannels)):
    #         tmpdf = df[(df.nch == n) & (df.sigmaCut == sigmaCut) & (df.position == position)]
    #         tmpdf = tmpdf.sort_values(by=['energy'])
    #         plt.plot(tmpdf.energy, tmpdf.effFinal, label=f'nch: {n}', marker='o')
            
    #     plt.legend()
    #     plt.ylim(0,1)
    #     plt.xlabel('Energy [GeV]')
    #     plt.ylabel('Efficiency')
    #     plt.grid(linestyle='dotted')
    #     plt.title(f'Efficiency, position {position}, sigma<{sigmaCut}')

    for n in list(range(0,nchannels)):
        plt.figure()
        for sigmaCut in sigmaCuts:
            tmpdf = df[(df.nch == n) & (df.sigmaCut == sigmaCut) & (df.position == position)]
            tmpdf = tmpdf.sort_values(by=['energy'])
            #print(tmpdf)
            plt.plot(tmpdf.energy, tmpdf.effFinal, label=f'<{sigmaCut:.0f} sigma', marker='o')
            
        plt.legend()
        plt.ylim(0,1)
        plt.xlabel('Energy [GeV]')
        plt.ylabel('Efficiency')
        plt.grid(linestyle='dotted')
        plt.title(f'Efficiency, position {position}, nch: {ch_name[n]}')
        plt.savefig(f'../plot_eff/eff_{position}_nch{n}.pdf', format='pdf')
        plt.close()


for position in ['G4', 'G4G5', 
                 'G5', 'G5H5',
                 'H5', 'H4H5',
                 'H4', 'G4H4',
                 'G4G5H4H5']:
    plt.figure()
    for n in list(range(0,nchannels)):
        tmpdf = dfRes[(dfRes.nch == n) & (dfRes.position == position)]
        #print(tmpdf)
        tmpdf = tmpdf.sort_values(by=['energy'])
        plt.plot(tmpdf.energy, tmpdf.resT_ps, label=f'nch: {ch_name[n]}', marker='o')
    plt.legend()
    plt.ylim(0,100)
    plt.xlabel('Energy [GeV]')
    plt.ylabel('Time Resolution [ps]')
    plt.grid(linestyle='dotted')
    plt.title(f'Time Resolution, position {position}')
    plt.savefig(f'../plot_eff/res_{position}.pdf', format='pdf')
    plt.close()

#plt.show()

