# -*- coding:utf-8 -*-
import json
from cookie_pool.settings import *
import requests
import time
from cookie_pool.captcha import Yundama
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from .database import CookiesRedisClient, AccountRedisClient



class CookieGenerator(object):
    def __init__(self,browser_type=DEFAULT_BROWSER):

        self.cookies_db = CookiesRedisClient()
        self.account_db =AccountRedisClient()
        self.browser_type= browser_type
        self.ydm = Yundama(YUNDAMA_USERNAME, YUNDAMA_PASSWORD, YUNDAMA_APP_ID, YUNDAMA_APP_KEY)
    def _init_browser(self,browser_type):
        if browser_type == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS#设置请求头
            caps[
                "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)

        elif browser_type =='Chrome':
            self.browser = webdriver.Chrome()
    def suceess_login(self,username):

        wait = WebDriverWait(self.browser, 8)  # 等待浏览器登陆成功跳转
        success = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'me_portrait_w')))
        if success:
            print('登录成功')
            self.browser.get('http://weibo.cn/')

            if "我的首页" in self.browser.title:  # 访问个人主页检验是否登陆成功
                print(self.browser.get_cookies())
                cookies = {}
                for cookie in self.browser.get_cookies():
                    cookies[cookie["name"]] = cookie["value"]
                print(cookies)
                print('成功获取到Cookies')

                return username, json.dumps(cookies)


    def new_cookies(self,username,password):

        print('正在从账号{}获取cookie'.format(username))
        self.browser.delete_all_cookies()
        time.sleep(3)
        self.browser.get('http://my.sina.com.cn/profile/unlogin')
        wait = WebDriverWait(self.browser,15)
        # time.sleep(4)
        try:
            # print(self.browser.)


            login = wait.until(EC.visibility_of_element_located((By.ID, 'hd_login')))
            login.click()
            user = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginformlist input[name="loginname"]')))
            user.send_keys(username)
            psd = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginformlist input[name="password"]')))
            psd.send_keys(password)
            submit = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.login_btn')))
            submit.click()#如果没有验证码就直接登陆了，接下来就检验登陆是否成功
            try:
                time.sleep(1)
                delay=self.browser.find_element_by_class_name('login_error_tips').text
                print(delay)
                if '登陆' in delay:
                    print('遇到登陆限制，进入睡眠一段时间')
                    time.sleep(1800)
                    submit.click()
                name,cook=self.suceess_login(username)
                if name and cook:
                    return name,cook
            except Exception as e:#如果超时，则出现了验证码
                print('出现验证码，开始识别')
                #先找到验证码的图片地址，然后发去在线打码平台
                captcha_info = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginform_yzm .yzm')))
                url = captcha_info.get_attribute('src')
                cookies = self.browser.get_cookies()
                cookies_dict = {}

                for cookie in cookies:
                    cookies_dict[cookie.get('name')] = cookie.get('value')
                response = requests.get(url, cookies=cookies_dict)
                result = self.ydm.identify(stream=response.content)
                if not result:
                    print('验证码识别失败, 跳过识别')
                    return
                door = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginform_yzm input[name="door"]')))
                door.send_keys(result)
                submit.click()
                name, cook = self.suceess_login(username)
                if name and cook:
                    return name,cook


        except WebDriverException as e:#有些账号密码错误我也没有办法

            print('该账号访问失败')

    def set_cookies(self,account):
        try:
            username, cookies = self.new_cookies(account.get('username'), account.get('password'))
            self.cookies_db.set(username,cookies)
        except:
            pass


    def close(self):
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')

    def run(self):#启动获取cookie的主程序
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        accounts = self.account_db.all() # Account 中对应的用户
        cookies = self.cookies_db.all()# Cookies中对应的用户

        valid_users = [cookie.get('username') for cookie in cookies]#找到已经有了cookie的用户，这些用户不用添加
        accounts_name = [account.get('username') for account in accounts]#所有用户
        self._init_browser(browser_type=self.browser_type)
        for user in accounts_name:
            if user not in valid_users:
                self.set_cookies({'username':user,'password':self.account_db.get(user)})

        print('生成器工作完成')

if __name__ == '__main__':
    #'PhantomJS'
    get_newcookie=CookieGenerator()
    get_newcookie.run()


