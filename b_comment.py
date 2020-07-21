# -*- coding: utf-8 -*-
# !/usr/bin/python3
'''
B站评论监控
@File    :   test2.py
@Time    :   2020/07/11
@Author  :   未闻丶死讯
@Contact :   1761512493@qq.com
'''
import requests
import re
import time
import os
import random
from fake_useragent import UserAgent

ua = UserAgent()
have = []
# 你的b站cookies 不知道怎么获取自己百度

cook = "sid=iltqdyjb; DedeUserID=32482364; DedeUserID__ckMd5=ce93b510ef5be598; SESSDATA=8a59ae8e%2C1604628849%2Cddb89*51; bili_jct=3fda1881cb2b6d0fae6908d3cb614ad0; CURRENT_FNVAL=16; rpdid=|(u|kJJYJ~lY0J'ul)m|~YmJ|; LIVE_BUVID=AUTO8615892797682858"
uid = re.findall("DedeUserID=(.*?);", cook)[0]
csrf = re.findall("bili_jct=(.*?);", cook)[0]

msg_dist = {
    "101037051": "土逼蛋蛋,我来了,",
    "430758745": "jiji我来了 [doge]",
    "81824112": "策导牛逼啊",
    "50212909": "我来了,",
    "11511322": "前来学习",
    "1393437": "八点??",
    "179058253": "小鸟我来了,",
    "1935882": "张坦克我来了,",
    "40433405": "前来学习[doge]",
    "26139491": "胖胖真好看,",
    "437316738": "枯燥[doge]",
    "390461123": "可有蒜,[doge]",
    "20165629": "小团团,[热词系列_知识增加]",
    "9265186": "乔哥,[热词系列_知识增加]",
    "686127": "籽岷大大,[tv_doge]",
    "1962633": "羡慕啊,",
    "5374954": "羡慕啊,",
    "3892132": "羡慕啊,",
    "1928235": "[tv_doge]",
    "193482959": "小孤影,",
    "405017096": "前来学习",
    "1285446":"我康康,银子今天总结了几点,[doge]",
    "2170934":"duang主,",
    "480366389":"希望早日没素材",
    "110904544":"家有小西瓜,[doge]",
    "108569350":"梦泪,永远滴神[doge]",
    "13118294":"木偶大大,[doge]",
    "250858633":"我看今天谁受迫害了,",
    "27669924":"外行员(x) 尾田(v)[doge]",
    "19428259":"大大大叔,",
    "295626593":"mo老ye",
    "94281836":"你,你,你,好骚啊,[doge]",
    "808171":"羡慕啊,",
    "16539048":"羡慕啊,",
    "14110780":"秃凉你来了,",
    "517327498":"罗老师课堂开始了,",
    "4029133":"看着想笑,",
    "52250":"羡慕啊,",
    "295723":"羡慕啊,",
    "777536":"雷电法王,lex",
    "122879":"厂长来了,",
}


def BV_AV(BV):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608
    r = 0
    for i in range(6):
        r += tr[BV[s[i]]] * 58 ** i
    return (r - add) ^ xor


def _Send(BV, msg):
    url = "https://api.bilibili.com/x/v2/reply/add"

    aid = BV_AV(BV)

    data = {
        'oid': f'{aid}',
        'type': '1',
        'message': f'{msg}',
        'plat': '1',
        'jsonp': 'jsonp',
        'csrf': f'{csrf}',
    }
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-length': '114',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': f"{cook}",
        'origin': 'https://www.bilibili.com',
        'referer': f'https://www.bilibili.com/video/{BV}',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': ua.random,
    }

    session = requests.Session()
    if session.post(url=url, data=data, headers=headers).status_code == 200:
        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(_time + "--" + BV + "已评论")
    else:
        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(_time + "--" + BV + "false!!")


def get_BV_list():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': f"{cook}",
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random,
    }
    a = requests.get(
        # url="https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?uid=32482364&type_list=268435455",
        url=f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?uid={uid}&type_list=8",
        headers=headers).json()
    # return re.findall('"bvid":"(.*?)"', a)[:5]
    try:
        a = a['data']['cards'][:5]
    except:
        a=[]
    return a


def save_have():
    global have
    if have:
        with open("hava.txt", "w+") as f:
            for x in have:
                f.write(str(x) + "\n")

    if os.path.exists("hava.txt"):
        with open("hava.txt", "r") as f:
            have = f.read().split("\n")[:-1]


def main():
    global have
    global msg_dist
    i = 0
    while True:
        i += 1
        BV_list = get_BV_list()
        for x in BV_list:
            buid = str(x['desc']['uid'])
            bvid = str(x['desc']['bvid'])
            if bvid not in have:
                if buid in msg_dist:
                    # print(2)
                    print(msg_dist[buid],end='--->>')
                    _Send(bvid, msg_dist[buid])
                else:
                    _Send(bvid, "前来支持,[doge]")
                have.append(bvid)
        if i == 10:
            i = 0
            save_have()
        time.sleep(random.randint(5, 7))


if __name__ == '__main__':
    save_have()
    main()
    # _message="""
# 三连进度▓░░░░░░░░░10%……
# 三连进度▓▓▓░░░░░░░30%……
# 三连进度▓▓▓▓▓░░░░░50%……
# 三连进度▓▓▓▓▓▓▓░░░70%……
# 三连进度▓▓▓▓▓▓▓▓▓░90%……
# 三连进度▓▓▓▓▓▓▓▓▓▓99%……
# 三连失败[doge]
# 下次一定[doge]
# """
# _Send("BV1ra4y1h77c", _message)
