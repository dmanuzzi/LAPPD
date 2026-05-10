import pandas
import pickle

list_df_resXY = []

#for E in [1,2,3,4,5]:
for E in [20,40,60,80,100]:
    # for opt in ['_baseline', '_wideRange']:
    #     for run in ['allRuns', 'allRuns3mcp']:    
    for opt in ['_baseline']:
        #for run in ['SPS2023allPos800V', 'SPS2023allPos825V']:    
        for run in ['SPS2023allPos800V']:    
            if run == 'allRuns3mcp' and (E not in [3,5]): continue
            dir = f'../out_position/{run}_{E}GeV_100_0_1_-1.0_sqrt{opt}'
            tmp_dict = {}        
            with open(f'{dir}/resXY.pickle', 'rb') as handle:
                tmp_dict = pickle.load(handle)
            #print(tmp_dict)    
            tmp_df = pandas.DataFrame(tmp_dict)
            tmp_df = tmp_df.assign(runs = lambda x: run)
            #print(tmp_df)
            list_df_resXY.append(tmp_df.copy())

df_resXY = pandas.concat(list_df_resXY, ignore_index=True)
from matplotlib import pyplot as plt

df_resXY = df_resXY.astype({'config' : 'str'})
for i, row in df_resXY.iterrows():
    energy = row.config.split('GeV')[0].split('_')[-1]
    df_resXY.at[i, 'energy'] = energy
    df_resXY.at[i, 'isBaseline'] = ('baseline' in row.config)
    #df_resXY.at[i, 'isWideRange'] = ('wideRange' in row.config)
##############################################################
##############################################################
##############################################################
##############################################################
df_resXY_baseline = df_resXY[(df_resXY.isBaseline) & (df_resXY.runs =='SPS2023allPos800V')]
#df_resXY_wideRange = df_resXY[(df_resXY.isWideRange) & (df_resXY.runs =='allRuns')]

df_resXY_baseline_3mcp = df_resXY[(df_resXY.isBaseline) & (df_resXY.runs =='allRuns3mcp')]
#df_resXY_wideRange_3mcp = df_resXY[(df_resXY.isWideRange) & (df_resXY.runs =='allRuns3mcp')]

plt.figure()
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_x_reducedX, label='Reduced x range', marker='o', linewidth=2)
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_x, label='Baseline x range', marker='x', linewidth=1, linestyle='dotted', color=plt.gca().lines[-1].get_color())
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_y_reducedy, label='Reduced y range', marker='o', linewidth=2)
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_y, label='Baseline y range', marker='x', linewidth=1, linestyle='dotted', color=plt.gca().lines[-1].get_color())
# plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_x_reduced, label='x reduced', marker='o', linewidth=1)
# plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_y_reduced, label='y reduced', marker='o', linewidth=1)
plt.ylim(0,4)
plt.legend()
plt.xlabel('Energy [GeV]')
plt.ylabel('Position Resolution [mm]')
plt.title('Position Resolution with RF regressor')
plt.grid(axis='both', linestyle='dotted')
plt.draw()  
plt.savefig('resXY_ReducedVsBaseline.pdf', format='pdf')

plt.figure()
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_x_reducedX, label='x coordinate', marker='o', linewidth=2)
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_y_reducedy, label='y coordinate', marker='o', linewidth=2)
plt.ylim(0,4)
plt.legend()
plt.xlabel('Energy [GeV]')
plt.ylabel('Position Resolution [mm]')
plt.title('Position Resolution with RF regressor')
plt.grid(axis='both', linestyle='dotted')
plt.draw()  
plt.savefig('resXY_ReducedRange.pdf', format='pdf')

plt.figure()
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_x_reducedX, label='x coord.; Train: Baseline, Test: Reduced', marker='o', linewidth=2)
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_x, label='x coord.; Train: Baseline, Test: Baseline', marker='x', linewidth=1, linestyle='dotted', color=plt.gca().lines[-1].get_color())
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_y_reducedy, label='y coord.; Train: Baseline, Test: Reduced', marker='o', linewidth=2)
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_y, label='y coord.; Train: Baseline, Test: Baseline', marker='x', linewidth=1, linestyle='dotted', color=plt.gca().lines[-1].get_color())
# plt.plot(df_resXY_wideRange.energy, df_resXY_wideRange.sigma_x_reducedX, label='x coord.; Train: Wide, Test: Reduced', marker='o', linewidth=2)
# plt.plot(df_resXY_wideRange.energy, df_resXY_wideRange.sigma_x_baselineX, label='x coord.; Train: Wide, Test: Baseline', marker='x', linewidth=1, linestyle='dotted', color=plt.gca().lines[-1].get_color())
# plt.plot(df_resXY_wideRange.energy, df_resXY_wideRange.sigma_y_reducedy, label='y coord.; Train: Wide, Test: Reduced', marker='o', linewidth=2)
# plt.plot(df_resXY_wideRange.energy, df_resXY_wideRange.sigma_y_baseliney, label='y coord.; Train: Wide, Test: Baseline', marker='x', linewidth=1, linestyle='dotted', color=plt.gca().lines[-1].get_color())

plt.ylim(0,4)
plt.legend()
plt.xlabel('Energy [GeV]')
plt.ylabel('Position Resolution [mm]')
plt.title('Position Resolution with RF regressor')
plt.grid(axis='both', linestyle='dotted')
plt.draw()  
plt.savefig('resXY_Train_WideVsBaseline.pdf', format='pdf')

plt.figure()
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_x_reducedX, label='x coord., 2 MCPs ', marker='o', linewidth=2)
#plt.plot(df_resXY_baseline_3mcp.energy, df_resXY_baseline_3mcp.sigma_x_reducedX, label='x coord., 3 MCPs', marker='x', linewidth=2, linestyle='dotted', color=plt.gca().lines[-1].get_color())
plt.plot(df_resXY_baseline.energy, df_resXY_baseline.sigma_y_reducedy, label='y coord., 2 MCPs', marker='o', linewidth=2)
#plt.plot(df_resXY_baseline_3mcp.energy, df_resXY_baseline_3mcp.sigma_y_reducedy, label='y coord., 3 MCPs', marker='x', linewidth=2, linestyle='dotted', color=plt.gca().lines[-1].get_color())
plt.ylim(0,4)
plt.legend()
plt.xlabel('Energy [GeV]')
plt.ylabel('Position Resolution [mm]')
plt.title('Position Resolution with RF regressor')
plt.grid(axis='both', linestyle='dotted')
plt.draw()  
plt.savefig('resXY_2vs3MCPs.pdf', format='pdf')


#plt.show()


