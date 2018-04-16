# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
import os
import urllib
import time

headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6','Referer':'http://app.sipo-reexam.gov.cn/reexam_out/searchdoc/searchfs.jsp'
           }
# 爬虫抓取网页
def getHtml(url):
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.text,'lxml')
    return soup

# 获取股票代码
def getStackCode(url):
    stcokcodes = []
    soup = getHtml(url)
    codes = soup.select('#quotesearch > ul > li > a') #找到code
    for code in codes:
        stcokcode = code.text
        r = re.findall(r'[^()]+', stcokcode)[1] #正则匹配括号里的code
        stcokcodes.append(r)
    #print(stcokcodes)
    return stcokcodes

url = 'http://quote.eastmoney.com/stocklist.html#sh'
filepath = 'D:\\stock_data\\stockinfo\\'  # 定义数据文件保存路径
#filepath = './stockinfo/'  # 定义数据文件保存路径，相对路径保存

# 调用函数获得股票代码
code = getStackCode(url)
# 获取以6开头的所有沪市股票数据
CodeList = []
for item in code:
    if item[0] == '6':
        CodeList.append(item)

# 抓取数据并保存到本地csv文件
#start = '20170101' 设置开始时间
today = time.strftime('%Y%M%d')
for code in CodeList:
    print('正在获取股票%s数据' % code)
    url = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + \
          '&end='+str(today)+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    urllib.request.urlretrieve(url, filepath + code + '.csv')

'''
http://quotes.money.163.com/service/chddata.html?code=1000002&start=19910129&end=20161006&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP 
其中我标记红色的部分，是针对每只股票的数据
code: 深市六位代码前加“1”，沪市股票代码前加“0”
start: 开始日期，如果想得到每只股票的所有历史交易数据，可以以公司上市日期来表达，8位数字，分别为yyyymmdd
end: 结束日期，表示的也是yyyymmdd八位数字
fields字段包括了开盘价、最高价、最低价、收盘价
'''
#########################将股票数据存入数据库###########################

# 数据库名称和密码
name = 'root'
password = 'root'  # 替换为自己的账户名和密码
db_name = 'stock_data'
db = pymysql.connect('localhost', name, password, db_name,charset='utf8')
cursor = db.cursor()

# 获取本地文件列表
fileList = os.listdir(filepath)
# 依次对每个数据文件进行存储
for fileName in fileList:
    data = pd.read_csv(filepath + fileName, encoding="gbk")
    # 创建数据表，如果数据表已经存在，会跳过继续执行下面的步骤print('创建数据表stock_%s'% fileName[0:6])
    sqlConn = "create table stock_%s" % fileName[0:6] + "(日期 date, 股票代码 VARCHAR(10),     名称 VARCHAR(10),\
                       收盘价 float,    最高价    float, 最低价 float, 开盘价 float, 前收盘 float, 涨跌额    float, \
                       涨跌幅 float, 换手率 float, 成交量 bigint, 成交金额 bigint, 总市值 bigint, 流通市值 bigint)"
    cursor.execute(sqlConn)

# 迭代读取表中每行数据，依次存储
    print('正在存储stock_%s' % fileName[0:6])
    length = len(data)
    for i in range(0, length):
        record = tuple(data.loc[i])
        # 插入数据语句
        try:
            sqlInsert = "insert into stock_%s" % fileName[0:6] + "(日期, 股票代码, 名称, 收盘价, 最高价, 最低价, 开盘价, 前收盘, 涨跌额, 涨跌幅, 换手率, \
                成交量, 成交金额, 总市值, 流通市值) values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
            # 获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
            sqlInsert = sqlInsert.replace('nan', 'null').replace('None', 'null').replace('none', 'null')
            cursor.execute(sqlInsert)
        except:
            # 如果以上插入过程出错，跳过这条数据记录，继续往下进行
            break
# 关闭游标，提交，关闭数据库连接
cursor.close()
db.commit()
db.close()