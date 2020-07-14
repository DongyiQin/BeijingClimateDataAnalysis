import pandas as pd
from sklearn.feature_extraction import DictVectorizer 
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV


def EncodeWeatherCondition(StringData):
    # 天气状况编码
    flag = 0
    if StringData == '晴':
        flag = 1
    elif StringData == '多云':
        flag = 2
    elif StringData == '阴':
        flag = 3
    elif '雨' in StringData:
        flag = 4
    elif '雪' in StringData and StringData != '雨夹雪':
        flag = 5
    elif '雾' in StringData or '霾' in StringData:
        flag = 6
    elif StringData == '扬沙':
        flag = 7
    return flag

def EncodeAirQualityLevel(StringData):
    # 空气质量情况编码
    flag = 0
    if StringData == '优':
        flag = 1
    elif StringData == '良':
        flag = 2
    elif StringData == '轻度污染':
        flag = 3
    elif StringData == '中度污染':
        flag = 4
    elif StringData == '重度污染':
        flag = 5
    elif StringData == '严重污染':
        flag = 6
    elif StringData == '无':
        flag = 2
    return flag

def ExtractNeededData(i, BJMergedData_Dict):
# 某一天的所需数据提取
    OneDayData = []
    OneDayData.append(BJMergedData_Dict[i]['AQI'])
    OneDayData.append(BJMergedData_Dict[i]['PM2.5'])
    OneDayData.append(BJMergedData_Dict[i]['PM10'])
    OneDayData.append(BJMergedData_Dict[i]['SO2'])
    OneDayData.append(BJMergedData_Dict[i]['CO'])
    OneDayData.append(BJMergedData_Dict[i]['NO2'])
    OneDayData.append(BJMergedData_Dict[i]['O3_8h'])

    DayNight = BJMergedData_Dict[i]['天气状况'].split('/') # 将白天晚上的天气状况数据分开
    DayCoder = EncodeWeatherCondition(DayNight[0])
    NightCoder = EncodeWeatherCondition(DayNight[1]) # 天气状况中文用数字来分类编码
                            #  晴：1，多云：2，阴：3，雨：4，雪：5，雾霾：6，扬沙：7
    OneDayData.append(DayCoder)
    OneDayData.append(NightCoder)
    return OneDayData
    
def EncodeData(BJMergedData):
    EncodedList = []
    BJMergedData_Dict = BJMergedData.to_dict(orient = 'record') # dataframe转化为dict数据
    # [{'日期': '2013-12-02', 'AQI': 142, '质量等级': '轻度污染', 
    # 'PM2.5': 109, 'PM10': 138, 'SO2': 61, 'CO': 2.6, 'NO2': 88, 
    # 'O3_8h': 11, '天气状况': '多云/多云', '气温': '11℃/-1℃', 
    # '风力风向': '无持续风向≤3级/无持续风向≤3级'}, .... ,{}]
    DayLength = len(BJMergedData_Dict)  # 一共多少天的数据
    for i in range(0, DayLength):
        if i >= 2:
            TheDayData = ExtractNeededData(i, BJMergedData_Dict) # 当天数据
            Last1DayData = ExtractNeededData(i-1, BJMergedData_Dict) # 前一天数据
            Last2DayData = ExtractNeededData(i-2, BJMergedData_Dict) # 前二天数据
            PredictOneDayData = TheDayData + Last1DayData + Last2DayData
                        #  预测某一天等级的全部数据，包括当天及前两天的空气数据和天气状况
            QuaLevFlag = EncodeAirQualityLevel(BJMergedData_Dict[i]['质量等级']) 
                        # 分类编码，共6种类别
                        # 优：1，良：2，轻度污染：3，中度污染：4，重度污染：5.严重污染：6，无：2
            PredictOneDayData.append(QuaLevFlag)    # 最后放入y，即标签值
            EncodedList.append(PredictOneDayData) 
    return EncodedList

def y_testToInteger(y_test):
    # 测试获得的结果不是整数，执行向下取整处理，
    # 得到分类1、2、3、4、5、6
    y_test_to_integer = []
    for y in y_test:
        if y < 1.5:
            y_test_to_integer.append(1)
        elif y < 2.5:
            y_test_to_integer.append(2)
        elif y < 3.5:
            y_test_to_integer.append(3)
        elif y < 4.5:
            y_test_to_integer.append(4)
        elif y < 5.5:
            y_test_to_integer.append(5)
        else:
            y_test_to_integer.append(6)
    return y_test_to_integer

def LinearRegPre(EncodedList): # 线性回归
    Data = np.array(EncodedList)
    X = Data[:,:-1]
    Y = Data[:,-1]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 1)
    # 训练数据、测试数据7：3划分

    # 线性回归训练
    regr = linear_model.LinearRegression()
    regr.fit(X_train,Y_train)
    print('coefficients(w1,w2...):',regr.coef_)  # 系数
    print('intercept(b):',regr.intercept_)  # 截距

    # 预测，获得的标签整数化，向下取整
    y_test = regr.predict(X_test)
    y_test_to_integer = y_testToInteger(y_test)

    print('多元线性回归结果：')
    print('准确率：', metrics.accuracy_score(Y_test, y_test_to_integer))
    print('精确率：', metrics.precision_score(Y_test, y_test_to_integer, average='weighted'))
    print('召回率：', metrics.recall_score(Y_test, y_test_to_integer, average='weighted')) 
            # weighted’: 为每个标签计算指标，并通过各类占比找到
            # 它们的加权均值（每个标签的正例数）.它解决了’macro’的标签不平衡问题；
    print('--------------------------------------')
    return

def SVMPre(EncodedList):  # 支持向量机
    Data = np.array(EncodedList)
    X = Data[:,:-1]
    Y = Data[:,-1]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 1)
    # 训练数据、测试数据7：3划分


    #构建SVM模型，并确定最优超参数
    svc = SVC()
    param = {'kernel':['linear', 'poly', 'rbf'], 'C': np.linspace(0.01, 1, 10), 'gamma': np.linspace(0.01, 1, 11)}
    gs = GridSearchCV(svc, param, cv = 5, n_jobs = -1, scoring = 'neg_mean_absolute_error')
    gs.fit(X_train,Y_train) # 训练并获得最优超参数
    
    # 使用最优超参数确定的模型预测
    # 获得的标签整数化，向下取整
    y_test = gs.predict(X_test)
    y_test_to_integer = y_testToInteger(y_test)

    print('支持向量机结果：')
    print('最优超参数：', gs.best_params_) # 输出最优超参数
    print('准确率：', metrics.accuracy_score(Y_test, y_test_to_integer))
    print('精确率：', metrics.precision_score(Y_test, y_test_to_integer, average='weighted'))
    print('召回率：', metrics.recall_score(Y_test, y_test_to_integer, average='weighted')) 
            # weighted’: 为每个标签计算指标，并通过各类占比找到
            # 它们的加权均值（每个标签的正例数）.它解决了’macro’的标签不平衡问题；
    print('--------------------------------------')
    return

if __name__ == '__main__':
    BJMergedData = pd.read_excel(r'北京合并数据.xlsx')  # 读取北京合并数据,得到DataFrame
    EncodedList = EncodeData(BJMergedData)  # 当天+前两天数据编码放入一个list 
    LinearRegPre(EncodedList)  # 多元线性回归预测   
    SVMPre(EncodedList)  # 支持向量机分类预测