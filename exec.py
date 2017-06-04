# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from threading import Thread
import log
import schedules_repository
import facebook

datetime_now = datetime.now().utcnow()
datetime_now = datetime_now.replace(second=1, microsecond=0)
one_minute_after = datetime_now + timedelta(minutes = 1)

log.info('Dispatch executed')

schedules = schedules_repository.find_all()

for schedule in schedules:
    token = schedule['profile']['token']

    if schedule['date'] > datetime_now and schedule['date'] < one_minute_after:
        log.info("Selecting schedule %s" %(schedule['id']))

        if 'photos' in  schedule['post']:
            photos_ids = facebook.savePhotos(schedule['post']['photos'], token)

        content = schedule['post']['content']
        thread = Thread(target=facebook.sendPost, args=(schedule['id'], content, photos_ids, token))
        thread.start()
