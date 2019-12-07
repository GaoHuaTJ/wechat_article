# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 21:51:21 2019
@author: Administrator
"""

import requests
import json
import time
import random

url='http://mp.weixin.qq.com/mp/profile_ext'


def get_wx_article(biz,uin,key,pass_ticket,appmsg_token,index,count=10):
    offset=1+(index+1)*11
    params={
        '__biz':biz,
        'uin':uin,
        'key':key,
        'offset':offset,
        'count':count,
        'action':'getmsg',
        'f':'json',
        'pass_ticket':pass_ticket,
        'scene':124,
        'is_ok':1,
        'appmsg_token':appmsg_token,
        'x5':0,
    }

    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }

    r=requests.get(url=url, params=params, headers=headers)

    resp_json=r.json()
    if resp_json.get('errmsg') == 'ok':
        # 是否还有分页数据，若没有更多数据则返回
        can_msg_continue=resp_json['can_msg_continue']
        # 当前分页文章数
        msg_count=resp_json['msg_count']
        print("当前分页共有{}篇文章".format(msg_count))
        general_msg_list=json.loads(resp_json['general_msg_list'])
        infolist=general_msg_list.get('list')
        print(infolist, "\n**************")
        for info in infolist:
            try:
                app_msg_ext_info=info['app_msg_ext_info']
                # 标题
                title=app_msg_ext_info['title']
                # 文章链接
                content_url=app_msg_ext_info['content_url']
                # 封面图
                cover=app_msg_ext_info['cover']
                # 发布时间
                datetime=info['comm_msg_info']['datetime']
                datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datetime))
                print(title,datetime)
            except Exception as e:
                print(e.args[-1])
                pass


        if can_msg_continue==1:
            return True
        return False
    else:
        print('获取文章异常...')
        return False


if __name__ == '__main__':
    # 参数通过抓包获得
    biz='MzAxNzMxNzgxMQ=='
    uin='MjM0Mzg1NDYzMw%3D%3D'
    key='e2a6a5ccea4b8ce4ceb1e7ca61ade949ca2962200e70338f21b844ce7fc06ccdc7f74d15fd4415aaebe4a263e9c1fe961036ef9f6a7c0985bf9043c4977666fd7a92f8d14d0b750f11b84b173947fae1'
    pass_ticket='QDbhJ0WvMxQceSKqddu3WaZHT3fp0mXLS%252BkiMOil2SPiMGL8yAOmPcrFYfyx1XHP'
    appmsg_token='1038_3sBF5sWNlswPjJp68Gp8X0MKqJeox1wvY2CK8-bCn7ntUP7klsuqJYr-97s3nOntzQOTcVzIviSPS5R8'
    index=-1
    while 1:
        print(f'开始抓取公众号第{index + 1} 页文章.')
        flag=get_wx_article(biz,uin,key,pass_ticket,appmsg_token,index=index)
        # 防止和谐，暂停8秒
        time.sleep(8)
        index+=1
        print(flag)
        if flag==False:
            print('该公众号文章已全部抓取并且存入本地数据库')
            break
        print(f'..........准备抓取公众号第 {index+2} 页文章.')