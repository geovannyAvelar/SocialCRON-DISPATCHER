# !/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from urllib2 import Request, urlopen
from datetime import datetime, timedelta
from threading import Thread
import json
import redis

BASE_URL = "http://api.socialcron.com.br:5756/"

log = file('dispatcher.log', 'a')
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

datetime_now = datetime.now().utcnow()
one_minute_after = datetime_now + timedelta(minutes = 1)

log.write('[DEBUG] - Dispatch executed at %s\n' %(datetime_now.strftime("%Y-%m-%dT%H:%M:%S%z")))

schedules_keys = redis.keys('*')

for key in schedules_keys:
  schedule = json.loads(redis.get(key))
  schedule_date = datetime.strptime(schedule['date'][0:-5], "%Y-%m-%dT%H:%M")

  if schedule_date > datetime_now and schedule_date < one_minute_after:

    photos_ids = []

    if 'photos' in  schedule['post']:
      for photo in schedule['post']['photos']:
        fb_photo_data = urllib.urlencode({'url': BASE_URL + photo['path'], 'published': False, 'access_token': schedule['profile']['token']})
        fb_photo_request = Request("https://graph.facebook.com/v2.4/me/photos")
        fb_photo_response = json.loads(urlopen(fb_photo_request, data = fb_photo_data).read())
        media_id = "{\"media_fbid\":\"%s\"}" %(fb_photo_response['id'])
        photos_ids.append(media_id)

    fb_post_data =  {'message': schedule['post']['content'], 'access_token': schedule['profile']['token']}
    fb_post_request = Request("https://graph.facebook.com/v2.4/me/feed")

    for index, id in enumerate(photos_ids):
      fb_post_data["attached_media[%s]" %(index)] = id

    fb_post_data =  urllib.urlencode(fb_post_data)
    print fb_post_data
    fb_post_response = json.loads(urlopen(fb_post_request, data = fb_post_data).read())

log.flush()
log.close()
