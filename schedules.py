# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen
from datetime import datetime
from api import BASE_URL
import json

def get_schedules(dateFrom='', to='',token=''):
    schedules_request = Request(BASE_URL + "v2/schedules/range/%s/%s" %(dateFrom, to))
    schedules_request.add_header("Authorization", "Bearer " + token)
    schedules_response = urlopen(schedules_request).read()
    return json.loads(schedules_response)

def mark_as_posted(id=-1, token=''):
    request = Request(BASE_URL + 'v2/schedules/' + str(id))
    request.add_header("Authorization", "Bearer " + token)
    request = urlopen(request).read()
    return json.loads(request)
