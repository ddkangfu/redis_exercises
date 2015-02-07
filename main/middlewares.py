#coding=utf-8
#!/usr/bin/python

from redis_exercises.settings import redis_con
import time
import datetime

class StatisticsMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            redis_con.zadd('users.online', time.time(), request.user.username)

        # 进行PV统计，三秒钟内生重复访问无效
        key = datetime.datetime.now().strftime('%Y%m%d%H%M')
        print key
        if not redis_con.hsetnx('users.pv', key, 1):
            pvs = redis_con.hget('users.pv', key)
            redis_con.hset('users.pv', key, int(pvs)+1)
