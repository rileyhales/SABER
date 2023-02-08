from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from functools import reduce
import json
import glob

clay = pd.read_csv('/Users/jonahdundas/data/SABER/Japan/clay_japan.csv')
coarse = pd.read_csv('/Users/jonahdundas/data/SABER/Japan/coarse_japan.csv')
landcover = pd.read_csv('/Users/jonahdundas/data/SABER/Japan/landcover_japan.csv')
sand = pd.read_csv('/Users/jonahdundas/data/SABER/Japan/sand_japan.csv')
silt = pd.read_csv('/Users/jonahdundas/data/SABER/Japan/silt_japan.csv')
average_slopes = pd.read_csv('/Users/jonahdundas/data/SABER/Japan/slopes_japan.csv')
max_slopes = pd.read_csv('/Users/jonahdundas/data/SABER/Japan/maxSlopes_japan.csv')

# slopes_japan_1
# pd.concat([pd.read_csv(f) for f in glob.glob('slopes_japan_*.csv')])


data_frames = [clay, coarse, landcover, sand, silt, average_slopes,max_slopes]

df_merged = reduce(lambda left, right: pd.merge(left, right, on=['OBJECTID'], how='outer', suffixes=('', '_drop')),
                   data_frames)
for col in df_merged:
    if str(col)[-4:] == 'drop':
        df_merged.drop(columns=[str(col), ], inplace=True, errors='ignore')

def split_ugly_string(x):
  b = json.loads(x.replace('{', '"{').replace('}', '}"'))
  b = list(map(lambda x: x.replace('{', '').replace('}', '').split(', '), b))
  b = pd.DataFrame(b).apply(lambda x: x.str.split('='))
  b[['code', 'value']] = pd.DataFrame(b.iloc[:,0].to_list(),index=b.index)
  b[['sum','area']] = pd.DataFrame(b.iloc[:,1].to_list(), index=b.index)
  b.drop(columns=['code','sum'], inplace=True)
  b.drop([0,1], axis=1, inplace=True)
  b = b.T
  b.columns = b.iloc[0]
  b.drop(['value'], axis=0, inplace=True)
  b.reset_index(drop=True,inplace=True)
  return b

tmp = df_merged['groups'].apply(split_ugly_string)
tmp = pd.concat(tmp.values).reset_index()
df_merged = pd.merge(df_merged, tmp, left_index=True, right_index=True)
land_col = ['10','20','30','40','50','60','70','80','90','95','100']
df_merged[land_col] = df_merged[land_col].apply(pd.to_numeric)
df_merged['total area'] = df_merged[land_col].sum(axis=1)
df_merged.drop(columns=['GridID', 'HydroID','NextDownID','OBJECTID','Shape_Area','Shape_Leng','Tot_Drain_','groups','index','system:index','CatType','.geo','clay_0-5cm_mean','clay_5-15cm_mean','clay_15-30cm_mean','clay_30-60cm_mean','sand_0-5cm_mean','sand_5-15cm_mean','sand_15-30cm_mean','sand_30-60cm_mean','silt_0-5cm_mean','silt_5-15cm_mean','silt_15-30cm_mean','silt_30-60cm_mean','cfvo_0-5cm_mean','cfvo_5-15cm_mean','cfvo_15-30cm_mean','cfvo_30-60cm_mean'],inplace=True)
df_merged.rename(columns={'mean':'average slope','max':'max slope'},inplace=True)

for percentage in land_col:
    df_merged[str(percentage) + '%'] = df_merged[percentage] / df_merged['total area']

# print(df_merged.columns)

df_merged['average_clay_0to60cm'] = df_merged['average_clay_0to60cm'].div(1000)
df_merged['average_coarse_0to60cm'] = df_merged['average_coarse_0to60cm'].div(1000)
df_merged['average_sand_0to60cm'] = df_merged['average_sand_0to60cm'].div(1000)
df_merged['average_silt_0to60cm'] = df_merged['average_silt_0to60cm'].div(1000)

df_merged['maxValueIndex'] = df_merged[land_col].idxmax(axis=1)

ohe_labels = sorted(df_merged['maxValueIndex'].unique())
x = df_merged['maxValueIndex'].to_numpy()
x = x.reshape(-1,1)
enc = OneHotEncoder()
enc.fit(x)
onehotlabels = enc.transform(x).toarray()
ohe = pd.DataFrame(onehotlabels)
ohe.columns = ohe_labels

df_merged = pd.concat([df_merged,ohe],axis=1)

df_merged.to_csv('/Users/jonahdundas/data/SABER/Japan/japan_stats.csv')
