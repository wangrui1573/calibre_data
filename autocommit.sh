#!/bin/bash
cd /docker/calibre/
pwd
git add . -A
git commit -m "cron auto commit"
git push oris
git push origin tencent
git status
