import os
inputdir = '../out'
listDir = [(name,os.path.abspath(inputdir+'/'+name)) for name in os.listdir(inputdir+'/') if os.path.isdir(inputdir+'/'+name)]
list_resTrain = []
list_resTest = []
list_Ntrees = []
list_maxLeaves = []
import pandas
df = pandas.DataFrame(columns=['energy', 'Ntrees', 'maxLeaves', 'bootstrap', 
                               'maxSamples', 'maxFeatures', 'resTrain', 'resTest'])
for n,f in listDir:
    print(n,f)
#    if 'baseline' in n: continue
    if 'sqrt' not in n: continue
    if '5.8' in n: continue
    energy = int(n.split('GeV')[0].split('_')[1])
    Ntrees = int(n.split('GeV')[1].split('_')[1])
    maxLeaves = int(n.split('GeV')[1].split('_')[2])
    bootstrap = n.split('GeV')[1].split('_')[3]
    maxSamples = n.split('GeV')[1].split('_')[4]
    maxFeatures = n.split('GeV')[1].split('_')[5]
    #print(Ntrees, maxLeaves)
    if Ntrees >= 10000 and maxLeaves == 0 : continue
    if maxLeaves >= 100000000: continue
                    
    fres = open(f+'/resolution.txt')
    lines = fres.read().split('\n')[:-1]
    #print(lines)
    fres.close()
    if len(lines)!=5: continue
    resTrain= float(lines[1].split(' ')[2])
    resTest = float(lines[4].split(' ')[3])
    
    new_row = [
        energy,
        Ntrees, 
        maxLeaves if int(maxLeaves) != 0 else int(1e9),
        bootstrap, 
        maxSamples, 
        maxFeatures, 
        resTrain, 
        resTest
    ]
    df.loc[len(df.index)] = new_row
df = df.sort_values(by=['energy', 'Ntrees', 'maxLeaves', 'maxFeatures','bootstrap', 'maxSamples'],ignore_index=True)
print(df)
#############################################################
#############################################################
#############################################################

import matplotlib.pyplot as plt
from itertools import product
import numpy as np
toPlotNtrees = [20, 100, 500]
toPlotMaxLeaves = [1000, 10000, 100000, 1000000000]
#toPlotMaxLeaves = [1000, 10000, 100000]
#toPlotMaxLeaves = [100000]
#toPlotEnergies = [1,2,3,4,5]
toPlotEnergies = [20,40,60,80,100]
toPlotMaxFeatures = ['sqrt']
toPlotMaxSamples = ['-1.0']
toPlotBootstrap = ['1']

plt.rc('font', family='serif', size=12)
#plt.rc('text', usetex=True)
plt.rcParams['axes.linewidth']=1.3
plt.rcParams['xtick.major.width']=1
plt.rcParams['ytick.major.width']=1
plt.rcParams['xtick.minor.width']=1
plt.rcParams['ytick.minor.width']=1
plt.rcParams['xtick.major.size']=10
plt.rcParams['ytick.major.size']=10
plt.rcParams['xtick.minor.size']=5
plt.rcParams['ytick.minor.size']=5

for maxFeatures, bootstrap, maxSamples in product(toPlotMaxFeatures, toPlotBootstrap, toPlotMaxSamples):
    for energy in toPlotEnergies:
        icolor = 0
        plt.figure()
        Ncolors = len(toPlotNtrees)
        color = iter(plt.cm.tab10(np.linspace(0, 1, 10)))    
        for targetNtrees in toPlotNtrees:
            print(energy, targetNtrees, bootstrap, maxFeatures, maxSamples)
            tmpdf = df[(df.energy == energy) & (df.Ntrees == targetNtrees) & (df.bootstrap == bootstrap) & (df.maxFeatures == maxFeatures) & (df.maxSamples == maxSamples)]
            print(tmpdf)
            c = next(color) 
            plt.plot(tmpdf.maxLeaves, tmpdf.resTest,  marker='o', linestyle='solid', color=c, label=f'Ntrees: {targetNtrees}')
#            plt.plot(tmpdf.maxLeaves, tmpdf.resTrain, marker='+', linestyle='dotted', color=c)
            icolor += 1
        title = f'Energy: {energy} GeV, maxFeatures: {maxFeatures}'
        if bootstrap == '1':
            title += ', bootstrap: ON'
        else:
            title += f', bootstrap: OFF, maxSamples: {maxSamples}'
        plt.title(title)
        plt.xscale('log')
        plt.xlabel('maxLeaves')
        plt.ylabel('Time Resolution [ps]')
        plt.legend()
        plt.grid(color='grey', linestyle='dotted', linewidth=1, axis='both')
    
        plt.ylim([0,100])    
        plt.draw()
    
    icolor = 0
    plt.figure() 
    
    Ncolors = len(toPlotMaxLeaves)*len([100])
    color = iter(plt.cm.gist_rainbow(np.linspace(0, 1, Ncolors)))    
    for maxLeaves, targetNtrees in product(toPlotMaxLeaves, [100]):
        print(energy, targetNtrees, bootstrap, maxFeatures, maxSamples)
        tmpdf = df[(df.maxLeaves == maxLeaves) & (df.Ntrees == targetNtrees) & (df.bootstrap == bootstrap) & (df.maxFeatures == maxFeatures) & (df.maxSamples == maxSamples)]
        print(tmpdf)
        c = next(color)
        tmplabel = f'maxLaves: {maxLeaves:.0e}, Ntrees: {targetNtrees}'
        plt.plot(tmpdf.energy, tmpdf.resTest,  marker='o', linestyle='solid', color=c, label=tmplabel)
#        plt.plot(tmpdf.energy, tmpdf.resTrain, marker='+', linestyle='dotted', color=c)
        icolor += 1
    title = f'maxFeatures: {maxFeatures}'
    if bootstrap == '1':
        title += ', bootstrap: ON'
    else:
        title += f', bootstrap: OFF, maxSamples: {maxSamples}'
    plt.title(title)
    
    plt.legend()
    plt.grid(color='grey', linestyle='dotted', linewidth=1, axis='both')
    plt.xlabel('Energy [GeV]')
    plt.ylabel('Time Resolution [ps]')
    plt.ylim([0,100])    
    plt.draw()
    
plt.show()
