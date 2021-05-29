!#/bin/sh
source /home/ubuntu/repos/dlm/twitter/env/bin/activate
cd /home/ubuntu/repos/dlm/twitter/
ayer=$(date -d "yesterday" +"%Y%m%d")
env/bin/python3 ./twittero.py dicenlosmedios ${ayer} lanacion politica-economia-internacional
