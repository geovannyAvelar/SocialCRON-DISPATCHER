# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen, HTTPError
from api import BASE_URL
import log
import json

def find_photos_by_post(id=-1,token=''):
    try:
        photos_request = Request(BASE_URL + "v2/photos/post/" + str(id))
        photos_request.add_header("Authorization", "Bearer " + token)
        photos_response = urlopen(photos_request).read()
        return json.loads(photos_response)
    except HTTPError:
        log.error('Cannot retrieve photos on post saving')