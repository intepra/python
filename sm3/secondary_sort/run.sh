#!/bin/bash
yarn jar /opt/hadoop/hadoop-streaming.jar \
-D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
-D stream.num.map.output.key.fields=2 \
-D mapred.text.key.partitioner.options=-k1,1 \
-D mapred.text.key.comparator.options="-k1 -k2" \
-files mapper.py,reducer.py \
-mapper "./mapper.py" \
-reducer "./reducer.py" \
-input /user/shtokhov/logs \
-output /user/shtokhov/ss1 \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner 
