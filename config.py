#coding:utf-8

import os
import sys

sys.path.append(os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'fundc.settings'

DEBUG = False

class Path:
    PROJECT = os.path.dirname(__file__)
    if os.name == 'nt':
        DATA = r'D:\data\fundc'
        LOG = r'D:\data\logs\fundc'
    else:
        DATA = '/data/appdatas/fundc'
        LOG = '/data/logs/fundc'
    WEB = os.path.join(PROJECT, 'web')
    FILE_LOCKER = os.path.join(DATA, 'filelocker')
    BACKUP = os.path.join(DATA, 'backup')
    TEMP = os.path.join(DATA, 'temp')

class DjangoDatabase:
    HOST = 'fundc12345678.mysql.rds.aliyuncs.com'
    NAME = 'django'
    USER = 'myadmin'
    PASSWORD = 'myadmin3335688'
    PORT = 3306
    ROUTERNAME = 'django'

class FundcDatabase:
    HOST = 'fundc12345678.mysql.rds.aliyuncs.com'
    NAME = 'fundc'
    USER = 'myadmin'
    PASSWORD = 'myadmin3335688'
    PORT = 3306
    ROUTERNAME = 'fundc'

class OkCoin:
    ApiKey = '250e4df5-a023-4017-82c5-676625e2b54b'
    SecretKey = 'FE7B5462F294969CAF05FC2007F1539C'