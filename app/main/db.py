# @Time    : 2018/8/1 上午7:00
# @Author  : idri
# @File    : room_message.py
# @Software: PyCharm
import redis


class Rdb:
    """ 发布订阅模式 """

    def __init__(self):
        self.rcon = redis.StrictRedis(host='localhost', db=5)
        self.rcon.set('chat:hall', '')

    def save(self, room, msg):
        #  ( name, value, ex=None, px=None, nx=False, xx=False):
        try:
            self.rcon.append('chat:{}'.format(room), msg)
        except Exception as e:
            return 'Save Error'

    def get_msg(self, room):
        return self.rcon.get('chat:{}'.format(room))
