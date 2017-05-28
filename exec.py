# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from threading import Thread
import json
import facebook
import redis

log = file('dispatcher.log', 'a')
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

datetime_now = datetime.now().utcnow()
one_minute_after = datetime_now + timedelta(minutes = 1)

log.write('[DEBUG] - Dispatch executed at %s\n' %(datetime_now.strftime("%Y-%m-%dT%H:%M:%S%z")))

schedules_keys = redis.keys('*')

for key in schedules_keys:
    schedule = json.loads(redis.get(key))
    schedule_date = datetime.strptime(schedule['date'][0:-5], "%Y-%m-%dT%H:%M")
    token = schedule['profile']['token']

    if schedule_date > datetime_now and schedule_date < one_minute_after:

        if 'photos' in  schedule['post']:
            photos_ids = facebook.savePhotos(schedule['post']['photos'], token)

        content = schedule['post']['content']
        thread = Thread(target=facebook.sendPost, args=(content, photos_ids, token))
        thread.start()

log.flush()
log.close()
