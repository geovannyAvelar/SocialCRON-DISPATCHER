# -*- coding: utf-8 -*-

from api import BASE_URL
from urllib2 import Request, urlopen
import urllib
import json

def sendPost(content='', photos=[], token=''):
    photos_ids = savePhotos(photos, token)

    fb_post_data =  {'message': content, 'access_token': token}
    fb_post_request = Request("https://graph.facebook.com/v2.4/me/feed")

    for index, id in enumerate(photos_ids):
      fb_post_data["attached_media[%s]" %(index)] = id

    fb_post_data =  urllib.urlencode(fb_post_data)
    fb_post_response = json.loads(urlopen(fb_post_request, data = fb_post_data).read())

    return fb_post_response

def savePhotos(photos=[], token=''):
    photos_ids = []

    for photo in photos:
        fb_photo_data = urllib.urlencode({'url': BASE_URL + photo['path'], 'published': False, 'access_token': token})
        fb_photo_request = Request("https://graph.facebook.com/v2.4/me/photos")
        fb_photo_response = json.loads(urlopen(fb_photo_request, data = fb_photo_data).read())
        media_id = "{\"media_fbid\":\"%s\"}" %(fb_photo_response['id'])
        photos_ids.append(media_id)

    return photos_ids
