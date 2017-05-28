# !/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen
import json
from api import BASE_URL

def authenticate(username='', password=''):
    auth_request = Request(BASE_URL + "oauth/token?username=root@root.com&password=root&grant_type=password")
    auth_request.add_header("Authorization", "Basic c29jaWFsY3Jvbjpzb2NpYWxjcm9u")
    auth_response = json.loads(urlopen(auth_request, data="").read())

    if auth_response['expires_in'] <= 120:
        refresh_request = Request(BASE_URL + "oauth/token?grant_type=refresh_token&refresh_token=" + auth_response['refresh_token'])
        refresh_request.add_header("Authorization", "Basic c29jaWFsY3Jvbjpzb2NpYWxjcm9u")
        refresh_request = json.loads(urlopen(refresh_request, data="").read())
        auth_response = refresh_request

    return auth_response
    