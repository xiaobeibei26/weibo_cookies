# -*- coding:utf-8 -*-
from cookie_pool.database import AccountRedisClient

'''这里录入账户密码'''

conn = AccountRedisClient()


def set(account):
    username, password = account.split('----')  # 这是因为淘宝店卖的账号密码是用这个符号进行分割的
    result = conn.set(username, password)
    print('账号', username, '密码', password, '录入成功')


def scan():
    f= open('account.txt','r+')
    for i in f:
        set(i.strip())
    f.close()
if __name__ == '__main__':
    scan()



