"""-*- coding: utf-8 -*-
 DateTime   : 2019/4/20 9:39
 Author  : Peter_Bonnie
 FileName    : data_helper.py
 Software: PyCharm
"""
import pandas as pd
import os

#对原始文件进行一个预处理
data=pd.read_csv("data/NEW-DATA-2.T15.csv")

columns=data.columns
vals=data.values

#获取csv文件的特征列
columns=columns.values
columns=str(columns).split(' ')
columns=[col for col in columns if col not in ['[','\'#','',']']]
columns[-1]=columns[-1].strip('\]\'')

#获取对应特征的值
print(vals)

df=pd.DataFrame(columns=columns)
dp_data=[[] for _ in range(len(columns))]

for i in range(vals.shape[0]):
    print([val for val in str(vals[i]).strip('\"\']').split(' ') if val not in ['[','\'#','','\']','\"']])
    for col_index in range(len(columns)):
            dp_data[col_index].append([val for val in str(vals[i]).strip('\"\']').split(' ') if val not in ['[','\'#','','\']','\"']][col_index])

    print(dp_data)

for i in range(len(columns)):
    df[columns[i]]=dp_data[i]

df[columns[0]]=df[columns[0]].apply(lambda x:x.lstrip('\''))


PATH='NEW-DATA-2.csv'
if os.path.exists(PATH):
    os.remove(PATH)

df.to_csv(PATH,index=False,encoding='utf-8')















