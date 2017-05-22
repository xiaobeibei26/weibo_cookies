# -*- coding:utf-8 -*-
import time
from multiprocessing import Process
from cookie_pool.get_cookie import CookieGenerator
from cookie_pool.tester_cookie import Check_cookie
from cookie_pool.settings import *
CYCLE = 120

'''两个进程，一个定期检验cookie的有效性，
一个定期检验是否有账号没有存储cookie，然
后执行登陆，获得cookie'''


class Scheduler(object):
    @staticmethod
    def get_cookie(cycle=300):
        while True:
            print('正在尝试获取cookie')
            try:
                #'PhantomJS'
                get_newcookie=CookieGenerator('PhantomJS')
                get_newcookie.run()
                print('cookie获取结束,关闭浏览器')
                get_newcookie.close()
                time.sleep(cycle)
            except Exception as e:
                print(e)


    @staticmethod
    def valid_cookie(cycle=3600):#cookie一般不会很快就失效，所以1小时check一次
        while True:
            print('正在测试cookie')
            try:
                tester=Check_cookie()
                tester.run()
                print('cookie测试完毕,关闭浏览器')
                del tester
                time.sleep(cycle)
            except Exception as e:
                print(e)



    def run(self):
        print('cookie池启动')
        if GENERATOR_PROCESS:#检验是否开启了该进程
            generate_process = Process(target=Scheduler.get_cookie)
            generate_process.start()
            # generate_process.join()
        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()
            # valid_process.join()











        # def valid_cookie(cycle=CYCLE):
    #     while True:
    #         print('正在测试cookie')
    #         try:
    #             for
    #
    #
    #
    #         except Exception as e:
    #             print(e)

