verbose=1
loss = 'mse'
#loss = 'mae'
radius = 7
maxmcp = 0.05


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

energy_run = {
    5 : [48,47,46,41,45,44,43,42,40],
    4 : [70,71,72,73,74,75,76,77,78],
    3 : [49,50,52,53,58,57,56,55,54],
    2 : [83,84,85,86,88,89,90,82,79],
    1 : [69,68,67,64,59,60,61,62,63],
    5.8 : [80]
}


beam_selection = [
  '((run==0 or run==16 or run==23 or run==25 or run==26 or run==27 or run==28 or run==29 or run==30 or run==31 or run==32 or run==33 or run==34 or run==35 or run==36 or run==37 or run==38 or run==39 or run==40 or run==54 or run==78 or run==80 or run==63 or run==79) and (xwc2-3.7)*(xwc2-3.7)+(ywc2+9.5)*(ywc2+9.5)<radius*radius)',
  '((run==1 or run==17 or run==41 or run==53 or run==73 or run==64 or run==86) and (xwc2-3.7)*(xwc2-3.7)+(ywc2-3.0)*(ywc2-3.0)<radius*radius)',
  '((run==3 or run==15 or run==42 or run==55 or run==77 or run==62 or run==82) and (xwc2-3.7)*(xwc2-3.7)+(ywc2+22.0)*(ywc2+22.0)<radius*radius)', 
  '((run==4 or run==20 or run==43 or run==56 or run==76 or run==61 or run==90) and (xwc2-16.2)*(xwc2-16.2)+(ywc2+22.0)*(ywc2+22.0)<radius*radius)',
  '((run==7 or run==18 or run==45 or run==58 or run==74 or run==59 or run==88) and (xwc2-16.2)*(xwc2-16.2)+(ywc2-3.0)*(ywc2-3.0)<radius*radius)',
  '((run==8 or run==19 or run==44 or run==57 or run==75 or run==60 or run==89) and (xwc2-16.2)*(xwc2-16.2)+(ywc2+9.5)*(ywc2+9.5)<radius*radius)',
  '((run==9 or run==13 or run==47 or run==50 or run==71 or run==68 or run==84) and (xwc2+8.8)*(xwc2+8.8)+(ywc2+9.5)*(ywc2+9.5)<radius*radius)',
  '((run==10 or run==14 or run==48 or run==49 or run==70 or run==69 or run==83) and (xwc2+8.8)*(xwc2+8.8)+(ywc2+22.0)*(ywc2+22.0)<radius*radius)',
  '((run==11 or run==12 or run==46 or run==52 or run==72 or run==67 or run==85) and (xwc2+8.8)*(xwc2+8.8)+(ywc2-3.0)*(ywc2-3.0)<radius*radius)'
]

mcp_selection = [
  'maxmcp0 > maxmcp',
  'maxmcp0 < 0.85',
  'maxmcp1 > maxmcp',
  'maxmcp1 < 0.85'
]

cleanup_selection = [
  'xwc2>-8.8-12.5',
  'xwc2<16.2+12.5',
  'ywc2>-22-12.5',
  'ywc2<3+12.5',
  'abs(xwc2-xwc1+0.2)<1',
  'abs(ywc2-ywc1-1.5)<1.5'
]

lappd_selection = []
lappd_selection += ['max%d < 0.85'%(i) for i in range(0,4) ]


datadir = "/storage/gpfs_data/local/lhcb/users/vagnoni/2022_december/"

import numpy as np
import pandas as pd
import uproot as upr
import pickle
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-od','--outDir', type = str, dest = 'outDir', default = './')
parser.add_argument('-o','--outFile', type = str, dest = 'outFile', default = '')
parser.add_argument('-r','--runs', nargs='+', dest = 'runs', default = [])
parser.add_argument('-v','--variables', nargs='+', dest = 'variables', default = [])
parser.add_argument('-t','--threads', type = str, dest = 'threads', default = '0')
parser.add_argument('-nt','--Ntrees', type = int, dest = 'Ntrees', default = '100')
parser.add_argument('-nl','--maxLeaves', type = int, dest = 'maxLeaves', default = None)
parser.add_argument('-ms','--maxSamples', type = float, dest = 'maxSamples', default = -1)
parser.add_argument('-b','--bootstrap', type = int, dest = 'bootstrap', default = True)
parser.add_argument('-mf','--maxFeatures', type = str, dest = 'maxFeatures', default = '0')

args = parser.parse_args()

n_estimators = args.Ntrees if args.Ntrees!=0 else 100 
max_leaf_nodes = args.maxLeaves if args.maxLeaves!= 0 else None
max_samples = args.maxSamples if args.maxSamples >= 0 else None
bootstrap = (args.bootstrap != 0)
max_features = args.maxFeatures if args.maxFeatures != '0' else 1
outDir = args.outDir
print("max_samples =", max_samples)

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

  dframe = pd.DataFrame(np.c_[ data['t'][:, 0:4, 1],
                               data['t'][:, 0:4, 2],
                               data['t'][:, 0:4, 3],
                               data['t'][:, 0:4, 4],
                               data['t'][:, 0:4, 5],
                               data['t'][:, 0:4, 6],
                               data['t'][:, 0:4, 7],
                               data['t'][:, 0:4, 8],
                               data['t'][:, 0:4, 9],
                               data['max'][:, 0:4],
                               data['maxmcp'][:,0:2],
                               data['xwc'][:, 1:3],
                               data['ywc'][:, 1:3],
                               data['tmcp'][:, 3],
                               data['tmcpd'][:, 3] ],
                        columns='t0_1,t1_1,t2_1,t3_1,t0_2,t1_2,t2_2,t3_2,t0_3,t1_3,t2_3,t3_3,t0_4,t1_4,t2_4,t3_4,t0_5,t1_5,t2_5,t3_5,t0_6,t1_6,t2_6,t3_6,t0_7,t1_7,t2_7,t3_7,t0_8,t1_8,t2_8,t3_8,t0_9,t1_9,t2_9,t3_9,max0,max1,max2,max3,maxmcp0,maxmcp1,xwc1,xwc2,ywc1,ywc2,tmcp3,tmcpd3'.split(','))

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

# #X = df[['t0','t1','t2','t3','max0','max1','max2','max3']].values
df.eval('xt = xwc2-3.7', inplace=True)
df.eval('yt = ywc2+9.5', inplace=True)
df0 = pd.DataFrame(columns=['x', 'y', 'max00', 'max01', 'max02', 'max03',
                                      'max10', 'max11', 'max12', 'max13',  
                                      'max20', 'max21', 'max22', 'max23', 
                                      'max30', 'max31', 'max33', 'max33'
                                      ])

for index, r in df.iterrows:
  pos = position_run[r['run']]
  new_rows = [[x, y,   0, 0, 0, 0,
                       0,m0,m1, 0,
                       0,m2,m3, 0,
                       0, 0, 0, 0]]
  x = r['xt']
  y = r['yt']
  m0 = r['max0']
  m1 = r['max1']
  m2 = r['max2']
  m3 = r['max3']
  if pos == 'G4H4':     
    new_rows.append([x, -25-y,  0, 0, 0, 0,
                                0, 0, 0, 0,
                                m3,m2,0, 0,
                                m1,m0,0, 0])
    new_rows.append([x, +25-y,  0, 0, 0, 0,
                                0, 0, 0, 0,
                                0, 0, 0, 0,
                                0, 0, 0, 0])
  elif pos == 'G4G5':     
    new_rows.append([-25-x, y,  m3,m2, 0, 0,
                                m1,m0, 0, 0,
                                m3,m2, 0, 0,
                                0, 0, 0, 0])
    new_rows.append([+25-x, y,  0, 0,m3,m2,
                                0, 0,m1,m0,
                                0, 0,m3,m2,
                                0, 0, 0, 0])
  elif pos == 'G5H5':     
    
  elif pos == 'H4H5':     
    new_rows.append([-25-x, y, m3,m2, 0, 0,
                               m1,m0, 0, 0,
                               m3,m2, 0, 0,
                                0, 0, 0, 0])
    new_rows.append([+25-x, y,  0, 0,m3,m2,
                                0, 0,m1,m0,
                                0, 0,m3,m2,
                                0, 0, 0, 0])
  elif pos == 'G4G5H4H5': 
    



# for i in range(0,len(df.index)):
  
X = df[args.variables].values
y = df[['xt', 'yt']].values
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.3)

def getWflat(_Y):
  hist, binLimX, binLimY = np.histogram2d(_Y[:,0], _Y[:,1], bins=[50, 50], range=[[-8.8,16.2],[-22,3]])
  binsx = np.digitize(_Y[:,0],binLimX)
  binsy = np.digitize(_Y[:,1],binLimY)
  def getWeight(binx,biny):
    return 1.0/hist[binx-1][biny-1]*100
  v_getWeight = np.vectorize(getWeight)
  return v_getWeight(binsx, binsy)

# w_train = getWflat(y_train)
# w_val = getWflat(y_val)

import math
def getWradial(_x,_y):
  r=(_x**2+_y**2)**0.5
  return math.exp(-r)
  #return -10/(25*2**0.5)*r+10
  #if r<12.5: return 1
  #else: return 0.2
v_getWradial = np.vectorize(getWradial)
w_train = v_getWradial(y_train[:,0],y_train[:,1])
w_val = v_getWradial(y_val[:,0],y_val[:,1])

  

print("Starting regressor")
#from sklearn.ensemble import HistGradientBoostingRegressor as regressor
from sklearn.ensemble import RandomForestRegressor as regressor

#regr = regressor(verbose=1, n_jobs=n_jobs)


regr = regressor(verbose=1, n_jobs=n_jobs,
                 max_leaf_nodes = max_leaf_nodes,
                 n_estimators = n_estimators,
                 max_features = max_features,
                 bootstrap = bootstrap,
                 max_samples = max_samples,
                 criterion = loss)


regr.fit(X_train, y_train, sample_weight=w_train)

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

outFile = open(outDir+'/output_train_%s.dat'%(args.outFile),'w')
for a,b,c,d,f,g,h,i,l in zip(y_hat_train[:,0],  y_hat_train[:,1], y_train[:,0], y_train[:,1], X_train[:,-1],  X_train[:,-2],  X_train[:,-3],  X_train[:,-4],w_train):
  outFile.write('%lf %lf %lf %lf %lf %lf %lf %lf %lf\n'%(a,b,c,d,f,g,h,i,l))
outFile.close()

outFile = open(outDir+'/output_eval_%s.dat'%(args.outFile),'w')
for a,b,c,d,f,g,h,i,l in zip(y_hat_val[:,0], y_hat_val[:,1], y_val[:,0], y_val[:,1], X_val[:,-1],  X_val[:,-2],  X_val[:,-3],  X_val[:,-4], w_val):
  outFile.write('%lf %lf %lf %lf %lf %lf %lf %lf %lf\n'%(a,b,c,d,f,g,h,i,l))
outFile.close()


# outFile = open(outDir+'/output_data_%s.dat'%(args.outFile),'w')
# for a,b,c,d,e,f,g in zip(df['run'].values,
#                          df['xwc2'].values,
#                          df['ywc2'].values,
#                          df['max0'].values,
#                          df['max1'].values,
#                          df['max2'].values,
#                          df['max3'].values) :
#   outFile.write('%d %lf %lf %lf %lf %lf %lf\n'%(a,b,c,d,e,f,g))
# outFile.close()

# outFile = open(outDir+'/output_target_%s.dat'%(args.outFile),'w')
# for a,b,c in zip(df['tmcpd3'].values, df['xwc2'].values, df['ywc2'].values):
#   outFile.write('%lf %lf %lf\n'%(a,b,c))
# outFile.close()

from sklearn.metrics import mean_squared_error
risk_train_x = mean_squared_error(y_train[:,0],y_hat_train[:,0])
risk_train_y = mean_squared_error(y_train[:,1],y_hat_train[:,1])
risk_val_x = mean_squared_error(y_val[:,0],y_hat_val[:,0])
risk_val_y = mean_squared_error(y_val[:,1],y_hat_val[:,1])
score_train = regr.score(X_train, y_train)
score_test = regr.score(X_val, y_val)

outFile = open(outDir+'/output_risk_%s.dat'%(args.outFile),'w')
outFile.write('risk train x %f\n'%risk_train_x)
outFile.write('risk train y %f\n'%risk_train_y)
outFile.write('risk test x %f\n'%risk_val_x)
outFile.write('risk test y %f\n'%risk_val_y)
outFile.write('score train %f\n'%score_train)
outFile.write('score test %f\n'%score_test)
outFile.close()

#outFile = open('bdt%s.pkl'%(args.outFile),'wb')
#pickle.dump(bdt,outFile)
#outFile.close()
