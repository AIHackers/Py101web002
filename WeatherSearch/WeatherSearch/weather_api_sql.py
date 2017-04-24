# -*- coding: utf-8 -*-

import requests
from WeatherData.models import Data

Data.objects.all().delete()

class GetData:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def city_data(self, keyword):
        r = requests.get(self.api_url, params={
            'key':self.api_key,
            'location':keyword
        }) #温度默认为 c（摄氏度）
        data = r.json()
        return data

class WeatherSearch:
    def __init__(self, api_url, api_key): #两个下划线
        self.api_url = api_url
        self.api_key = api_key

    def weather(self, keyword):

        data = GetData(self.api_url, self.api_key).city_data(keyword)
        if 'status_code' in data:
            p = "{}暂无数据".format(keyword)
            return p
        else:
            text = data['results'][0]['now']['text']
            code = data['results'][0]['now']['code']
            temperature = data['results'][0]['now']['temperature']
            last_update = data['results'][0]['last_update']
            if keyword not in Data.objects.all():
                data_inserted = Data(city=keyword, text=text, code=code, temperature=temperature, last_update=last_update)
                data_inserted.save()
            else:
                Data.objects.filter(city=keyword).update(text=text, code=code, temperature=temperature, last_update=last_update)

        query_data = Data.objects.get(city=keyword)
        p = '{}的天气为{}, 温度为{}摄氏度，更新时间为：{}'.format(
                    keyword,
                    query_data.text,
                    query_data.temperature,
                    query_data.last_update)
        return p


    def get_help(self):
        p = ['输入城市名，点击 查询 获得该城市的天气；',
            '点击 帮助, 获取帮助文档；',
            '点击 历史，获取查询历史；']
        return p

    def history(self):
        record = []
        all_data = Data.objects.all()
        if len(all_data) == 0:
            p = ["暂无查询历史"]
            return p
        else:
            for i in all_data:
                p = '{}的天气为{}, 温度为{}摄氏度，更新时间为{}。'.format(i.city,i.text,i.temperature,i.last_update)
                print(p)
                record.append(p)
        return record

if __name__ == "__main__":
    url = 'https://api.thinkpage.cn/v3/weather/now.json'
    key = 'tgypbgrcnda2arbz'
    WeatherSearch(url, key)
