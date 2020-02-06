#!/usr/bin/python3
import sys
sys.path.insert(0,"/var/www/blogprojectemz/")
sys.path.insert(0,"/var/www/blogprojectemz/blogprojectemz/")

import logging
logging.basicConfig(stream=sys.stderr)

from blogprojectemz import app as application
