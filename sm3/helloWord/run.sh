yarn jar /opt/hadoop/hadoop-streaming.jar \
-files mapper.py,reducer.py \
-mapper "./mapper.py" \
-combiner "./reducer.py" \
-reducer "./reducer.py" \
-input /user/shtokhov/logs \
-output /user/shtokhov/wc5
