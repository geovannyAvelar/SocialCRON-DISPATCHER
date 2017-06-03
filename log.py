# -*- coding: utf-8 -*-

from datetime import datetime

log = file('dispatcher.log', 'a')

def debug(message=''):
  log.write('[DEBUG] - %s - %s\n' %(get_date(), message))
  log.flush()
  log.close

def info(message=''):
  log.write('[INFO] - %s - %s\n' %(get_date(), message))
  log.flush()
  log.close

def error(message=''):
  log.write('[ERROR] - %s - %s\n' %(get_date(), message))
  log.flush()
  log.close

def get_date():
  return datetime.now()