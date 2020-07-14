# BeijingClimateDataAnalysis
爬虫爬取北京天气数据，pandas和numpy处理数据，matplot可视化展示数据，sklearn机器学习方法预测空气状况。


ReadBJWeather.py
从 http://www.tianqihoubao.com/lishi/beijing.html 网站上通过爬虫把北京2011年-至今的天气数据爬下来，
并保存为 北京天气爬虫.xlsx


MergeTwoExcel.py
读入北京空气质量数据（北京空气质量.xlsx），并把该数据和第1步中得到的北京天气爬虫数据进行融合，得到一个
同时包含天气和空气质量的表格数据，保存为 合并数据.xlsx


WeatherPie.py
对2011-2019年的每一年，统计这一年中白天为晴、雨、多云、阴、雪、雾霾、扬沙的天数，并绘制成饼图.


ContinuePollution.py
对2014-2019年的每一年，统计这一年中持续1天污染的次数、持续2天污染的次数、持续3天污染的次数、持续4天污染
的次数和持续5天及以上有污染的次数，把所有年份的统计结果绘制成一幅柱状图.


Prediction.py
在北京历史天气和空气质量数据的基础上，根据当天的天气情况以及前两天的天气及空气质量情况，预测当天的空气质量
等级，要求至少比较两种算法，从中选出较优的算法并确定最优超参数.
