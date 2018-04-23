import datetime
import numpy as np
import pandas as pd
import pylab
import os
import time
import warnings
from sklearn.cross_validation import train_test_split
warnings.filterwarnings("ignore")
from sklearn import  preprocessing
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.dates import  date2num
from pylab import mpl
import copy
import pandas
import math





def get_forecast(data):
    mpl.rcParams['font.sans-serif'] = ['SimHei']#解决中文乱码问题
    mpl.rcParams['axes.unicode_minus'] = False#解决标点符号显示问题
    pylab.rcParams['figure.figsize'] = (15, 9) #设置绘图尺寸

    #print(data)
    # print(stock['名称'][0][:10])

    #data['收盘价'].plot()
    del data['名称']
    forecast_col = '收盘价'
    data.fillna(-99999, inplace=True)
    forecast_out = 5
    #forecast_out = int(math.ceil(0.01 * len(data)))  # math.ceil：返回大于等于数字参数的最小整数(取整函数)
    data['label'] = data[forecast_col].shift(-forecast_out)  # shift函数是对数据进行移动的操作,此处是将股票收盘价向前移动forecast_out个位置，然后作为标签
    data = data[data.index > '2018-01-01']


    try:
        # 将最后一条数据的日期转化为时间戳

        last_date = data.iloc[-1].name
        last_unix = time.strptime(last_date, '%Y-%m-%d')
        last_unix = time.mktime(last_unix)

        #last_unix = last_date.timestamp()
        #last_unix = time.mktime(last_date.timetuple())
        one_day = 86400
        next_unix = last_unix + one_day
    except IndexError:
        pass
    X = np.array(data.drop(['label'], 1))  # 对于DataFrame，可以从任何坐标轴删除索引值：
    try:
        X = preprocessing.scale(X)  # 数据缩放的算法
        X = X[:-forecast_out]
        X_lately = X[-forecast_out:]
        data.dropna(inplace=True)#可以按行丢弃带有nan的数据
        y = np.array(data['label'])
    except ValueError:
        pass


    #print(data)
    #模型建立与模型预测
    # 划分训练集和测试集，测试集占比20%，训练集占比80%
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        clf = LinearRegression(n_jobs=-1)  # n_jobs=-1 表示使用所有CPU

        clf.fit(X_train, y_train)
        accuracy = clf.score(X_test, y_test)
        forecast_set = clf.predict(X_lately)

        data['预测'] = np.nan
    except UnboundLocalError:
        pass
    try:
        # 将最后一条数据的日期转化为时间戳

        try:
            last_unix = time.strptime(last_date, '%Y-%m-%d')
            last_unix = time.mktime(last_unix)

            #last_unix = last_date.timestamp()
            #last_unix = time.mktime(last_date.timetuple())
            one_day = 86400
            next_unix = last_unix + one_day
        except UnboundLocalError:
            pass
    except IndexError:
        pass
    try:
        # 循环输出日期及预测值
        try:
            for i in forecast_set:
                next_date = datetime.datetime.fromtimestamp(next_unix).strftime('%Y-%m-%d')

                next_unix += one_day
                data.loc[next_date] = [np.nan for _ in range(len(data.columns) - 1)] + [i]    # 查看预测后的数据表

            # 对真实值和预测值可视化
            #print(data)
            #exit()
            fig, ax = plt.subplots()
            ax.set_title(stocks['名称'][0][:10] + '预测收盘走势', fontsize=17)
            plt.xlabel("时间")
            ax.set_ylabel("股价（元）")

            data['收盘价'].plot()
            data['预测'].plot()

            plt.legend()
            plt.xlabel('Date')
            plt.ylabel('Price')
            #plt.show()
            print('正在打印'+e.split('\\')[3].split('.')[0])
            plt.savefig(str('E:\\stock_data\\stock_trend_chart\\'+e.split('\\')[3].split('.')[0]))
            #plt.show()
        except ValueError:
            pass
    except UnboundLocalError:
        pass

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
    for e in list:  # e返回的文件名
        try:
            df = pd.read_csv(e, encoding='gbk')
        except pandas.errors.EmptyDataError:
            pass

        stocks = df.loc[:, ['日期', '名称', '开盘价', '最高价', '收盘价', '最低价', '成交量']]
        #stock = stocks[stocks['日期'] > '2018-01-01']

        data = stocks.set_index('日期')
        data = data[::-1]

        if data.empty:#判断DataFrame是否为空，即是否有数据，有数据就画图，没有就忽略
            pass
        else:
            get_forecast(data)
