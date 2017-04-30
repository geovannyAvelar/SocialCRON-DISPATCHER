# !/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen
from datetime import datetime
import redis
import json

BASE_URL = "http://api.socialcron.com.br:5756/"

redis = redis.StrictRedis(host='localhost', port=6379, db=0)

now = datetime.now().strftime("%Y-%m-%d")

auth_request = Request(BASE_URL + "oauth/token?username=root@root.com&password=root&grant_type=password")
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
  try:
    redis.set(post['id'], json.dumps(posts_response))
  except:
    pass
