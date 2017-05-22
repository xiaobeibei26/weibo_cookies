# -*- coding:utf-8 -*-
import redis,random



class RedisClient(object):
    def __init__(self,host='127.0.0.1',port='6379',):
        self._db=redis.Redis(host=host,port=port)
        self.name=''


    def _key(self,key):
        return '{name}:{key}'.format(name=self.name,key=key)
    def keys(self):
        """
        得到所有的键名
        :return:
        """
        return self._db.keys('{name}:*'.format(name=self.name))

    def flush(self):
        """
        清空数据库, 慎用
        :return:
        """
        self._db.flushall()


class AccountRedisClient(RedisClient):
    def __init__(self):
        RedisClient.__init__(self)
        self.name='account'

    def set(self,key,value):
        try:
            return self._db.set(self._key(key),value)
        except:
            print('账户密码插入有误')
            pass
    def get(self,key):

        try:
            return self._db.get(self._key(key)).decode('utf-8')
        except:
            print('没有账户密码')
            pass
    def all(self):
        try:
            for key in self._db.keys('{name}:*'.format(name=self.name)):

                group = key.decode('utf-8').split(':')
                if len(group) == 2:
                    username = group[1]
                    yield {
                        'username':username,
                        'password':self.get(username)
                    }
        except Exception as e:
            print(e)


    def delete(self,key):
        try:
            return self._db.delete(self._key(key))

        except:
            print('删除失败')


class CookiesRedisClient(RedisClient):
    def __init__(self):
        RedisClient.__init__(self)
        self.name='cookies'

    def set(self,key,value):
        try:
            self._db.set(self._key(key),value)
            print('一条cookie插入成功')
        except:
            print('cookie存储失败')
    def get(self,key):
        try:
            return self._db.get(self._key(key)).decode('utf-8')
        except:
            pass


    def delete(self,key):
        try:
            print('删除用户{}的cookie'.format(key))
            return self._db.delete(self._key(key))
        except:
            print('删除失败')


    def random(self):
        try:
            keys = self.keys()
            return self._db.get(random.choice(keys))
        except:
            print('没有cookie可以获得')


    def all(self):
        """
        获取所有账户, 以字典形式返回
        :return:
        """
        try:
            for key in self._db.keys('{name}:*'.format(name=self.name)):
                group = key.decode('utf-8').split(':')
                if len(group) ==2:
                    username=group[1]
                    yield {
                        'username':username,
                        'cookies':self.get(username)
                    }

        except Exception as e:
            print(e)

    def count(self):
        return len(self.keys())

if __name__ == '__main__':
    conn = AccountRedisClient()

    # print(conn.get('j21522@163.com'))
    for i in conn.all():
        print(i)







