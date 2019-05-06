"""-*- coding: utf-8 -*-
 DateTime   : 2019/4/20 9:39
 Author  : Peter_Bonnie
 FileName    : data_helper.py
 Software: PyCharm
"""
import pandas as pd
import os
import logging
import time
from config import *
import numpy as np

#对原始文件进行一个预处理
def data_loader(filename):
    logging.info("start run the code")

    start=time.time()
    data=pd.read_csv(filename)

    columns=data.columns
    vals=data.values

    #获取csv文件的特征列
    columns=columns.values
    columns=str(columns).split(' ')
    columns=[col for col in columns if col not in ['[','\'#','',']']]
    columns[-1]=columns[-1].strip('\]\'')

    #创建一个数据框对象，用于存储数据
    df=pd.DataFrame(columns=columns)
    dp_data=[[] for _ in range(len(columns))]

    for i in range(vals.shape[0]):
        print([val for val in str(vals[i]).strip('\"\']').split(' ') if val not in ['[','\'#','','\']','\"']])
        for col_index in range(len(columns)):
                dp_data[col_index].append([val for val in str(vals[i]).strip('\"\']').split(' ') if val not in ['[','\'#','','\']','\"']][col_index])

    for i in range(len(columns)):
        df[columns[i]]=dp_data[i]

    df[columns[0]]=df[columns[0]].apply(lambda x:x.lstrip('\''))

    PATH='data/NEW-DATA-1.csv'
    if os.path.exists(PATH):
        os.remove(PATH)

    df.to_csv(PATH,index=False,encoding='utf-8')

    end=time.time()
    #代码运行时间
    print("it total costs {:.8f} sec".format(end-start))

def data_batch_normal(filename,config=Config()):
    """mainly batch normalization data of filename
    Args:
       filename

    Returns:
      new file
    """
    data=pd.read_csv(filename)
    config.config("conf/NASDAQ100.json")


    for i in data.columns:
        if i not in ["NDX"]:
            mean_value=np.mean(data[i].values)
            std_value=np.std(data[i].values)
            data[i]=(data[i].values-mean_value)/std_value

    if os.path.exists("data/nasdaq100/small/nasdaq100_padding_1.csv"):
        os.remove("data/nasdaq100/small/nasdaq100_padding_1.csv")
    data.to_csv("data/nasdaq100/small/nasdaq100_padding_1.csv",index=False)

def get_landsensor_set(filename):
    df=pd.read_excel(filename,encoding="utf_8_sig")
    for i in ['id（记录id）','create_date（记录插入时间）','equid（网关地址）','land_ec（土壤电导率 S/m）']:
        df.pop(i)
    df=df.rename(columns={"air_temperature（空气温度 摄氏度）":"air_temperature","air_humidity（空气湿度 %RH）":"air_humidity",
                          "land_temperature（土壤温度 摄氏度）":"land_temperature","land_humidity（土壤湿度 %RH）":"land_humidity",
                          "land_ph（土壤酸碱度）":"land_ph","light（光照度 Lux）":"light"})
    df.fillna(0.0)
    print(df)
    print(df.columns)

    df.to_csv("data/landsensor.csv",index=False)

if __name__=="__main__":
    # data_batch_normal("data/nasdaq100/small/nasdaq100_padding.csv")
    get_landsensor_set("data/jd_sensor_data.xls")










