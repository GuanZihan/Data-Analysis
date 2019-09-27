#encoding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
import re
import requests
from pylab import mpl
from pyecharts import Geo
from pandas import DataFrame,Series

#读取数据
mpl.rcParams['font.sans-serif'] = ['SimHei']
data = pd.read_excel('1.xls',header=0,index_col='location',sheet_name='压力')
data_flow = pd.read_excel('1.xls',header=0,index_col='location',sheet_name='流量')
data_tem = pd.read_excel('1.xls',header=0,index_col='location',sheet_name='温度')
data_sum = pd.read_excel('2.xls',header=0,sheet_name='东网',usecols=[4,5,6])
locations = pd. read_excel('1.xls',header=0,usecols=[0])
data = data.fillna(0)

#全局变量放在这
location=[]
place_pressure=dict()
place_20 = dict()
time_pressure_mean=[]
time_flow_mean=[]
time_tem_mean=[]
ak='5AgD1Ss0UHD1xhVBx7wM9v50z2rV0vvm'
lng_lat={}
#获取百度经纬度
def getCoordinate(place):
    place_dalian = "大连市" + str(place)
    url = 'http://api.map.baidu.com/geocoding/v3/?address=' + place_dalian + '&output=json&ak=' + str(
        ak) + '&callback=showLocation'
    r = requests.get(url).text
    lng = eval(re.findall('lng":(.*?),"', r)[0])
    lat = eval(re.findall('lat":(.*?)},"', r)[0])
    return lng,lat
#取得建筑物名字
def getLocation():
    for index,value in locations.iterrows():
        location.append(value['location'])
    return location
#GIS图
for place in getLocation():
    mean_pressure = data.loc[[place]].T.mean().loc[place]
    place_pressure[place]=mean_pressure
lng, lat =getCoordinate(place)
lng_lat[place] = [lng,lat]
net_map = list(zip(place_v.keys(), place_v.values()))
geo = Geo(u"全国主要城市影院数量分布", "data from dydata", title_color="#fff",
                title_pos="center", width= 1200, height=600, background_color='#404a59')
attr, value = geo.cast(net_map)
geo.add("cinema_distribution", attr, value, type="heatmap", visual_range=[0, int(max(value))+1],
                visual_text_color="#fff", symbol_size=12, is_visualmap=True, geo_city_coords=lng_lat)
geo.render("cinema_distribution.html")

#管网节点-压力图
place_v = sorted(zip(place_pressure.values(),place_pressure.keys()),reverse=True)
for i in place_v[1:21]:
    num = float(str(i).split(', ')[0].replace('(',''))
    place_name = str(i).split(', ')[1].replace("')",'').replace("'",'')
    place_20[place_name] = num
DataFrame([place_20.keys()]).to_excel('3.xls')

DataFrame([place_20.values()]).to_excel('4.xls')

plt.figure()
plt.subplot(212)
plt.plot(place_20.keys(),place_20.values())
plt.xticks(rotation=45)
plt.ylabel('管网日均压力')
#时间-压力图
for i in range(0,24):
    time_pressure_mean.append(data[i].mean())
plt.subplot(231)
plt.plot(time_pressure_mean)
plt.plot(data_sum['pressure'],color='black')
plt.xlabel('时间')
plt.ylabel('管网平均压力')
#DataFrame(time_pressure_mean).to_excel('5.xls',sheet_name="压力")
#时间-流量图
for i in range(0,24):
    time_flow_mean.append(data_flow[i].sum())
plt.subplot(232)
plt.plot(time_flow_mean,color='green')
plt.plot(data_sum['flow'],color='black')
plt.plot(data_sum['flow']-time_flow_mean,color='blue')
#DataFrame(time_flow_mean).to_excel('6.xls',sheet_name="流量")
plt.xlabel('时间')
plt.ylabel('管网平均流量')
#时间-温度图
for i in range(0,24):
    time_tem_mean.append(data_tem[i].mean())
plt.subplot(233)
plt.plot(time_tem_mean,color='red')
plt.plot(data_sum['tem'],color='black')
#DataFrame(time_tem_mean).to_excel('7.xls',sheet_name="温度")
plt.xlabel('时间')
plt.ylabel('管网平均温度')

plt.show()






