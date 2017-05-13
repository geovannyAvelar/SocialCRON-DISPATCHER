# !/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen
from datetime import datetime
import time
import redis
import json

BASE_URL = "http://api.socialcron.com.br:5756/"

log = file('dispatcher.log', 'a')
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

datetime_now = datetime.now()
now = datetime_now.strftime("%Y-%m-%d")

log.write('Sync executed at %s\n' %(datetime_now.strftime("%Y-%m-%dT%H:%M%S%z")))

auth_request = Request(BASE_URL + "oauth/token?username=geovanny.avelar@gmail.com&password=root&grant_type=password")
auth_request.add_header("Authorization", "Basic c29jaWFsY3Jvbjpzb2NpYWxjcm9u")
auth_response = json.loads(urlopen(auth_request, data="").read())

if auth_response['expires_in'] <= 120:
  refresh_request = Request(BASE_URL + "oauth/token?grant_type=refresh_token&refresh_token=" + auth_response['refresh_token'])
  refresh_request.add_header("Authorization", "Basic c29jaWFsY3Jvbjpzb2NpYWxjcm9u")
  refresh_request = json.loads(urlopen(refresh_request, data="").read())
  auth_response = refresh_request

posts_request = Request(BASE_URL + "v2/schedules/day/" + now)
posts_request.add_header("Authorization", "Bearer " + auth_response['access_token'])
posts_response = json.loads(urlopen(posts_request).read())

for post in posts_response:
 date = datetime.strptime(post['date'], '%Y-%m-%dT%H:%M+0000')
 now_timestamp = int(time.mktime(datetime.now().timetuple()))
 timestamp = int(time.mktime(date.timetuple()))
 diff = timestamp - now_timestamp

 if diff > 60:
   try:
    redis.set('schedule:%s' %(post['id']), json.dumps(posts_response), diff)
    log.write("[DEBUG] - Schedule id %s stored. Will be posted at %s\n" %(post['id'], post['date']))
   except:
     log.write('[ERROR] - Error on redis\n')

log.flush()
log.close()

