import json
import re

from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
def show(request):
    if request.method == 'GET':
        resq = HttpResponseRedirect('/movies/search/1')

        resq.delete_cookie('keyword')
        return resq
    elif request.method == 'POST':
        resq = HttpResponseRedirect('/movies/show')

        return resq


def search(request, name):
    if request.method == 'GET':
        if len(name)==1:
            if name=='h':
                title="本周热播:"
            elif name=='m':
                title="最新电影:"
            elif name == 't':
                title = "最新连续剧:"
            elif name == 's':
                title = "最新综艺:"
            elif name == 'c':
                title = "最新动漫:"

            import requests

            headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
             }

            url = 'https://vip.88-spa.com:8443/v1/home-list'
            response = requests.get(url, headers=headers)

            json_data = response.json()

            while (len(json_data[name]) % 3):
                json_data[name].append([])


            return render(request, 'search.html', {'json': json_data[name],'title':title})
        else:
            if name=='movie':
                title="本周电影排行榜:"
            elif name=='show':
                title="本周综艺排行榜:"
            elif name == 'teleplay':
                title = "本周电视剧排行榜:"
            import requests

            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
            }

            url = 'https://vip.88-spa.com:8443/v1/rank-list?cate=vod_hits_week'
            response = requests.get(url, headers=headers)

            json_data = response.json()

            while (len(json_data[name]) % 3):
                json_data[name].append([])


            return render(request, 'search.html', {'json': json_data[name], 'title': title})


    elif request.method == 'POST':
        get_name = request.POST['name']

        import requests

        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
        }

        from urllib import parse
        keyword = parse.quote(get_name)
        url = 'https://vip.88-spa.com:8443/v1/auto-search?keyword=' + keyword
        response = requests.get(url, headers=headers)

        json_data = response.json()

        while (len(json_data['data']) % 3):
            json_data['data'].append([])

        return render(request, 'show.html', {'json': json_data['data']})


def about(request, url):
    if request.method == 'GET':
        import requests

        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
        }
        url1 = 'https://vip.88-spa.com:8443/v1/vod-details?id=' + url

        response = requests.get(url1, headers=headers)
        json1 = response.json()
        json2 = list(json1.get('vod').get('VodPlayUrls').values())
        while (len(json1['rand']) % 3):
            json1['rand'].append([])
        while (len(json1['relate']) % 3):
            json1['relate'].append([])

        res = render(request, 'about.html', {'json': json1, 'json2': json2})

        return res


def play(request):
    if request.method == 'GET':
        url = request.GET.get('url', None)
        vodname = request.GET.get('name', None)



        print(vodname)
        if re.match('http+[\S*]+.m3u8', url):
            urls = re.findall(r'=http+[\S*]+.m3u8', url)
            urlss = re.findall(r'http+[\S*]+.m3u8', urls[0])

            return render(request, 'play.html', {"urls": vodname, 'url': urlss[0]})
        else:
            urls = re.findall(r'=http+[\S*]+.html', url)
            urlss = re.findall(r'http+[\S*]+.html', urls[0])

            return render(request, 'play.html', {"urls": vodname, 'url': urlss[0]})
