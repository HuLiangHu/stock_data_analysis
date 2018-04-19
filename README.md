# stock_data_analysis
#股票数据分析
1.股票数据爬虫
2.pandas,numpy对数据进行清洗
3.matplotlib数据可视化
stockinfo.py
设计爬虫项目从网易财经获取股票数据

get_k_line.py
Python绘制股票K线图

Forecast.py
使用python预测股票收盘价


Python打包exe文件,遇到的坑
1.安装pywin32  #https://jingyan.baidu.com/article/22fe7ced1ca36b3003617f7a.html
2.pip install pyinstaller
3.去github下载pyinstaller,复制pyinstaller-develop文件夹下的Pyinstaller文件到Python的工具包文件夹（site-packages)下替换pyinstaller https://github.com/pyinstaller/pyinstaller
4.安装sip pipinstall sip
5.pip uninstall enum34
5.pip install --upgrade setuptools  #解决module six  [AttributeError: 'str' object has no attribute 'items'
6396 WARNING: stderr: AttributeError: 'str' object has no attribute 'items']
6.安装PyQt5  pip install PyQt5或者下载PyQt5.exe #https://sourceforge.net/projects/pyqt/?source=typ_redirect   #Exception: Cannot find PyQt5 plugin directories


打包
pyinstaller -F Forecast.py --hidden-import sklearn.neighbors.typedefs   #ImportError: No module named typedefs`

pyinstaller -F K_line_graph.py

pyinstaller -F stockinfo.py


有其他问题欢迎大家提问。
