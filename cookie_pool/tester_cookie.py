# -*- coding:utf-8 -*-

import json
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError

from cookie_pool.database import CookiesRedisClient,AccountRedisClient

class Check_cookie(object):
    def __init__(self):
        self.cookies_db = CookiesRedisClient()
        self.account_db = AccountRedisClient()

    def test(self,username,cookies):
        print('正在测试',username,'的cookie')

        try:
            cookies = json.loads(cookies)#变成字典
        except TypeError:
            # Cookie 格式不正确
            print('Invalid Cookies Value', username)
            self.cookies_db.delete(username)
            print('Deleted User', username)
            return None
        try:
            response = requests.get('http://weibo.cn', cookies=cookies)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                title = soup.title.string
                if title == '我的首页':
                    print('有效cookie', username)
                else:
                    print('Title is', title)
                    # Cookie已失效
                    print('失效cookie', username)
                    self.cookies_db.delete(username)
                    print('删除该cookie', username)
        except ConnectionError as e:
            print('Error', e.args)
            print('Invalid Cookies', username)


    def run(self):
        accounts = self.cookies_db.all()
        for account in accounts:
            username = account.get('username')
            cookies = account.get('cookies')
            self.test(username,cookies)


if __name__ == '__main__':
    tester = Check_cookie()



