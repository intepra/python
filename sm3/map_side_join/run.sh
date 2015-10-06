#!/bin/bash
yarn jar /opt/hadoop/hadoop-streaming.jar \
-files mapper.py,ip_region.txt \
-mapper "./mapper.py ip_region.txt" \
-input /user/shtokhov/logs \
-output /user/shtokhov/out2 \
