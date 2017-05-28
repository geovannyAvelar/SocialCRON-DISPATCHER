from api import BASE_URL
from flask import Flask, request, Response
from functools import wraps
from urllib2 import Request, urlopen
from datetime import datetime, timedelta
import auth
import time
import json
import os
import redis

app = Flask(__name__)
redis = redis.StrictRedis(host='localhost', port=6379, db=0)
log = file('dispatcher.log', 'a')

def check_auth(username, password):
  try:
    auth_response = auth.authenticate(username, password)
  except:
    return False
  
  return 'access_token' in auth_response

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/info", methods = ['GET'])
@requires_auth
def getInfo():
  log_lines = ''
  for line in file('dispatcher.log', 'r').readlines():
    log_lines = log_lines + line
   
  info = { 'synced_schedules': len(redis.keys("*")), 'log': log_lines}
  return Response(json.dumps(info), mimetype='application/json')


@app.route("/sync", methods = ['POST'])
@requires_auth
def sync():
  post = request.json

  auth_response = auth.authenticate('root@root.com', 'root')

  date = datetime.strptime(post['date'], '%Y-%m-%dT%H:%M+0000')
  now_timestamp = int(time.mktime(datetime.now().timetuple()))
  timestamp = int(time.mktime(date.timetuple()))
  diff = timestamp - now_timestamp

  if diff > 60:
    try:
      if not redis.exists('schedule:' + str(post['id'])):
        photos_request = Request(BASE_URL + "v2/photos/post/" + str(post['post']['id']))
        photos_request.add_header("Authorization", "Bearer " + auth_response['access_token'])
        photos_response = json.loads(urlopen(photos_request).read())
        post['post']['photos'] = []

        for photos in photos_response:
          post['post']['photos'].append(photos)

        redis.set('schedule:%s' %(post['id']), json.dumps(post), diff + 120)
        log.write("[DEBUG] - Schedule id %s stored. Will be posted at %s\n" %(post['id'], post['date']))
    except:
      log.write('[ERROR] - Error on redis\n')
      return "ERROR"

  return "OK"
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)