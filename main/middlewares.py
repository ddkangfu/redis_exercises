#coding=utf-8
#!/usr/bin/python

from redis_exercises.settings import redis_con
import time
from django.utils import timezone

class StatisticsMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            redis_con.zadd('users.online', time.time(), request.user.username)

        # 进行PV统计，三秒钟内生重复访问无效
        ip = request.META['HTTP_X_FORWARDED_FOR'] if request.META.has_key('HTTP_X_FORWARDED_FOR') else request.META['REMOTE_ADDR']
        if not redis_con.exists(ip):
            key = timezone.now().strftime('%Y%m%d%H%M')
            pvs = redis_con.hincrby('users.pv', key, 1)

            redis_con.set(ip, 0)
            redis_con.expire(ip, 3)
