# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen, HTTPError
from datetime import datetime
from api import BASE_URL
import log
import json

def get_schedules(dateFrom='', to='',token=''):
    try:
        schedules_request = Request(BASE_URL + "v2/schedules/range/%s/%s" %(dateFrom, to))
        schedules_request.add_header("Authorization", "Bearer " + token)
        schedules_response = urlopen(schedules_request).read()
        return json.loads(schedules_response)
    except HTTPError as error:
        log.error("Cannot retrieve schedules from server. %s %s" %(error.code, error.reason))
        return []

def mark_as_posted(id=-1, token=''):
    try:
        request = Request(BASE_URL + 'v2/schedules/' + str(id))
        request.add_header("Authorization", "Bearer " + token)
        response = urlopen(request).read()
        return json.loads(response)
    except HTTPError as error:
        log.error("Cannot mark schedule as complete. Server error. %s %s" %(error.code, error.reason))
        return {}
