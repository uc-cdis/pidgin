#!/bin/bash

cd /var/www/$appname

(
  # Wait for nginx to create uwsgi.sock
  let count=0
  while [[ (! -e uwsgi.sock) && count -lt 10 ]]; do
    sleep 2
    let count="$count+1"
  done
  if [[ ! -e uwsgi.sock ]]; then
    echo "WARNING: /var/www/$appname/uwsgi.sock does not exist!!!"
  fi
  uwsgi --ini /etc/uwsgi/uwsgi.ini
) &

nginx -g 'daemon off;'
