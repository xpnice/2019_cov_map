# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # 需另外导入模块Axes 3D
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType
import time
import json
import requests


def get_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(
        time.time()*1000)
    res = json.loads(requests.get(url=url).json()['data'])
    # print(res.keys())
    data = []
    china = res['areaTree'][0]['children']
    for province in china:
        print('正在抓取', province['name'], '的数据')
        for city in province['children']:
            # if city['name'] not in data:#目前无效
            data.append((city['name'], int(city['total']['confirm'])))
    return data


def draw_geo():
    data = get_data()  # 从腾讯爬取数据
    cities = []  # 去除在地图中无对应坐标的城市列表
    geo = (
        Geo()
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(
                title="全国2019-nCoV确诊情况", subtitle="data from Tencent")
        )
        .add_schema(maptype="china")
    )
    for (city, num) in data:
        if not geo.get_coordinate(city):
            print(f'{city}有{num}例确诊，但没有地图坐标对应')
        else:
            cities.append((city, num))
    geo.add(
        "",
        cities,
        type_=ChartType.HEATMAP,  # 热力图
        symbol_size=12,
        blur_size=12,  # 晕染大小
        point_size=10,  # 坐标点大小
        label_opts=opts.LabelOpts(is_show=True))
    geo.render()


if __name__ == '__main__':
    draw_geo()
    # get_data()
