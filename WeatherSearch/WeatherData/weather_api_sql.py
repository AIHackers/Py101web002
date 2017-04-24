# -*- coding: utf-8 -*-

import requests
import sqlite3

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

class sql_data:
    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(self.filename, check_same_thread=False)
        self.c = self.conn.cursor()
        #判断表 city_weather 是否存在
        self.c.execute("SELECT * FROM sqlite_master where type='table' and name='city_weather'")
        if len(self.c.fetchall()) == 0:
            self.c.execute('CREATE TABLE city_weather(city, weather_text, weather_code, temperature, last_update)')
            self.conn.commit()
        else:
            self.c.execute('DELETE FROM city_weather')#清空所有行数据
            self.conn.commit()

    def insert_data(self, keyword, text, code, temperature, last_update):
        #使用变量插入值，需使用占位符；data 要是元组
        self.c.execute('INSERT INTO city_weather VALUES (?,?,?,?,?)', (keyword, text, code, temperature, last_update))
        self.conn.commit()

    def select_data(self, data):
        self.c.execute('SELECT ? FROM city_weather', (data,))#带上括弧和逗号，形成元组
        return self.c.fetchall()

    def select_all(self):
        self.c.execute('SELECT * FROM city_weather')
        return self.c.fetchall()

    def select_all_where(self, where):
        self.c.execute('SELECT * FROM city_weather WHERE city=?',(where,))
        return self.c.fetchone()

    def update_data(self, city_name, change_text):
        self.c.execute("UPDATE city_weather SET weather_text = ? WHERE city = ?", (change_text, city_name, ))#用元组
        self.conn.commit()

    def close_database(self):
        self.conn.close()


class search_weather:
    def __init__(self, api_url, api_key): #两个下划线
        self.api_url = api_url
        self.api_key = api_key

    def weather(self, keyword):
        #判断表中是否已有数据
        cities_tup = database.select_data('city')
        keyword_tup = (keyword,)
        if keyword_tup not in cities_tup:
            data = get_api(self.api_url, self.api_key).get_data(keyword)
            if 'status_code' in data:
                p = "{}暂无数据".format(keyword)
                return p
            else:
                text = data['results'][0]['now']['text']
                code = data['results'][0]['now']['code']
                temperature = data['results'][0]['now']['temperature']
                last_update = data['results'][0]['last_update']
                database.insert_data(keyword, text, code, temperature, last_update)

        tup = database.select_all_where(keyword)
        p = '{}的天气为{}, 温度为{}摄氏度，更新时间为：{}'.format(
                    keyword,
                    tup[1],
                    tup[3],
                    tup[4])
        return p


    def get_help(self):
        p = ['输入城市名，点击 查询 获得该城市的天气；',
            '点击 帮助, 获取帮助文档；',
            '点击 历史，获取查询历史；']
        return p

    def history(self):
        record = []
        all_data = database.select_all()
        if all_data == []:
            record = ["暂无查询历史"]
        else:
            for row in all_data:
                p = '{}的天气为{}, 温度为{}摄氏度，更新时间为{}。'.format(row[0],row[1],row[3],row[4])
                record.append(p)
        return record

    def change_weather(self, updata_info):
        l = updata_info.split(' ')
        city = l[0]
        text = l[1]
        database.update_data(city, text)
        tup = database.select_all_where(city)
        p = '{}的天气为{}, 温度为{}摄氏度，更新时间为：{}'.format(
                    city,
                    tup[1],
                    tup[3],
                    tup[4])
        return p

class update_weather:
    def __init__(self, api_url, api_key, t):
        self.api_url = api_url
        self.api_key = api_key
        self.t = t
        flag = True
        while flag:
#            lock.acquire()
            if database.select_data('city') == []:
#                lock.release()
                continue #明确流程控制
            else:
                flag = False
#                lock.release()
        else:
            time.sleep(self.t)
#            lock.acquire()
            cities_tup = database.select_data('city')
#            lock.release()
            for i in range(len(cities_tup)):
                city = cities_tup[i][0]
                data = get_api(self.api_url, self.api_key).get_data(city)
                text = data['results'][0]['now']['text']
                code = data['results'][0]['now']['code']
                temperature = data['results'][0]['now']['temperature']
                last_update = data['results'][0]['last_update']
                database.insert_data(city, text, code, temperature, last_update)

database = sql_data('weather.db')

if __name__ == "__main__":
    url = 'https://api.thinkpage.cn/v3/weather/now.json'
    key = 'tgypbgrcnda2arbz'
    search_weather(url, key)
