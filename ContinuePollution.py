#!/usr/bin/python
#coding = utf-8
# ==============================================================================
#       Filename:  ContinuePollution.py
#       Author:    Qin Dongyi
#       本人承诺本程序是自己编写的，没有抄袭
# ==============================================================================
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

def SplitToOneYear(BJAirData):
    BJAirData_Dict = BJAirData.to_dict(orient = 'record') # dataframe转化为dict数据
    # [{'日期': '2013-12-02', 'AQI': 142, '质量等级': '轻度污染', 
    # 'PM2.5': 109, 'PM10': 138, 'SO2': 61, 'CO': 2.6, 'NO2': 88, 
    # 'O3_8h': 11, '天气状况': '多云/多云', '气温': '11℃/-1℃', 
    # '风力风向': '无持续风向≤3级/无持续风向≤3级'}, .... ,{}]
    YearAirData = {}
    for i in range(2014,2020): # 14-19年数据Dict，年份为key
        YearAirData[str(i)] = []

    for OneDay in BJAirData_Dict:
        Year = OneDay['日期'].split('-')[0].replace('\ufeff','',1) # 把年份单独取出来，
                                        # 便于按照年份分割，‘\ufeff’是数据中的一个乱码
        if Year != '2013' and Year != '2020':
            YearAirData[Year].append(OneDay['质量等级'])
    return YearAirData

def PolluDaysStatistic(YearAirData):
    AllYearStatistic = []
    for OneYearData in YearAirData:
        DaysNum = len(YearAirData[OneYearData])
        OneYearStatistic = {'连续一天': 0, '连续两天': 0, '连续三天': 0,\
                                 '连续四天': 0, '连续五天及以上': 0}

        for i in range(0, DaysNum):
            if i == 0 and ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' not in YearAirData[OneYearData][i+1]):
                OneYearStatistic['连续一天'] += 1
            elif i == DaysNum-1 and ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' not in YearAirData[OneYearData][i-1]):
                OneYearStatistic['连续一天'] += 1
            elif ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' not in YearAirData[OneYearData][i-1]) and \
                ('污染' not in YearAirData[OneYearData][i+1]):
                OneYearStatistic['连续一天'] += 1
#  [1]	该年的第一天：当前天有污染，之后一天无污染；
#  [2]	该年最后一天：当前天有污染，前面一天无污染；
#  [3]	该年中间：当前天有污染，前面一天无污染，之后一天无污染。
#-------------------------------------连续一天------------------------------------------
            elif i == DaysNum-1 and ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' in YearAirData[OneYearData][i-1]) and \
                ('污染' not in YearAirData[OneYearData][i-2]):
                OneYearStatistic['连续两天'] += 1
            elif i>=1 and ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' in YearAirData[OneYearData][i-1]) and \
                ('污染' not in YearAirData[OneYearData][i-2]) and \
                ('污染' not in YearAirData[OneYearData][i+1]):
                OneYearStatistic['连续两天'] += 1
#  [1]	非该年的最后一天：当前天有污染，前一天有污染，前二天无污染，后一天无污染；
#  [2]	该年的最后一天：当前天有污染，前一天有污染，前二天无污染。
#-------------------------------------连续两天------------------------------------------
            elif i == DaysNum-1 and ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' in YearAirData[OneYearData][i-1]) and \
                ('污染' in YearAirData[OneYearData][i-2]) and \
                ('污染' not in YearAirData[OneYearData][i-3]):
                OneYearStatistic['连续三天'] += 1
            elif i>=2 and ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' in YearAirData[OneYearData][i-1]) and \
                ('污染' in YearAirData[OneYearData][i-2]) and \
                ('污染' not in YearAirData[OneYearData][i-3]) and \
                ('污染' not in YearAirData[OneYearData][i+1]):
                OneYearStatistic['连续三天'] += 1   
#  [1]  非该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天无污染，后一天无污染；
#  [2]  该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天无污染。
#-------------------------------------连续三天------------------------------------------
            elif i == DaysNum-1 and ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' in YearAirData[OneYearData][i-1]) and \
                ('污染' in YearAirData[OneYearData][i-2]) and \
                ('污染' in YearAirData[OneYearData][i-3]) and \
                ('污染' not in YearAirData[OneYearData][i-4]):
                OneYearStatistic['连续四天'] += 1
            elif i>=3 and ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' in YearAirData[OneYearData][i-1]) and \
                ('污染' in YearAirData[OneYearData][i-2]) and \
                ('污染' in YearAirData[OneYearData][i-3]) and \
                ('污染' not in YearAirData[OneYearData][i-4]) and \
                ('污染' not in YearAirData[OneYearData][i+1]):
                OneYearStatistic['连续四天'] += 1
#  [1]	非该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天有污染，前四天无污染，后一天无污染；
#  [2]	该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天有污染，前四天无污染。
#-------------------------------------连续四天------------------------------------------
            elif i == DaysNum-1 and ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' in YearAirData[OneYearData][i-1]) and \
                ('污染' in YearAirData[OneYearData][i-2]) and \
                ('污染' in YearAirData[OneYearData][i-3]) and \
                ('污染' in YearAirData[OneYearData][i-4]):
                OneYearStatistic['连续五天及以上'] += 1
            elif i>=4 and ('污染' in YearAirData[OneYearData][i]) and \
                ('污染' in YearAirData[OneYearData][i-1]) and \
                ('污染' in YearAirData[OneYearData][i-2]) and \
                ('污染' in YearAirData[OneYearData][i-3]) and \
                ('污染' in YearAirData[OneYearData][i-4]) and \
                ('污染' not in YearAirData[OneYearData][i+1]):
                OneYearStatistic['连续五天及以上'] += 1
#  [1]	非该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天有污染，前四天有污染，后一天无污染；
#  [2]	该年的最后一天：当前天有污染，前一天有污染，前二天有污染，前三天有污染，前四天有污染。
#-------------------------------------连续五天及以上------------------------------------------
        AllYearStatistic.append(OneYearStatistic)
    return AllYearStatistic

def DrawConPollution(AllYearStatistic):
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    for OneYearData in AllYearStatistic:
        y1.append(OneYearData['连续一天'])
        y2.append(OneYearData['连续两天'])
        y3.append(OneYearData['连续三天'])
        y4.append(OneYearData['连续四天'])
        y5.append(OneYearData['连续五天及以上'])
    width = 0.15  #设置柱与柱之间的宽度
    
    x1 = range(len(y1))  #横坐标
    x2 = [i+width for i in x1]
    x3 = [i+width for i in x2]
    x4 = [i+width for i in x3]
    x5 = [i+width for i in x4]

    Bar1 = plt.bar(x1, y1, width = 0.15, alpha = 0.9, color = 'purple')
    Bar2 = plt.bar(x2, y2, width = 0.15, alpha = 0.9, color= 'red')
    Bar3 = plt.bar(x3, y3, width = 0.15, alpha = 0.9, color= 'blue')
    Bar4 = plt.bar(x4, y4, width = 0.15, alpha = 0.9, color= 'green')
    Bar5 = plt.bar(x5, y5, width = 0.15, alpha = 0.9, color= 'yellow')

    Year = ['2014', '2015', '2016', '2017', '2018', '2019']
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xticks([i+2*width for i in x1], Year)
    plt.yticks([0,5,10,15,20,25])
    plt.legend(['连续一天', '连续两天', '连续三天', '连续四天', '连续五天及以上'], \
                loc = "upper left")
    plt.title('2014-2019年持续污染天数按年份统计情况')

# 下面对所有柱子进行数字标注
    for rect in Bar1:  
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=15, ha='center', va='bottom')
    for rect in Bar2:  
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=15, ha='center', va='bottom')
    for rect in Bar3:  
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=15, ha='center', va='bottom')
    for rect in Bar4:  
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=15, ha='center', va='bottom')
    for rect in Bar5:  
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=15, ha='center', va='bottom')
    plt.show()
    return

if __name__ == '__main__':
    BJAirData = pd.read_excel(r'北京空气质量.xlsx')  # 读取北京合并数据,得到DataFrame
    YearAirData = SplitToOneYear(BJAirData) # 按年份把污染情况数据提取出来
    AllYearStatistic = PolluDaysStatistic(YearAirData) # 统计污染情况
    DrawConPollution(AllYearStatistic) # 绘制柱状图