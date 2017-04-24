# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf
from . import weather_api_sql



# 接收POST请求数据
def search_post(request):
    url = 'https://api.thinkpage.cn/v3/weather/now.json'
    key = 'tgypbgrcnda2arbz'
    weather_get_api = weather_api_sql.WeatherSearch(url, key)
    ctx ={}
    if request.POST:
        if request.POST['button'] == '查询':
            input_city = request.POST['city']
            display_content = weather_get_api.weather(input_city)
            ctx['display_content'] = display_content
        elif request.POST['button'] == '历史':
            history_text = weather_get_api.history()
            ctx['history_text'] = history_text
        elif request.POST['button'] == '帮助':
            help_text = weather_get_api.get_help()
            ctx['help_text'] = help_text
    else:
        ctx = {}

    return render(request, "search_weather.html", ctx)
