#!/usr/bin/env python

import sys

prev_ip = None
count = 0

for line in sys.stdin:
    items = line.split('\t')
    cur_ip = items[0]
    one = int(items[1])

    if cur_ip == prev_ip:
        count = count + one
    else:
        if prev_ip is not None:
            print "%s\t%s" % (prev_ip, count)
        prev_ip = cur_ip
        count = one
print "%s\t%s" % (prev_ip, count)
