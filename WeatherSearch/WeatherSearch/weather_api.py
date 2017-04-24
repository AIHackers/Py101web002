# -*- coding: utf-8 -*-
# 面向对象编程

import requests
import datetime
import time

class get_api:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def get_data(self, keyword):
        r = requests.get(self.api_url, params={
            'key':self.api_key,
            'location':keyword
        }) #温度默认为 c（摄氏度）
        data = r.json()
        return data


class search_weather:
    def __init__(self, api_url, api_key): #两个下划线
        self.api_url = api_url
        self.api_key = api_key
        self.record = []

    def weather(self, keyword):
        data = get_api(self.api_url, self.api_key).get_data(keyword)
        if 'status_code' in data:
            p = "{}暂无数据".format(keyword)
            return p
        else:
            p = '{}的天气为{}, 温度为{}摄氏度。'.format(
                    keyword,
                    data['results'][0]['now']['text'],
                    data['results'][0]['now']['temperature'])
            # html显示中，\n 并不会读为回车，只能从 html 上改变
            p = p + '更新时间为：{}'.format(data['results'][0]['last_update'])
            self.record.append(p)
            return p

    def quit(self):
        exit()

    def get_help(self):
        p = ['输入城市名，点击 查询 获得该城市的天气；',
            '点击 帮助, 获取帮助文档；',
            '点击 历史，获取查询历史；']
        return p

    def history(self):
        if self.record == []:
            p = ["暂无查询历史"]
        else:
            p = self.record
        return p

    def time(self):
        input_day = input('请按照格式（2017年1月1日，输入：\'2017-01-01\'），输入设定的日期：')
        input_time = input('请按照格式（18点30分30秒，输入\'18:30:30\'），输入设定的时间：')
        keyword = input('请输入设定的城市名：')
        now_time = datetime.datetime.now()
        day_time = input_day + ' ' + input_time
        set_time = datetime.datetime.strptime(day_time, '%Y-%m-%d %H:%M:%S')
        sleep_time = int((set_time - now_time).total_seconds())
        time.sleep(sleep_time) #必须是整数
        self.weather(keyword)


if __name__ == "__main__":
    url = 'https://api.thinkpage.cn/v3/weather/now.json'
    key = 'tgypbgrcnda2arbz'
    search_weather(url, key)
