# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import auth
import log
import photos
import redis
import time
import json

redis = redis.StrictRedis(host='localhost', port=6379, db=0)
api_auth = auth.authenticate('root', 'root')

def save(schedule):
    date = datetime.strptime(schedule['date'], '%Y-%m-%dT%H:%M:%s+0000')
    now_timestamp = int(time.mktime(datetime.now().timetuple()))
    timestamp = int(time.mktime(date.timetuple()))
    diff = timestamp - now_timestamp

    if diff > 60:
        schedule['post']['photos'] = []
        photos_response = photos.find_photos_by_post(schedule['post']['id'], api_auth['access_token'])

        for photos_data in photos_response:
            schedule['post']['photos'].append(photos_data)

        redis.set('schedule:%s' %(schedule['id']), json.dumps(schedule), diff + 120)
        log.info('Schedule %s has been synchronized. Will be executed at %s' %(schedule['id'], schedule['date']))

def find_all():
    schedules_keys = redis.keys('*')
    schedules = []

    for key in schedules_keys:
        schedule = json.loads(redis.get(key))
        schedule['date'] = datetime.strptime(schedule['date'][0:-5] + ":30", "%Y-%m-%dT%H:%M:%S")
        schedules.append(schedule)

    return schedules

