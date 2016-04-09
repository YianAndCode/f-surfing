#!/usr/bin/env python
print "Checking..."
print "==============="
print
try:
    import urllib2
except ImportError, e:
    print e

try:
    import time
except ImportError, e:
    print e

try:
    import json
except ImportError, e:
    print e

try:
    import socket
except ImportError, e:
    print e

try:
    import uuid
except ImportError, e:
    print e

try:
    import hashlib
except ImportError, e:
    print e

print
print "==============="
print "Done."