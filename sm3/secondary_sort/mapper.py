#!/usr/bin/env python
import sys
import re
import shlex
from datetime import datetime

print >> sys.stderr, 'start mapper'

date_format = "%d/%b/%Y"
for line in sys.stdin:
    items = shlex.split(line.lower())
    ip = items[0]
    bytes_count = items[7]
    browser = items[9]
    date = datetime.strptime(re.search('[0-3][0-9]/\S*/\d\d\d\d',items[3]).group(0), date_format)

    print '%s\t%s\t%s\t%s' % (ip, date.strftime("%Y/%m/%d"), bytes_count, browser)

print >> sys.stderr, 'end mapper'