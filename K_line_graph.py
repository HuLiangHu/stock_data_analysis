import datetime
import warnings
from matplotlib.finance import candlestick2_ohlc
import numpy as np
import matplotlib.pyplot as plt
import pylab
import os
import pandas as pd
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import  date2num
from pylab import mpl
import copy
import pandas
warnings.filterwarnings("ignore")




def get_k_line(stock):
    mpl.rcParams['font.sans-serif'] = ['SimHei']#解决中文乱码问题
    mpl.rcParams['axes.unicode_minus'] = False#解决标点符号显示问题
    pylab.rcParams['figure.figsize'] = (20, 12) #设置绘图尺寸

    fig, (ax, ax2) = plt.subplots(2)

    try:
        ax.set_title(stock['名称'][0][:10] + '股票K线图', fontsize=17)
    except IndexError:
        pass
    ax.set_ylabel("股价（元）")
    ax.set_xticks(range(1, len(time), 10))
    ax.set_xticklabels(time[0:len(time):10],rotation=30)

    ax.grid(True)
    ax.xaxis_date()
    ax.autoscale_view()
    candlestick2_ohlc(ax, open1, high1, low1, close1, width=1, colorup='red', colordown='green')

    # MA5
    data['ma5'] = pd.rolling_mean(data['收盘价'], 5)
    ax.plot(tuple(data['ma5']), label='五日均线')
    # MA10
    data['ma10'] = pd.rolling_mean(data['收盘价'], 10)
    ax.plot(tuple(data['ma10']), label='十日均线')
    # MA20
    data['ma20'] = pd.rolling_mean(data['收盘价'], 20)
    ax.plot(tuple(data['ma20']), label='二十日均线')
    # MA30
    data['ma30'] = pd.rolling_mean(data['收盘价'], 30)
    ax.plot(tuple(data['ma30']), label='三十日均线')
    # MA60
    data['ma60'] = pd.rolling_mean(data['收盘价'], 60)
    ax.plot(tuple(data['ma60']), label='六十日均线')
    ax.legend()# 绘制K线图


    #print(stock['名称'][0][:10])

    plt.xlabel("时间")
    ax.set_ylabel("股价（元）")

    # 可同时绘制其他折线图
    ax.grid(True)
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    try:
        data['成交量'][::5].plot(kind='bar')
    except TypeError:
        pass
    ax2.set_ylabel('成交量')
    ax2.xaxis_date()
    ax2.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.savefig(str('E:\\stock_data\\K_line\\'+f.split('\\')[3].split('.')[0]))
    print('正在打印',f.split('\\')[3].split('.')[0])
    #plt.show()

if __name__ == '__main__':

    # 获取文件夹里所有股票文件,返回它的路径
    def GetFileList(dir, fileList):
        if os.path.isfile(dir):
            fileList.append(dir)
        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                newDir = os.path.join(dir, s)
                GetFileList(newDir, fileList)
        return fileList

    list = GetFileList('E:\\stock_data\\stockinfo', [])
    # 循环遍历路径列表,读取每个csv文件内容,将stockcode传入pandas_candlestick_ohlc函数里
    for f in list:  # e返回的文件名
        try:
            df = pd.read_csv(f,encoding='gbk')
        except pandas.errors.EmptyDataError:
            pass

        stocks = df.loc[:, ['日期', '名称', '开盘价', '最高价', '收盘价', '最低价', '成交量']]
        stock = stocks[stocks['日期'] > '2017-05-01']
        data = stock.set_index('日期')
        data=data[::-1]
        # 将日期转成数字,再将t,open,highs,lows,close放到series

        time = data.index
        t = []
        for x in time:
            x = str(x).split()[0]
            x = x.split('-')
            x = x[0] + x[1] + x[2]
            x = int(x)
            t.append(x)
        # 画图数据
        time = t
        #print(time[::20])

        try:
            open1 = tuple(data['开盘价'])
            high1 = tuple(data['最高价'])
            low1 =tuple(data['最低价'])
            close1 = tuple(data['收盘价'])
        except TypeError:
            pass


        if data.empty:#判断DataFrame是否为空，即是否有数据，有数据就画图，没有就忽略
            pass
        else:
            get_k_line(stock)

        #exit()








