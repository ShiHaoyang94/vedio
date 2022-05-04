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


def search(request):
    if request.method == 'GET':

        return render(request, 'search.html')

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

        res = render(request, 'about.html', {'json': json1,'json2':json2})

        return res
    if request.method == 'POST':
        url=request.POST['url']


        if re.match('http+[\S*]+.m3u8',url):
            urls = re.findall(r'=http+[\S*]+.m3u8', url)
            urlss = re.findall(r'http+[\S*]+.m3u8', urls[0])
            print(urlss[0])

            return render(request, 'play.html', {'url': urlss[0]})
        else:
            urls = re.findall(r'=http+[\S*]+.html', url)
            urlss = re.findall(r'http+[\S*]+.html', urls[0])
            print(urlss[0])

            return render(request, 'play.html', {'url': urlss[0]})


def play(request, url):
    if request.method == 'GET':
        res = render(request, 'play.html', {'url': url})
        return res


