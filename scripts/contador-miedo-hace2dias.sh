!#/bin/sh
source /home/ubuntu/repos/dlm/twitter/env/bin/activate
cd /home/ubuntu/repos/dlm/twitter/
ayer=$(date -d "2 days ago" +"%Y%m%d")
env/bin/python3 ./twittero.py contador miedo ${ayer}