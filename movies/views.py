import json

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

def search(request,page):
    if request.method == 'GET':
        if request.COOKIES.get('keyword'):
            name=request.COOKIES.get('keyword')
            import requests

            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
            }
            i = page
            keyword = name
            url = 'http://app.ouyangpeng.top/app/poncon-movie/api/search.php?keyword=' + keyword + '&page=' + str(i)
            response = requests.get(url, headers=headers)
            json_data = response.json()
            while (len(json_data['list']) % 3):
                json_data['list'].append([])






            return render(request, 'show.html', {'json': json_data['list'], 'page': page + 1})
        else:
            return render(request, 'search.html')

    elif request.method == 'POST':
        get_name = request.POST['name']




        import requests

        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
        }
        i = page
        keyword = get_name
        url = 'http://app.ouyangpeng.top/app/poncon-movie/api/search.php?keyword=' + keyword + '&page=' + str(i)
        response = requests.get(url, headers=headers)
        json_data = response.json()
        while(len(json_data['list'])%3):

            json_data['list'].append([])



        res = render(request, 'show.html', {'json': json_data['list'], 'page': page + 1})
        res.set_cookie('keyword',keyword)

        return res

def about(request,url,urls):
    if request.method == 'GET':
        import requests

        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
        }
        url1='http://app.ouyangpeng.top/app/poncon-movie/api/movieInfo.php?url='+'/'+url+'/'+urls

        response = requests.get(url1, headers=headers)
        json1 = response.json()
        res = render(request, 'about.html', {'json': json1})
        return res
    elif request.method == 'POST':
        resq = HttpResponseRedirect('/movies/search/1')


        return resq

def play(request,url):
    if request.method == 'GET':
        import requests

        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
        }
        url1 = 'http://app.ouyangpeng.top/app/poncon-movie/api/playData.php?url=/play/' + url

        response = requests.get(url1, headers=headers)
        json1 = response.json()
        res = render(request, 'play.html', {'json': json1})
        return res
    elif request.method == 'POST':
        resq = HttpResponseRedirect('/movies/search/1')
        return resq