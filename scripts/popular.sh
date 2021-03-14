!#/bin/sh
source /home/ec2-user/repos/dlm-twitter/env/bin/activate
cd /home/ec2-user/repos/dlm-twitter/
ayer=$(date -d "yesterday" +"%Y%m%d")
env/bin/python3 ./twittero.py dicenlosmedios ${ayer} popular politica-economia-sociedad-internacional
