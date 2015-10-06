#!/usr/bin/env python

import sys
import shlex

print >> sys.stderr, 'start mapper'

for line in sys.stdin:
    items = shlex.split(line.lower())
    ip = items[0]
    print "%s\t%s" % (ip, "1")