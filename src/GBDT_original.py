verbose=1
learning_rate = 0.1
max_depth = 50
max_leaf_nodes = 200
max_iter = 500
max_bins = 255
min_samples_leaf = 20
loss = 'squared_error'

radius = 7
maxmcp = 0.05

beam_selection = [
  '((run==251 or run==173 or run==172 or run==170 or run==134 or run==20 or run==37 or run==46 or run==55 or run==65 or run==82 or run==86 or run==95 or run==104 or run==113) and (xwc0+8.5)**2+(ywc0+13.0)**2<radius**2)', #G4G5H4H5
  '((run==21 or run==38 or run==47 or run==56 or run==66 or run==81 or run==87 or run==96 or run==105 or run==114) and (xwc0+8.5)**2+(ywc0+0.5)**2<radius**2)', #G4G5
  '((run==23 or run==39 or run==48 or run==57 or run==67 or run==80 or run==88 or run==97 or run==106 or run==115) and (xwc0+21.0)**2+(ywc0+0.5)**2<radius**2)', #G5
  '((run==24 or run==40 or run==49 or run==58 or run==68 or run==79 or run==89 or run==98 or run==107 or run==116) and (xwc0+21.0)**2+(ywc0+13.0)**2<radius**2)', #G5H5
  '((run==25 or run==41 or run==50 or run==59 or run==69 or run==78 or run==90 or run==99 or run==108 or run==117) and (xwc0+21.0)**2+(ywc0+25.5)**2<radius**2)', #H5
  '((run==26 or run==42 or run==51 or run==60 or run==70 or run==77 or run==91 or run==100 or run==109 or run==118) and (xwc0+8.5)**2+(ywc0+25.5)**2<radius**2)', #H4H5
  '((run==27 or run==43 or run==52 or run==61 or run==71 or run==76 or run==92 or run==101 or run==110 or run==119) and (xwc0-4.0)**2+(ywc0+25.5)**2<radius**2)', #H4
  '((run==28 or run==44 or run==53 or run==62 or run==72 or run==75 or run==93 or run==102 or run==111 or run==120) and (xwc0-4.0)**2+(ywc0+13.0)**2<radius**2)', #G4H4
  '((run==29 or run==45 or run==54 or run==64 or run==73 or run==74 or run==94 or run==103 or run==112 or run==121) and (xwc0-4.0)**2+(ywc0+0.5)**2<radius**2)' #G4
]

mcp_selection = [
  'maxmcp0 > maxmcp',
  'maxmcp0 < 0.85',
  'maxmcp1 > maxmcp',
  'maxmcp1 < 0.85'
]

cleanup_selection = [
  'xwc0>-21.0',
  'xwc0<4.0',
  'ywc0>-25.5',
  'ywc0<-0.5',
  'abs(xwc1-xwc0-2.39)<1',
  'abs(ywc1-ywc0+0.217)<1'
]

lappd_selection = []
lappd_selection += ['max%d < 0.85'%(i) for i in range(0,4) ]


datadir = "/storage/gpfs_data/local/lhcb/users/vagnoni/2023_july/spacal_w_LAPPD_DIG_SPS/"

import numpy as np
import pandas as pd
import uproot as upr
import pickle
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-o','--outFile', type = str, dest = 'outFile', default = '')
parser.add_argument('-r','--runs', nargs='+', dest = 'runs', default = [])
parser.add_argument('-v','--variables', nargs='+', dest = 'variables', default = [])
parser.add_argument('-t','--threads', type = str, dest = 'threads', default = '0')
args = parser.parse_args()

if(args.threads != '0'):
  os.environ["OMP_NUM_THREADS"] = args.threads
  n_jobs = int(args.threads)

import warnings
warnings.filterwarnings('ignore')

## t[16][11]/D:tdown[16][10]/D:max[16]/D:min[16]/D:area[16]/D:xwc[3]/D:ywc[3]/D:tmcp[11]/D:tmcpd[11]/D:maxmcp[2]/D:trun/D:imax[4]/I:jmax[4]/I:entry/I

dtype = np.dtype([("t",     ">f8", (16, 11)),
                  ("tdown", ">f8", (16, 10)),
                  ("max",   ">f8", 16),
                  ("min",   ">f8", 16),
                  ("area",  ">f8", 16),
                  ("xwc",   ">f8", 3),
                  ("ywc",   ">f8", 3),
                  ("tmcp",  ">f8", 11),
                  ("tmcpd", ">f8", 11),
                  ("maxmcp",">f8", 2),
                  ("ttrig", ">f8", 4),
                  ("trun",  ">f8", 1),
                  ("imax",  ">i4", 4),
                  ("jmax",  ">i4", 4),
                  ("entry", ">i4", 1) ])
interpretation = upr.AsDtype(dtype)

def read_file(run):
  print("Reading run %s"%run)
  T = upr.open('%s/mergedana_%s.root'%(datadir,run))
  data = T['T'].arrays({'data':interpretation},library='np')['data']
  data = {varname: np.array([d[varname] for d in data]) for varname in dtype.names}

  dframe = pd.DataFrame(np.c_[ data['t'][:, 10:14, 1],
                               data['t'][:, 10:14, 2],
                               data['t'][:, 10:14, 3],
                               data['t'][:, 10:14, 4],
                               data['t'][:, 10:14, 5],
                               data['t'][:, 10:14, 6],
                               data['t'][:, 10:14, 7],
                               data['t'][:, 10:14, 8],
                               data['t'][:, 10:14, 9],
                               data['max'][:, 10:14],
                               data['maxmcp'][:,0:2],
                               data['xwc'][:, 0:3],
                               data['ywc'][:, 0:3],
                               data['tmcp'][:, 3],
                               data['tmcpd'][:, 3] ],
                        columns='t0_1,t1_1,t2_1,t3_1,t0_2,t1_2,t2_2,t3_2,t0_3,t1_3,t2_3,t3_3,t0_4,t1_4,t2_4,t3_4,t0_5,t1_5,t2_5,t3_5,t0_6,t1_6,t2_6,t3_6,t0_7,t1_7,t2_7,t3_7,t0_8,t1_8,t2_8,t3_8,t0_9,t1_9,t2_9,t3_9,max0,max1,max2,max3,maxmcp0,maxmcp1,xwc0,xwc1,xwc2,ywc0,ywc1,ywc2,tmcp3,tmcpd3'.split(','))

  dframe['run'] = int(run)
  dframe['maxmcp'] = maxmcp
  dframe['radius'] = radius
  dframe.query('('+' or '.join(beam_selection)+') and'+
               '('+' and '.join(mcp_selection)+') and'+
               '('+' and '.join(cleanup_selection)+') and'+
               '('+' and '.join(lappd_selection)+')' , inplace=True)
  return dframe

############ MAIN
dfList = []
from multiprocessing import Pool
pool = Pool(len(args.runs))

for dframe in pool.imap_unordered(read_file, args.runs):
  dfList.append(dframe)

df = pd.concat(dfList)

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(value=-999,inplace=True)

#X = df[['t0','t1','t2','t3','max0','max1','max2','max3']].values
X = df[args.variables].values
y = df['tmcp3'].values

from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.1)

print("Starting regressor")
#from sklearn.ensemble import HistGradientBoostingRegressor as regressor
from sklearn.ensemble import RandomForestRegressor as regressor

#regr = regressor(verbose=1, n_jobs=n_jobs)
regr = regressor(verbose=1, n_jobs=n_jobs)

"""
regr = regressor(verbose = verbose,
           learning_rate = learning_rate,
           max_depth = max_depth,
           max_leaf_nodes = max_leaf_nodes,
           max_iter = max_iter,
           min_samples_leaf = min_samples_leaf,
           loss = loss)
"""

regr.fit(X_train, y_train)


"""
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance

result = permutation_importance(
    regr, X_val, y_val, n_repeats=10, random_state=42
)

sorted_importances_idx = result.importances_mean.argsort()
importances = pd.DataFrame(
    result.importances[sorted_importances_idx].T,
    columns=df[args.variables].columns[sorted_importances_idx],
)
ax = importances.plot.box(vert=False, whis=10)
ax.set_title("Permutation Importances (test set)")
ax.axvline(x=0, color="k", linestyle="--")
ax.set_xlabel("Decrease in accuracy score")
ax.figure.tight_layout()
plt.show()
"""

y_hat_train = regr.predict(X_train)
y_hat_val = regr.predict(X_val)

outFile = open('output_train%s.dat'%(args.outFile),'w')
for a,b,c in zip(y_hat_train - y_train, X_train[:,0], X_train[:,1]):
  outFile.write('%lf %lf %lf\n'%(a,b,c))
outFile.close()

outFile = open('output_eval%s.dat'%(args.outFile),'w')
for a,b,c in zip(y_hat_val - y_val, X_val[:,0], X_val[:,1]):
  outFile.write('%lf %lf %lf\n'%(a,b,c))
outFile.close()

outFile = open('output_data%s.dat'%(args.outFile),'w')
for a,b,c,d,e,f,g in zip(df['run'].values,
                         df['xwc0'].values,
                         df['ywc0'].values,
                         df['max0'].values,
                         df['max1'].values,
                         df['max2'].values,
                         df['max3'].values) :
  outFile.write('%d %lf %lf %lf %lf %lf %lf\n'%(a,b,c,d,e,f,g))
outFile.close()

outFile = open('output_target%s.dat'%(args.outFile),'w')
for a,b,c in zip(df['tmcpd3'].values, df['xwc2'].values, df['ywc2'].values):
  outFile.write('%lf %lf %lf\n'%(a,b,c))
outFile.close()

#outFile = open('bdt%s.pkl'%(args.outFile),'wb')
#pickle.dump(bdt,outFile)
#outFile.close()
