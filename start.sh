#!/bin/bash

SOCK=/tmp/fundc.sock

echo 'kill nginx process, wait 5 seconds...'
nginx -s quit -c /data/apps/fundc/nginx.conf

sleep 5

echo 'kill fundc python process...'
ps -ef | grep fundc/manage.py | grep -v grep | awk '{print $2}' | xargs kill

echo 'start /data/apps/fundc/manage.py ...'
python2.6 /data/apps/fundc/manage.py runfcgi method=prefork maxrequests=1000 daemonize=true socket=$SOCK maxspare=10

echo 'start nginx... '
nginx -c /data/apps/fundc/nginx.conf

echo 'all is ok.'