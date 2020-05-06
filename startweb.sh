#! /bin/bash
. ~/miniconda3/bin/activate
nohup sudo sh -c ". /home/ubuntu/miniconda3/bin/activate && python manage.py runserver --insecure 0.0.0.0:80"  >/home/ubuntu/web.log 2>&1 &
echo 'starting....'

