#!/bin/bash
cd /docker/calibre/
pwd
git add . -A
git commit -m "cron auto commit"
git push origin tencent
git status

#cd /docker/wallabag
#pwd
#git add . -A
#git commit -m "cron auto commit"
#git push origin main
#git status

