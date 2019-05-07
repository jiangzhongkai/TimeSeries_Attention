"""-*- coding: utf-8 -*-
 DateTime   : 2019/5/7 20:07
 Author  : Peter_Bonnie
 FileName    : mlt.py
 Software: PyCharm
"""
import matplotlib.pyplot as plt
import seaborn as sns

def plot_boxplot(xlabel,ylabel,title):
    fig = plt.figure()  # 创建画布
    ax = plt.subplot()  # 创建作图区域
    plt.title(title,fontsize=14)
    f=ax.boxplot([[1.5, 2.3, 4.1], [2, 1, 8, 10], [2, 4]],patch_artist=False,boxprops={'color':'green'})  # 设置最大值不超过95分位点；最小值不小于5%分位点。
    #箱体内部填充颜色
    # for box in f['boxes']:
    #     box.set(facecolor='red')
    #设置横坐标的刻度值
    ax.set_xticklabels(['24', '18', '3'],fontsize=12)
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
    plt.xlabel(xlabel,fontsize=14)
    plt.savefig(title+'_'+xlabel+'.pdf')

    plt.show()

if __name__=='__main__':
    plot_boxplot(xlabel='Time Steps',ylabel='RMSE',title='Landsensor Dataset')


