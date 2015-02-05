#coding=utf-8
#!/usr/bin/python

from redis_exercises.settings import redis_con
import time

class StatisticsMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            redis_con.zadd('users.online', time.time(), request.user.username)
