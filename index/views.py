import os.path

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import requests, re
from django.contrib import messages

# Create your views here.
from vedio import settings


def index(request):
    if request.method == 'GET':

        return render(request, 'index.html')

    elif request.method == 'POST':
        resq = HttpResponseRedirect('/index')

        resq.delete_cookie('web')
        get_web = request.POST['web']
        if re.match("^http", get_web):

            resq.set_cookie('web', get_web, 60 * 60 * 2)

            moren_web = "https://z1.m1907.cn/?jx="

            last_web = moren_web + get_web

            resq.set_cookie('last_web', last_web, 60 * 60 * 2)

            return resq
        else:

            messages.error(request, "解析网址格式错误,请重新输入")

            return HttpResponseRedirect('/index')


def indexs(request, name):
    if request.method == 'GET':
        play_line_json = [
            {"name": "纯净1", "url": "https://z1.m1907.cn/?jx=", "t": "m"},
            {"name": "B站1", "url": "https://vip.parwix.com:4433/player/?url=", "t": "m"},
            {"name": "爱跟", "url": "https://vip.2ktvb.com/player/?url=", "t": "m"},
            {"name": "爱豆", "url": "https://jx.aidouer.net/?url="},
            {"name": "BL", "url": "https://vip.bljiex.com/?v="},
            {"name": "冰豆", "url": "https://api.qianqi.net/vip/?url="},
            {"name": "百域", "url": "https://jx.618g.com/?url="},
            {"name": "CK", "url": "https://www.ckplayer.vip/jiexi/?url="},
            {"name": "CHok", "url": "https://www.gai4.com/?url="},
            {"name": "ckmov", "url": "https://www.ckmov.vip/api.php?url="},
            {"name": "大幕", "url": "https://jx.52damu.com/dmjx/jiexi.php?url="},
            {"name": "迪奥", "url": "https://123.1dior.cn/?url="},
            {"name": "H8", "url": "https://www.h8jx.com/jiexi.php?url="},
            {"name": "江湖", "url": "https://api.jhdyw.vip/?url=", "t": "m"},
            {"name": "解析", "url": "https://ckmov.ccyjjd.com/ckmov/?url="},
            {"name": "解析la", "url": "https://api.jiexi.la/?url="},
            {"name": "九八", "url": "https://jx.youyitv.com/?url="},
            {"name": "LE", "url": "https://lecurl.cn/?url="},
            {"name": "老板", "url": "https://vip.laobandq.com/jiexi.php?url="},
            {"name": "乐多", "url": "https://api.leduotv.com/wp-api/ifr.php?isDp=1&vid=", "t": "m"},
            {"name": "MAO", "url": "https://www.mtosz.com/m3u8.php?url="},
            {"name": "M3U8", "url": "https://jx.m3u8.tv/jiexi/?url="},
            {"name": "MUTV", "url": "https://jiexi.janan.net/jiexi/?url="},
            {"name": "诺诺", "url": "https://www.ckmov.com/?url="},
            {"name": "诺讯", "url": "https://www.nxflv.com/?url="},
            {"name": "OK", "url": "https://okjx.cc/?url="},
            {"name": "PM", "url": "https://www.playm3u8.cn/jiexi.php?url="},
            {"name": "盘古", "url": "https://www.pangujiexi.cc/jiexi.php?url="},
            {"name": "奇米", "url": "https://qimihe.com/?url="},
            {"name": "全民", "url": "https://jx.blbo.cc:4433/?url="},
            {"name": "RDHK", "url": "https://jx.rdhk.net/?v=", "t": "m"},
            {"name": "思云", "url": "https://jx.ap2p.cn/?url="},
            {"name": "思古3", "url": "https://jsap.attakids.com/?url="},
            {"name": "淘电影", "url": "https://jx.vodjx.top/vip/?url="},
            {"name": "听乐", "url": "https://jx.dj6u.com/?url=", "t": "m"},
            {"name": "维多", "url": "https://jx.ivito.cn/?url="},
            {"name": "虾米", "url": "https://jx.xmflv.com/?url="},
            {"name": "小蒋", "url": "https://www.kpezp.cn/jlexi.php?url="},
            {"name": "云端", "url": "https://sb.5gseo.net/?url="},
            {"name": "云析", "url": "https://jx.yparse.com/index.php?url="},
            {"name": "0523", "url": "https://go.yh0523.cn/y.cy?url="},
            {"name": "17云", "url": "https://www.1717yun.com/jx/ty.php?url="},
            {"name": "4K", "url": "https://jx.4kdv.com/?url=", "t": "m"},
            {"name": "8090", "url": "https://www.8090g.cn/?url="}
        ]

        resq = HttpResponseRedirect('/index')

        resq.delete_cookie('last_web')

        try:
            request.COOKIES.get('web')
            last_web = play_line_json[int(name)].get('url') + request.COOKIES.get('web')
        except Exception as e:

            last_web = play_line_json[int(name)].get('url')

        resq.set_cookie('last_web', last_web, 60 * 60 * 2)

        return resq

    elif request.method == 'POST':
        resq = HttpResponseRedirect('/index')

        resq.delete_cookie('last_web')

        get_web = request.POST['web']
        moren_web = "https://z1.m1907.cn/?jx="

        last_web = moren_web + get_web

        resq.set_cookie('last_web', last_web, 60 * 60 * 2)
        return resq


def tiyu(request, name):
    if request.method == 'GET':
        play_line_json = [
            {"name": "人人体育", "url": "http://www.rrty36.com/home"},
            {"name": "咪咕体育", "url": "https://www.miguvideo.com/mgs/website/prd/sportsHomePage.html?from=001"},

        ]

        return render(request, 'tiyu.html', {'web': play_line_json[int(name) - 1].get('url')})


def douyin(request):
    if request.method == 'GET':

        return render(request, 'douyin.html')

    elif request.method == 'POST':

        try:

            get_url = request.POST['web']
            urls = re.findall(r'https://v.douyin.com/[A-Za-z0-9]*/', get_url)
            share_url = urls[0]

            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
            }
            response = requests.get(share_url, headers=headers)
            url = response.url  # 处理页面重定向，提取新连接
            id = re.search(r'/video/(.*?)/', url).group(1)  # 获取视频id

            # 提取带水印的视频链接地址
            url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + id
            response = requests.get(url, headers=headers)
            json = response.json()

            download_url = json['item_list'][0]['video']['play_addr']['url_list'][0].replace('wm', '')

            return render(request, 'douyin.html', {'url': download_url})
        except Exception as e:
            return HttpResponseRedirect('/busy')


def elsfk(request):
    if request.method == 'GET':
        return render(request, 'elsfk.html')


def xbw(request):
    if request.method == 'GET':
        return render(request, 'xbw.html')


def words(request):
    if request.method == 'GET':

        return render(request, 'words.html')

    elif request.method == 'POST':
        import base64
        import requests
        from datetime import datetime
        print(datetime.now())
        try:
            file_name = request.FILES['file_name']
            file_names = os.path.join(settings.MEDIA_ROOT, request.session.get('username'))
            with open(file_names, 'wb') as f:
                data = file_name.file.read()
                f.write(data)

            # 获取access_token
            # client_id 为官网获取的AK， client_secret 为官网获取的SK
            appid = '26149347'
            client_id = 'M9LCsi0v2Q9wHTDDiFQH8R06'
            client_secret = 'TasRoL1atapwOvwkdzNK9u67ctqM0NG7'
            print("appid:" + appid)
            print("client_id:" + client_id)
            print("client_secret:" + client_secret)

            token_url = "https://aip.baidubce.com/oauth/2.0/token"
            host = f"{token_url}?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

            response = requests.get(host)
            access_token = response.json().get("access_token")

            # 调用通用文字识别高精度版接口
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
            # 以二进制方式打开图文件
            # 参数image：图像base64编码
            # 下面图片路径请自行切换为自己环境的绝对路径
            with open(file_names, "rb") as f:
                image = base64.b64encode(f.read())

            body = {
                "image": image,
                "language_type": "auto_detect",
                "detect_direction": "true",
                "paragraph": "true",
                "probability": "true",
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            request_url = f"{request_url}?access_token={access_token}"
            response = requests.post(request_url, headers=headers, data=body)
            content = response.json()
            print(content)
            os.remove(file_names)
            # 打印调用结果

            return render(request, 'words.html', {'words': content['words_result']})

        except Exception as e:

            messages.success(request,
                             "图片不为空，现阶段我们支持的图片格式为：PNG、JPG、JPEG、BMP，请进行转码或更换图片，现阶段我们支持的图片大小为：base64编码后小于4M，分辨率不高于4096*4096，请重新上传图片，现阶段不支持 10M 或以上的数据包")

            return HttpResponseRedirect('/index/words/')


def laji(request):
    if request.method == 'GET':

        return render(request, 'laji.html')

    elif request.method == 'POST':
        name = request.POST['names']
        app_id = 'lcau18holcsotnrg'
        app_secret = 'TjBhTUpiZEpSZlAxSlVIc09IRWQ2UT09'
        from urllib import parse
        keyword = parse.quote(name)
        url = 'https://www.mxnzp.com/api/rubbish/type?name=' + keyword + '&app_id=' + app_id + '&app_secret=' + app_secret
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        jsons = response.json()
        return render(request, 'laji.html', {'jsons': jsons.get("data")})


def main(request):
    if request.method == 'GET':
        return render(request, 'main.html')

