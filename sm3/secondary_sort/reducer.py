#!/usr/bin/env python
import sys
from datetime import datetime

const_user_days = 3

date_format = "%Y/%m/%d"

current_ip = None
prev_day = None
continues_days = 0
max_continues_days = 0
for line in sys.stdin:
    data = line.split('\t')
    ip = data[0]
    if (current_ip == ip):
        cur_day = datetime.strptime(data[1], date_format);
        delta = cur_day - prev_day
        if (delta.days == 1):
            continues_days = continues_days + 1
        if (delta.days > 1):
            if (continues_days > max_continues_days):
                max_continues_days = continues_days
            continues_days = 0
        prev_day = cur_day
    else:
        if (continues_days > max_continues_days):
                max_continues_days = continues_days

        if (max_continues_days > const_user_days):
            print '%s\t%s' % (current_ip, max_continues_days)
        current_ip = ip
        prev_day = datetime.strptime(data[1], date_format)
        continues_days = 1
        max_continues_days = 1

if (max_continues_days > const_user_days):
    print '%s\t%s' % (current_ip, max_continues_days)