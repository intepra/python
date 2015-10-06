#!/usr/bin/env python
import sys
import re
import shlex
from datetime import datetime

print >> sys.stderr, 'start mapper'

filename = sys.argv[1]
ipRegionList = []
with open(filename) as f:
    for line in f:
        fields = line.strip().split("\t")
        ipRegionList.append((fields[0], fields[1]))
ip_reg_dict = dict(ipRegionList)

date_format = "%d/%b/%Y"
for line in sys.stdin:
    items = shlex.split(line.lower())
    ip = items[0]
    bytes_count = items[7]
    browser = items[9]
    date = datetime.strptime(re.search('[0-3][0-9]/\S*/\d\d\d\d',items[3]).group(0), date_format)

    region = "unknown"
    if ip in ip_reg_dict:
        region = ip_reg_dict[ip]
    print '%s\t%s\t%s\t%s\t%s' % (ip, region, date.strftime("%y/%m/%d"), bytes_count, browser)



    