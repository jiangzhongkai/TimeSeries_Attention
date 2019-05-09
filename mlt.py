"""-*- coding: utf-8 -*-
 DateTime   : 2019/5/7 20:07
 Author  : Peter_Bonnie
 FileName    : mlt.py
 Software: PyCharm
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#TODO:主要是画图代码
def plot_boxplot(xlabel,ylabel,title,xticklabels):
    fig = plt.figure(figsize=(9,7))  # 创建画布
    ax = plt.subplot()  # 创建作图区域
    plt.title(title,fontsize=14)
    f=ax.boxplot([[0.0026,0.00087,0.00075], [0.00234,0.00075,0.00128], [0.00105,0.00075]],patch_artist=False,boxprops={'color':'green'})  # 设置最大值不超过95分位点；最小值不小于5%分位点。
    #箱体内部填充颜色
    # for box in f['boxes']:
    #     box.set(facecolor='red')
    #设置横坐标的刻度值
    ax.set_xticklabels(xticklabels,fontsize=12)
    for cap in f['caps']:
        cap.set(color='blue',linewidth=2)
    for median in f['medians']:
        median.set(color='red',linewidth=2)
    for whisker in f['whiskers']:
        whisker.set(color='#CA6F1E',linewidth=2)
    ax.set_alpha(alpha=0.2)
    plt.grid(True,linestyle='--',color='lightgrey',alpha=0.8)
    plt.yticks(fontsize=12)
    plt.ylabel(ylabel,fontsize=14)
    # plt.xlabel(xlabel,fontsize=14)
    plt.savefig(title+'_'+xlabel+'.pdf')

    plt.show()

def attention_plot():
    """仿照nlp中的权中进行简单查看"""
    pass

def plot_figure(data,save_name,drop_cols):
    """
    :param data:
    :return:
    """
    data = pd.read_csv(data)
    for col in drop_cols:
        data.pop(col)
    values = data.values[:1500]
    size=len(data.columns)
    group=[i for i in range(1,size,1)]
    i = 1
    plt.figure(figsize=(10,10))
    for g in group:
        plt.subplot(len(group), 1, i)
        plt.plot(values[:,g],'r')
        plt.xlabel("Date")
        plt.title(data.columns[g], y=0.5, loc="right")
        i += 1
    plt.savefig(save_name)
    plt.show()

if __name__=='__main__':
    # plot_boxplot(xlabel='Time Steps',ylabel='RMSE',title='SML2010 Dataset',xticklabels=['learning rate','timesteps','hidden units'])
    plot_boxplot(xlabel='Time Steps', ylabel='MSE', title='SML2010 Dataset',
                 xticklabels=['learning rate', 'timesteps', 'hidden units'])

    # plot_figure("data/NEW-DATA-1.csv",save_name='state.pdf',drop_cols=["1:Date",
    #     "2:Time",
    #     "19:Exterior_Entalpic_1",
    #     "20:Exterior_Entalpic_2",
    #     "21:Exterior_Entalpic_turbo",
    #     "24:Day_Of_Week"])


