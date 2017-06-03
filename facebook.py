# -*- coding: utf-8 -*-

from api import BASE_URL
from urllib2 import Request, urlopen, HTTPError
import log
import urllib
import json

def sendPost(content='', photos=[], token=''):
    photos_ids = savePhotos(photos, token)

    try:
        fb_post_data =  {'message': content, 'access_token': token}
        fb_post_request = Request("https://graph.facebook.com/v2.4/me/feed")

        for index, id in enumerate(photos_ids):
            fb_post_data["attached_media[%s]" %(index)] = id

        fb_post_data =  urllib.urlencode(fb_post_data)
        fb_post_response = json.loads(urlopen(fb_post_request, data = fb_post_data).read())
        log.info('Facebook response %s' %(fb_post_response))
        return fb_post_response
    except HTTPError as error:
        log.error("Cannot perform post on Facebook, %s %s" %(error.code, error.reason))    

def savePhotos(photos=[], token=''):
    photos_ids = []

    for photo in photos:
        try:
            fb_photo_data = urllib.urlencode({'url': BASE_URL + photo['path'], 'published': False, 'access_token': token})
            fb_photo_request = Request("https://graph.facebook.com/v2.4/me/photos")
            fb_photo_response = json.loads(urlopen(fb_photo_request, data = fb_photo_data).read())
            media_id = "{\"media_fbid\":\"%s\"}" %(fb_photo_response['id'])
            log.info("Photo %s saved on Facebook" %(fb_photo_response['id']))
            photos_ids.append(media_id)
        except HTTPError as error:
            log.error("Cannot post photo on Facebook, %s %s" %(error.code, error.reason))

    return photos_ids

