# -*- coding:utf-8 -*-

DEFAULT_BROWSER='Chrome'#默认用于登陆的浏览器

# 云打码相关配置到yundama.com申请注册，这个是开发者账号
YUNDAMA_USERNAME = ''#用户名
YUNDAMA_PASSWORD = ''#密码
YUNDAMA_APP_ID = '3523'
YUNDAMA_APP_KEY = '6916d827de5e35e6e807c39bdaeab49d'

YUNDAMA_API_URL = 'http://api.yundama.com/api.php'

# 云打码最大尝试次数
YUNDAMA_MAX_RETRY = 20


# 进程开关
# 产生器，模拟登录添加Cookies
GENERATOR_PROCESS = False
# 验证器，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
