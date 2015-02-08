#coding=utf-8
#!/usr/bin/python

import time
from django.utils import timezone

from redis_exercises.settings import redis_con, MINI_INTERVAL_OF_PV_STATISTICS


class StatisticsMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            redis_con.zadd('users.online', time.time(), request.user.username)

        # 进行PV统计，(MINI_INTERVAL_OF_PV_STATISTICS)秒钟内生重复访问无效
        ip = self.get_remote_ip(request)
        if not redis_con.exists(ip):
            key = timezone.now().strftime('%Y%m%d%H%M')
            pvs = redis_con.hincrby('users.pv', key, 1)

            redis_con.set(ip, 0)
            redis_con.expire(ip, MINI_INTERVAL_OF_PV_STATISTICS)

    def get_remote_ip(self, request):
        return request.META['HTTP_X_FORWARDED_FOR'] if request.META.has_key('HTTP_X_FORWARDED_FOR') else request.META['REMOTE_ADDR']
