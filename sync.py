# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import log
import auth
import schedules
import schedules_repository

log.info('Sync started')

auth_response = auth.authenticate('root', 'root')

datetime_now = datetime.now().utcnow()
now = datetime_now.strftime("%Y-%m-%dT%H:%M") + "-0000"
final = (datetime_now + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M") + "-0000"

schedules = schedules.get_schedules(now, final, auth_response['access_token'])

for schedule in schedules:
   schedules_repository.save(schedule)

