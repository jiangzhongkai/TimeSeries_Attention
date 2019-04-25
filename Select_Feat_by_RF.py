"""-*- coding: utf-8 -*-
 DateTime   : 2019/4/25 14:31
 Author  : Peter_Bonnie
 FileName    : Select_Feat_by_RF.py
 Software: PyCharm
"""
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold,StratifiedKFold,ShuffleSplit,train_test_split
import  pandas as pd
import  numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import *
"""主要是利用RF随机森林进行数据初步特征选取"""
config=Config()
config.config("conf/NASDAQ100_best.json")
print(config.data_paths)

global data
if len(config.data_paths)<1:
    raise ValueError("data path is empty.")
elif len(config.data_paths)==1:
    data=pd.read_csv(config.data_paths[0])
else:
    # 拼接代码
    pass

Y=data.pop(config.target_cols[0])
X=data

print(X.info())

#设置K折交叉验证
feature_columns=X.columns
X,Y=X.values,Y
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=2019)

print("X_train.shape:{0},X_shape:{1}".format(X_train.shape,X_test.shape))

print("computing feature importantance.....")
#模型
rf=RandomForestRegressor(n_estimators=1000,random_state=2019,n_jobs=-1)
rf.fit(X_train,Y_train)

importantces=rf.feature_importances_
indices=np.argsort(importantces)[::-1]
threshold=0.001
imp_list=[]
for i in feature_columns:
    if importantces[i]>=threshold:
        imp_list.append(i)
for i in range(X_train.shape[1]):
    print("%2d)%-*s%f"%(i+1,30,feature_columns[indices[i]],importantces[indices[i]]))

np.savetxt("importantance.txt",imp_list)








