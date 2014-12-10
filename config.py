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
    HOST = 'localhost'
    NAME = 'django'
    USER = 'root'
    PASSWORD = 'zhouzhenhua'
    PORT = 3306
    ROUTERNAME = 'django'

class FundcDatabase:
    HOST = 'localhost'
    NAME = 'fundc'
    USER = 'root'
    PASSWORD = 'zhouzhenhua'
    PORT = 3306
    ROUTERNAME = 'fundc'
