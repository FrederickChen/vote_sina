#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib
import requests
import random
import uuid
import json
import time
import sys
from datetime import datetime

try:
    import cookielib
except:
    import http.cookiejar as cookielib

headers = {'Host':'support.finance.sina.com.cn',
           'Referer': 'http://finance.sina.com.cn/zt_d/bankpinxuan19/',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
           'Accept': '*/*',
           'Accept-Language': 'zh-CN',
           'Accept-Encoding':'gzip, deflate',
           'Connection': 'Keep-Alive'}

vote_url = 'http://support.finance.sina.com.cn/service/api/openapi.php/VoteService.setVote'
params = {'appid':'yinhangzh19','openid': '','enopenid':'','opflag':'','optime':'','wxflag':'0','captcode':'','roller_id':''}
params['uuid'] = uuid.uuid1().hex
proxies = urllib.request.getproxies()
awards =[
         {'id':'lcxyk19bkzhpxppyh400103','disp': '最佳金融科技银行'},
         {'id':'lcxyk19bkzhpxcxyh400203','disp': '最具创新金融科技银行'},
         {'id':'lcxyk19bkzhpxtyyh400303','disp': '最佳体验金融科技银行'},
         {'id':'lcxyk19bkzhpxsjyh400403','disp': '最佳手机银行'},
         {'id':'lcxyk19bkzhpxhysjyh400503','disp': '最受欢迎手机银行'},
         {'id':'lcxyk19bkzhpxcxsjyh400603','disp': '最具创新手机银行'}
         ]
#Get vote rank
def get_rank(session):
    rank_url = 'http://support.finance.sina.com.cn/service/api/openapi.php/VoteService.getRank'
    post_data='ids=lcxyk19bkzhpxppyh400103,lcxyk19bkzhpxcxyh400203,lcxyk19bkzhpxtyyh400303,lcxyk19bkzhpxsjyh400403,lcxyk19bkzhpxhysjyh400503,lcxyk19bkzhpxcxsjyh400603&appid=yinhangzh19&page=1&pagesize=194'
    headers['Origin'] = 'http://finance.sina.com.cn'
    headers['Content-Type']='application/x-www-form-urlencoded; charset=UTF-8'
    try:
        resp = session.post(rank_url, data=post_data, headers=headers,proxies=proxies)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        return False
    if resp.status_code == 200:
        resp.encoding = resp.apparent_encoding
        json_data = resp.json()
        ranks = json_data['result']['data']['data']
        for award in awards:
            vote = next(rank for rank in ranks if rank["id"] == award['id'] )
            print('    Votes for %s : %d' % (award['disp'],vote['vote']), end='\n')
    return True

#Vote function
#Params: session,id,disp 
def vote_sina(session,id,disp):
    params['id'] = id
    timestamp = int(datetime.now().timestamp()*1000) #time.time()
    params['callback'] = 'jsonp_'+str(timestamp)
    params['_'] = str(timestamp+1)
    try:
        resp = session.get(vote_url, params=params, headers=headers,proxies=proxies)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        return False
    if resp.status_code == 200:
        resp.encoding = resp.apparent_encoding
        data = resp.text.splitlines()[1]
        data = data.split('(')[1]
        data = data[:-1]
        try:
            json_data = json.loads(data)
        except ValueError as e:
            print(e)
            return False
        msg = json_data['result']['data']['msg']
        print("    %s -- %s" % (disp, msg), end='\n')
    return True
#End Vote fuction    

if __name__ == '__main__':
    session = requests.session()
    get_rank(session)
    print('    Vote time: %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='\n')
    for item in awards:
        vote_sina(session,item['id'], item['disp'])
        time.sleep(1)
    get_rank(session) 

