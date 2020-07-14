#!/usr/bin/python
#coding = utf-8
# ==============================================================================
#       Filename:  MergeTwoExcel.py
#       Author:    Qin Dongyi
#       本人承诺本程序是自己编写的，没有抄袭
# ==============================================================================
import pandas as pd
import re
from string import digits

def Merge(AllBJAirQualityData, AllBJWeatherData):
    AllBJAirQualityDatRows = len(AllBJAirQualityData) # 总行数
    AllBJWeatherDataRows = len(AllBJWeatherData) # 总行数
    
    MergedDate = [] # 存储两表共同的日期数据
    MergedWeatherCondition = [] # 天气状况
    MergedTemperature = [] # 气温
    MergedWindDirection = []# 风力风向
    MergedAQI = []
    MergedQuaLevel = []
    MergedPM25 = []
    MergedPM10 = []
    MergedSO2 = []
    MergedCO = []
    MergedNO2 = []
    MergedO3_8h = []
    for i in AllBJAirQualityData['日期']:
        for j in AllBJWeatherData['日期']:
            i_To_Num = str(i).replace('-', '', 2).replace(' 00:00:00', '',1) 
            j_To_Num = str(j).replace('-', '', 2).replace(' 00:00:00', '',1)
                # 这里的日期解析出来很奇怪，最后索性直接当作字符串处理了
            if i_To_Num == j_To_Num: # 相同的日期，存储起来
                MergedDate.append(i)
                break
    
    for i in range(0, AllBJAirQualityDatRows): # 遍历所有行
        OneLineData = AllBJAirQualityData[i:i+1]
        Date = str(OneLineData['日期']).replace('Name: 日期, dtype: object', '')[-11: -1]
        if Date in MergedDate:
            AQIData = str(OneLineData['AQI']).replace('\nName: AQI, dtype: int64', '')[-4: ].replace(' ', '')
            MergedAQI.append(AQIData)

            QuaLevelData = str(OneLineData['质量等级']).replace('\nName: 质量等级, dtype: object','')[-5: ].replace(' ', '')
            MergedQuaLevel.append(QuaLevelData)
            
            PM25Data = str(OneLineData['PM2.5']).replace('\nName: PM2.5, dtype: int64','')[-4: ].replace(' ', '')
            MergedPM25.append(PM25Data)
            
            PM10Data = str(OneLineData['PM10']).replace('\nName: PM10, dtype: int64','')[-4: ].replace(' ', '')
            MergedPM10.append(PM10Data)
            
            SO2Data = str(OneLineData['SO2']).replace('\nName: SO2, dtype: int64','')[-4: ].replace(' ', '')
            MergedSO2.append(SO2Data)

            COData = str(OneLineData['CO']).replace('\nName: CO, dtype: float64','')[-6: ].replace(' ', '')
            MergedCO.append(COData)

            NO2Data = str(OneLineData['NO2']).replace('\nName: NO2, dtype: int64','')[-4: ].replace(' ', '')
            MergedNO2.append(NO2Data) 

            O3_8hData = str(OneLineData['O3_8h']).replace('\nName: O3_8h, dtype: int64','')[-4: ].replace(' ', '')
            MergedO3_8h.append(O3_8hData)
    
    remove_digits = str.maketrans('', '', digits)
    for i in range(0,AllBJWeatherDataRows):
        OneLineData = AllBJWeatherData[i:i+1]
        Date = str(OneLineData['日期']).replace('\nName: 日期, dtype: datetime64[ns]', '')[-11: ].replace(' ', '')
        if Date in MergedDate:
            WeatherConditionData = str(OneLineData['天气状况']).translate(remove_digits)
            WeatherConditionData = WeatherConditionData.replace('\nName: 天气状况, dtype: object', '')[-10: ].replace(' ', '')
            MergedWeatherCondition.append(WeatherConditionData)

            TemperatureData = str(OneLineData['气温']).replace('\nName: 气温, dtype: object', '')[-10: ].replace(' ', '')
            MergedTemperature.append(TemperatureData)

            WindDirectionData = str(OneLineData['风力风向']).replace('\nName: 风力风向, dtype: object', '')[-20: ].replace(' ', '')
            while WindDirectionData[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                WindDirectionData = WindDirectionData[1: ]
            MergedWindDirection.append(WindDirectionData)
    
    df1 = pd.DataFrame({'日期': MergedDate})
    df2 = pd.DataFrame({'AQI': MergedAQI})
    df3 = pd.DataFrame({'质量等级': MergedQuaLevel})
    df4 = pd.DataFrame({'PM2.5': MergedPM25})
    df5 = pd.DataFrame({'PM10': MergedPM10})
    df6 = pd.DataFrame({'SO2': MergedSO2})
    df7 = pd.DataFrame({'CO': MergedCO})
    df8 = pd.DataFrame({'NO2': MergedNO2})
    df9 = pd.DataFrame({'O3_8h': MergedO3_8h})
    df10 = pd.DataFrame({'天气状况': MergedWeatherCondition})
    df11 = pd.DataFrame({'气温': MergedTemperature})
    df12 = pd.DataFrame({'风力风向': MergedWindDirection})

    
    result = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12], axis=1)
    result.to_excel('北京合并数据.xlsx', sheet_name = '合并数据', startcol = 0, index = False)
    return

if __name__ == '__main__':
    AllBJAirQualityData = pd.read_excel(r'北京空气质量.xlsx') # 读取空气质量数据
    BJWeatherData = pd.ExcelFile(r'北京天气爬虫.xlsx') # 读取天气数据
    # 因为爬取的时候为了显示好看，将数据按年份分了sheet存储
    # 这里为了合并方便需要先把天气数据合并到一起
    SheetNames = BJWeatherData.sheet_names  # 获取北京天气爬虫工作区的工作表名称
    AllBJWeatherData = pd.DataFrame()
    for i in SheetNames:
        OneYearData = pd.read_excel('北京天气.xlsx', sheet_name = i)
        AllBJWeatherData = pd.concat([AllBJWeatherData, OneYearData]) # 不同sheet数据级联
    Merge(AllBJAirQualityData, AllBJWeatherData)