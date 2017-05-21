# !/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen
from datetime import datetime, timedelta
import time
import json
import redis

BASE_URL = "http://api.socialcron.com.br:5756/"

log = file('dispatcher.log', 'a')
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

datetime_now = datetime.now().utcnow()
now = datetime_now.strftime("%Y-%m-%dT%H:%M") + "-0000"
final = (datetime_now + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M") + "-0000"

log.write('[DEBUG] - Sync executed at %s\n' %(now))

auth_request = Request(BASE_URL + "oauth/token?username=root@root.com&password=root&grant_type=password")
auth_request.add_header("Authorization", "Basic c29jaWFsY3Jvbjpzb2NpYWxjcm9u")
auth_response = json.loads(urlopen(auth_request, data="").read())

if auth_response['expires_in'] <= 120:
  refresh_request = Request(BASE_URL + "oauth/token?grant_type=refresh_token&refresh_token=" + auth_response['refresh_token'])
  refresh_request.add_header("Authorization", "Basic c29jaWFsY3Jvbjpzb2NpYWxjcm9u")
  refresh_request = json.loads(urlopen(refresh_request, data="").read())
  auth_response = refresh_request

posts_request = Request(BASE_URL + "v2/schedules/range/%s/%s" %(now, final))
posts_request.add_header("Authorization", "Bearer " + auth_response['access_token'])
posts_response = json.loads(urlopen(posts_request).read())

for post in posts_response:
 date = datetime.strptime(post['date'], '%Y-%m-%dT%H:%M+0000')
 now_timestamp = int(time.mktime(datetime.now().timetuple()))
 timestamp = int(time.mktime(date.timetuple()))
 diff = timestamp - now_timestamp

 if diff > 60:
   try:
    if not redis.exists('schedule:%s' %(post['id'])):

     photos_request = Request(BASE_URL + "v2/photos/post/" + str(post['post']['id']))
     photos_request.add_header("Authorization", "Bearer " + auth_response['access_token'])
     photos_response = json.loads(urlopen(photos_request).read())

     for photos in photos_response:
      post['post']['photos'] = []
      post['post']['photos'].append(photos)

     redis.set('schedule:%s' %(post['id']), json.dumps(post), diff + 120)
     log.write("[DEBUG] - Schedule id %s stored. Will be posted at %s\n" %(post['id'], post['date']))
   except:
     log.write('[ERROR] - Error on redis\n')

log.flush()
log.close()
